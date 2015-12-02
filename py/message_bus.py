from collections import defaultdict

class MessageBus():
    def __init__(self):
        self.listeners = defaultdict(list)

    def register(self, key, listener):
        self.listeners[key].append(listener)

    def unregister(self, key, listener):
        self.listeners[key].remove(listener)

    def send(self, key, data=None):
        for listener in self.listeners[key]:
            listener(data)

