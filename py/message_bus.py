from collections import defaultdict
from enum import Enum


class MessageBus():
    def __init__(self, logger=None):
        self.logger = logger
        self.listeners = defaultdict(list)

    def register(self, key, listener):
        self.listeners[key].append(listener)

    def unregister(self, key, listener):
        self.listeners[key].remove(listener)

    def send(self, key, data=None):

        if not isinstance(key, MType):
            raise Exception('%s is not a valid message' % key)

        if self.logger:
            logger.log('message: %s' % key)

        for listener in self.listeners[key]:
            listener(data)


# types of messages
class MType(Enum):

    #player actinos
    NAVIGATE = 0
    KEY_PRESS = 1

    #game actions
    TICK = 100
    SET_VIEW_COORDS = 101
    SET_MAP = 102
    SET_GAME_MODE = 103
    REQUEST_INPUT = 104
    EXIT_PROGRAM = 105
