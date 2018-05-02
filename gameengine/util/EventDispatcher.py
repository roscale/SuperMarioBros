class EventDispatcher:
    def __init__(self, sender):
        self._sender = sender
        self._handlers = []

    def notify(self, *args):
        for h in self._handlers:
            h(self._sender, *args)

    def addHandler(self, h):
        if h not in self._handlers:
            self._handlers.append(h)
        return self

    def removeHandler(self, h):
        if h in self._handlers:
            self._handlers.remove(h)
        return self

    def clearHandlers(self):
        self._handlers = []

    __iadd__ = addHandler
    __isub__ = removeHandler
    __call__ = notify