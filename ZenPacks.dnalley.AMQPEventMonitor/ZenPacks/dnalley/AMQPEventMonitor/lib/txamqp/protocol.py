# coding: utf-8
from twisted.python import log
from twisted.internet import defer, protocol, reactor
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
from txamqp import spec
from txamqp.codec import Codec, EOF
from txamqp.connection import Header, Frame, Method, Body, Heartbeat
from txamqp.message import Message
from txamqp.content import Content
from txamqp.queue import TimeoutDeferredQueue, Empty, Closed as QueueClosed
from txamqp.client import TwistedEvent, TwistedDelegate, Closed
from cStringIO import StringIO
import struct
from time import time

class GarbageException(Exception):
    pass

# An AMQP channel is a virtual connection that shares the
# same socket with others channels. One can have many channels
# per connection
class AMQChannel(object):

    def __init__(self, id, outgoing):
        self.id = id
        self.outgoing = outgoing
        self.incoming = TimeoutDeferredQueue()
        self.responses = TimeoutDeferredQueue()

        self.queue = None

        self.closed = False
        self.reason = None

    def close(self, reason):
        if self.closed:
            return
        self.closed = True
        self.reason = reason
        self.incoming.close()
        self.responses.close()

    def dispatch(self, frame, work):
        payload = frame.payload
        if isinstance(payload, Method):
            if payload.method.response:
                self.queue = self.responses
            else:
                self.queue = self.incoming
                work.put(self.incoming)
        self.queue.put(frame)

    @defer.inlineCallbacks
    def invoke(self, method, args, content = None):
        if self.closed:
            raise Closed(self.reason)
        frame = Frame(self.id, Method(method, *args))
        self.outgoing.put(frame)

        if method.content:
            if content == None:
                content = Content()
            self.writeContent(method.klass, content, self.outgoing)

        try:
            # here we depend on all nowait fields being named nowait
            f = method.fields.byname["nowait"]
            nowait = args[method.fields.index(f)]
        except KeyError:
            nowait = False

        try:
            if not nowait and method.responses:
                resp = self.responses.get()
                yield resp
                resp = resp.payload

                if resp.method.content:
                    content = readContent(self.responses)
                    yield content
                else:
                    content = None
                if resp.method in method.responses:
                    defer.returnValue(Message(resp.method, resp.args, content))
                else:
                    raise ValueError(resp)
        except QueueClosed, e:
            if self.closed:
                raise Closed(self.reason)
            else:
                raise e

    def writeContent(self, klass, content, queue):
        size = content.size()
        header = Frame(self.id, Header(klass, content.weight(), size, **content.properties))
        queue.put(header)
        for child in content.children:
            self.writeContent(klass, child, queue)
        # should split up if content.body exceeds max frame size
        if size > 0:
            queue.put(Frame(self.id, Body(content.body)))

class FrameReceiver(protocol.Protocol, basic._PauseableMixin):

    frame_mode = False
    MAX_LENGTH = 4096
    HEADER_LENGTH = 1 + 2 + 4 + 1
    __buffer = ''

    def __init__(self, spec):
        self.spec = spec
        self.FRAME_END = self.spec.constants.bypyname["frame_end"].id

    # packs a frame and writes it to the underlying transport
    def sendFrame(self, frame):
        data = self._packFrame(frame)
        self.transport.write(data)

    # packs a frame, see qpid.connection.Connection#write
    def _packFrame(self, frame):
        s = StringIO()
        c = Codec(s)
        c.encode_octet(self.spec.constants.bypyname[frame.payload.type].id)
        c.encode_short(frame.channel)
        frame.payload.encode(c)
        c.encode_octet(self.FRAME_END)
        data = s.getvalue()
        return data

    # unpacks a frame, see qpid.connection.Connection#read
    def _unpackFrame(self, data):
        s = StringIO(data)
        c = Codec(s)
        frameType = spec.pythonize(self.spec.constants.byid[c.decode_octet()].name)
        channel = c.decode_short()
        payload = Frame.DECODERS[frameType].decode(self.spec, c)
        end = c.decode_octet()
        if end != self.FRAME_END:
            raise GarbageException('frame error: expected %r, got %r' % (self.FRAME_END, end))
        frame = Frame(channel, payload)
        return frame

    def setRawMode(self):
        self.frame_mode = False

    def setFrameMode(self, extra=''):
        self.frame_mode = True
        if extra:
            return self.dataReceived(extra)

    def dataReceived(self, data):
        self.__buffer = self.__buffer + data
        while self.frame_mode and not self.paused:
            sz = len(self.__buffer) - self.HEADER_LENGTH
            if sz >= 0:
                length, = struct.unpack("!I", self.__buffer[3:7]) # size = 4 bytes
                if sz >= length:
                    packet = self.__buffer[:self.HEADER_LENGTH + length]
                    self.__buffer = self.__buffer[self.HEADER_LENGTH + length:]
                    frame = self._unpackFrame(packet)

                    why = self.frameReceived(frame)
                    if why or self.transport and self.transport.disconnecting:
                        return why
                    else:
                        continue
            if len(self.__buffer) > self.MAX_LENGTH:
                frame, self.__buffer = self.__buffer, ''
                return self.frameLengthExceeded(frame)
            break
        else:
            if not self.paused:
                data = self.__buffer
                self.__buffer = ''
                if data:
                    return self.rawDataReceived(data)

    def sendInitString(self):
        initString = "!4s4B"
        s = StringIO()
        c = Codec(s)
        c.pack(initString, "AMQP", 1, 1, self.spec.major, self.spec.minor)
        self.transport.write(s.getvalue())

