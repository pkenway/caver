import config_loader
import message_bus
import commands
import screen
import game_state
from caverlib.world.mapping import Point
CONFIG_FOLDER = '../data/config'

print('loading...')
mode_stack = []

# load game engine with message bus
message_bus = message_bus.MessageBus()
game_state = game_state.GameState(message_bus)
command_config = config_loader.get_config('../data/config', 'commands') 
cmd_interpreter = commands.CommandInterpreter(message_bus, command_config)
screen =screen.Screen(message_bus, game_state)

# main menu

# activate main menu command mode

# trigger main menu display


# in game
game_state.new_game()

print('loading graphics...')
screen.init_graphics()

#runloop
while True:
    message_bus.send('tick')
    message_bus.send('get_input')
