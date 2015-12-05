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
        if self.logger:
            logger.log('message: %s' % key)

        for listener in self.listeners[key]:
            listener(data)

# types of messages
class MType(Enum):

    #player actinos
    NAVIGATE = 'NAVIGATE'
    KEY_PRESS = 'KEY_PRESS'

    #game actions
    TICK = 'TICK'
    SET_VIEW_COORDS = 'SET_VIEW_COORDS'
    SET_MAP = 'SET_MAP'
    SET_GAME_MODE = 'SET_GAME_MODE'
    REQUEST_INPUT = 'REQUEST_INPUT'
    EXIT_PROGRAM = 'EXIT_PROGRAM'
