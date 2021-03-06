import config_loader
import message_bus
import commands
import screen
import game_state
from caverlib.world.mapping import Point
from data.config.commands import COMMAND_LIST

CONFIG_FOLDER = '../data/config'

print('loading...')
mode_stack = []

# load game engine with message bus
msg_bus = message_bus.MessageBus()
game_state = game_state.GameState(msg_bus)
cmd_interpreter = commands.CommandInterpreter(msg_bus, COMMAND_LIST)
screen =screen.Screen(msg_bus, game_state)

# main menu

# activate main menu command mode

# trigger main menu display


# in game
game_state.new_game()

print('loading graphics...')
screen.init_graphics()

#runloop
while True:
    msg_bus.send(message_bus.MType.TICK)
    msg_bus.send(message_bus.MType.REQUEST_INPUT)