@defer.inlineCallbacks
def readContent(queue):
    frame = queue.get()
    yield frame
    header = frame.payload
    children = []
    for i in range(header.weight):
        content = readContent(queue)
        yield content
        children.append(content)
    size = header.size
    read = 0
    buf = StringIO()
    while read < size:
        body = queue.get()
        yield body
        content = body.payload.content
        buf.write(content)
        read += len(content)
    defer.returnValue(Content(buf.getvalue(), children, header.properties.copy()))

class AMQClient(FrameReceiver):

    channelClass = AMQChannel

    # Max unreceived heartbeat frames. The AMQP standard says it's 3.
    MAX_UNSEEN_HEARTBEAT = 3

    def __init__(self, delegate, vhost, spec, heartbeat=0):
        FrameReceiver.__init__(self, spec)
        self.delegate = delegate

        # XXX Cyclic dependency
        self.delegate.client = self

        self.vhost = vhost

        self.channelFactory = type("Channel%s" % self.spec.klass.__name__,
                                    (self.channelClass, self.spec.klass), {})
        self.channels = {}
        self.channelLock = defer.DeferredLock()

        self.outgoing = defer.DeferredQueue()
        self.work = defer.DeferredQueue()

        self.started = TwistedEvent()

        self.queueLock = defer.DeferredLock()
        self.basic_return_queue = TimeoutDeferredQueue()

        self.queues = {}

        self.outgoing.get().addCallback(self.writer)
        self.work.get().addCallback(self.worker)
        self.heartbeatInterval = heartbeat
        if self.heartbeatInterval > 0:
            self.checkHB = reactor.callLater(self.heartbeatInterval *
                          self.MAX_UNSEEN_HEARTBEAT, self.checkHeartbeat)
            self.sendHB = LoopingCall(self.sendHeartbeat)
            d = self.started.wait()
            d.addCallback(lambda _: self.reschedule_sendHB())
            d.addCallback(lambda _: self.reschedule_checkHB())

    def reschedule_sendHB(self):
        if self.heartbeatInterval > 0:
            if self.sendHB.running:
                self.sendHB.stop()
            self.sendHB.start(self.heartbeatInterval, now=False)

    def reschedule_checkHB(self):
        if self.checkHB.active():
            self.checkHB.cancel()
        self.checkHB = reactor.callLater(self.heartbeatInterval *
              self.MAX_UNSEEN_HEARTBEAT, self.checkHeartbeat)

    def check_0_8(self):
        return (self.spec.minor, self.spec.major) == (0, 8)

    @defer.inlineCallbacks
    def channel(self, id):
        yield self.channelLock.acquire()
        try:
            try:
                ch = self.channels[id]
            except KeyError:
                ch = self.channelFactory(id, self.outgoing)
                self.channels[id] = ch
        finally:
            self.channelLock.release()
        defer.returnValue(ch)

    @defer.inlineCallbacks
    def queue(self, key):
        yield self.queueLock.acquire()
        try:
            try:
                q = self.queues[key]
            except KeyError:
                q = TimeoutDeferredQueue()
                self.queues[key] = q
        finally:
            self.queueLock.release()
        defer.returnValue(q)

    def close(self, reason):
        for ch in self.channels.values():
            ch.close(reason)
        for q in self.queues.values():
            q.close()
        self.delegate.close(reason)

    def writer(self, frame):
        self.sendFrame(frame)
        self.outgoing.get().addCallback(self.writer)

    def worker(self, queue):
        d = self.dispatch(queue)
        def cb(ign):
            self.work.get().addCallback(self.worker)
        d.addCallback(cb)
        d.addErrback(self.close)

    @defer.inlineCallbacks
    def dispatch(self, queue):
        frame = queue.get()
        yield frame
        channel = self.channel(frame.channel)
        yield channel
        payload = frame.payload
        if payload.method.content:
            content = readContent(queue)
            yield content
        else:
            content = None
        # Let the caller deal with exceptions thrown here.
        message = Message(payload.method, payload.args, content)
        self.delegate.dispatch(channel, message)

    # As soon as we connect to the target AMQP broker, send the init string
    def connectionMade(self):
        self.sendInitString()
        self.setFrameMode()

    def frameReceived(self, frame):
        self.processFrame(frame)

    def sendFrame(self, frame):
        if frame.payload.type != Frame.HEARTBEAT:
            self.reschedule_sendHB()
        FrameReceiver.sendFrame(self, frame)

    @defer.inlineCallbacks
    def processFrame(self, frame):
        ch = self.channel(frame.channel)
        yield ch
        if frame.payload.type == Frame.HEARTBEAT:
            self.lastHBReceived = time()
        else:
            ch.dispatch(frame, self.work)
        if self.heartbeatInterval > 0:
            self.reschedule_checkHB()

    @defer.inlineCallbacks
    def authenticate(self, username, password, mechanism='AMQPLAIN', locale='en_US'):
        if self.check_0_8():
            response = {"LOGIN": username, "PASSWORD": password}
        else:
            response = "\0" + username + "\0" + password

        yield self.start(response, mechanism, locale)

    @defer.inlineCallbacks
    def start(self, response, mechanism='AMQPLAIN', locale='en_US'):
        self.response = response
        self.mechanism = mechanism
        self.locale = locale

        yield self.started.wait()

        channel0 = self.channel(0)
        yield channel0
        yield channel0.connection_open(self.vhost)

    def sendHeartbeat(self):
        self.sendFrame(Frame(0, Heartbeat()))
        self.lastHBSent = time()

    def checkHeartbeat(self):
        if self.checkHB.active():
            self.checkHB.cancel()
        self.transport.loseConnection()

    def connectionLost(self, reason):
        if self.heartbeatInterval > 0:
            if self.sendHB.running:
                self.sendHB.stop()
            if self.checkHB.active():
                self.checkHB.cancel()
        self.close(reason)

