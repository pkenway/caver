from collections import namedtuple
import curses
from caverlib.world.mapping import Point
from message_bus import MType

class CommandInterpreter():

    def __init__(self, message_bus, command_list):
        self.message_bus = message_bus
        self.command_list = command_list
        self.key_bindings = None
        self.input_buffer = []
        self.message_bus.register(MType.KEY_PRESS, self.key_press)
        self.message_bus.register(MType.SET_GAME_MODE, self.set_mode)
 
    def __del__(self):
        self.message_bus.unregister(MType.KEY_PRESS, self.key_press)
        self.message_bus.unregister(MType.SET_GAME_MODE, self.set_mode)

    @staticmethod
    def get_key_bindings(mode, command_list):
        # in python 3.5 could use this comprehension.  Maybe faster than `update()`?
        # return  { **bindings for bindings in grouping for grouping in command_list if mode in grouping.modes }
        key_bindings = {}
        for keyset in command_list:
            if mode not in keyset['modes']:
                continue
            key_bindings.update(keyset['bindings'])
        return key_bindings

    def set_mode(self, new_mode):
        if new_mode not in UI_MODES:
            raise ValueError('mode %s does not exist' % new_mode)
        
        self.mode = new_mode
        if self.key_bindings:
            del self.key_bindings
        
        self.key_bindings = self.get_key_bindings(new_mode, self.command_list)

    def get_action_by_key(self, key):
        if key in self.key_bindings:
            self.input_buffer.clear()
            return self.key_bindings[key]
        self.input_buffer

    def key_press(self, key):
        self.input_buffer.append(key)

        #check if the entire input buffer matches
        # if ''.join(str(self.input_buffer)) in self.key_bindings:
        #     action = self.key_bindings[self.input_buffer]

        # check if the last key matches
        if key in self.key_bindings:
            action = self.key_bindings[key]

        if not action:
            self.input_buffer.append(key)
            return

        self.input_buffer.clear()
        self.message_bus.send(action['action'], action['data'])


UI_MODES = {
    'main_menu': ['system','main_menu'],
    'browse' : ['system', 'navigation']
}

