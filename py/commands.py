from collections import namedtuple
import curses
from caverlib.world.mapping import Point

class CommandInterpreter():
    
    keyreg = None

    def __init__(self, message_bus, config):
        self.message_bus = message_bus
        self.config = config
        self.message_bus.register('key_press', self.key_press)
        self.message_bus.register('mode_change', self.set_mode)

    def __del__(self):
        self.message_bus.unregister('key_press', self.key_press)
        self.message_bus.unregister('mode_change', self.set_mode)

    def set_mode(self, new_mode):
        if new_mode not in UI_MODES:
            raise ValueError('mode %s does not exist' % new_mode)
        
        self.mode = new_mode
        
        del keyreg
        keyreg = {}
        for cmdlist in self.config:
            for cmd in cmdlist:
                for key in cmd['key']:
                    if key in keyreg:
                        raise Exception('Duplicate key registration of %s for mode %s' % (key, new_mode))
                    keyreg[key] = cmd['action']


    def key_press(self, key):
        if not key in self.keyreg:
            return
        self.message_bus.send(self.keyreg[key])

UI_MODES = {
    'main_menu': ['system','main_menu'],
    'browse' : ['system', 'navigation']
}

