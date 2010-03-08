# coding: utf-8
from twisted.internet.defer import DeferredQueue

class Empty(Exception):
    pass

class Closed(Exception):
    pass

class TimeoutDeferredQueue(DeferredQueue):

    END = object()

    def __init__(self, clock=None):
        if clock is None:
            from twisted.internet import reactor as clock
        self.clock = clock
        DeferredQueue.__init__(self)

    def _timeout(self, deferred):
        if not deferred.called:
            if deferred in self.waiting:
                self.waiting.remove(deferred)
                deferred.errback(Empty())

    def _raiseIfClosed(self, result, call_id):
        if call_id is not None:
            call_id.cancel()
        if result == TimeoutDeferredQueue.END:
            self.put(TimeoutDeferredQueue.END)

            raise Closed()
        else:
            return result

    def get(self, timeout=None):
        deferred = DeferredQueue.get(self)

        call_id = None
        if timeout:
            call_id = self.clock.callLater(timeout, self._timeout, deferred)
        deferred.addCallback(self._raiseIfClosed, call_id)

        return deferred

    def close(self):
        self.put(TimeoutDeferredQueue.END)
