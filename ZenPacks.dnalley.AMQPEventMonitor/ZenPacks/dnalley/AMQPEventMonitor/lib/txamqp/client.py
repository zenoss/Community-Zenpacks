# coding: utf-8
from twisted.internet import defer
from txamqp.delegate import Delegate

class Closed(Exception):
    pass

class TwistedEvent(object):
    def __init__(self):
        self.deferred = defer.Deferred()
        self.alreadyCalled = False

    def set(self):
        self.deferred.callback(True)

    def wait(self):
        return self.deferred

    def reset(self):
        deferred, self.deferred = self.deferred, defer.Deferred()
        deferred.callback(True)

class TwistedDelegate(Delegate):

    def connection_start(self, ch, msg):
        ch.connection_start_ok(mechanism=self.client.mechanism,
                               response=self.client.response,
                               locale=self.client.locale)

    def connection_tune(self, ch, msg):
        self.client.MAX_LENGTH = msg.frame_max
        args = msg.channel_max, msg.frame_max, self.client.heartbeatInterval
        ch.connection_tune_ok(*args)
        self.client.started.reset()

    @defer.inlineCallbacks
    def basic_deliver(self, ch, msg):
        queue = self.client.queue(msg.consumer_tag)
        yield queue
        queue.put(msg)

    def basic_return_(self, ch, msg):
        self.client.basic_return_queue.put(msg)

    def channel_close(self, ch, msg):
        ch.close(msg)

    def connection_close(self, ch, msg):
        self.client.close(msg)

    def close(self, reason):
        self.client.closed = True
        self.client.started.reset()
