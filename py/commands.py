from collections import namedtuple
import curses
from caverlib.world.mapping import Point

class Command(namedtuple('Command', ['name','keys','target'])):
    __slots__ = ()


def get_all_commands(command_list, input_char):
    return [c for c in command_list if input_char in c.keys]

def get_first_command(command_list, input_char):
    for c in command_list:
        if input_char in c.keys:
            return c
    return None

# transformation for each key
NAVIGATION_MOVES = [
    
    Command(
        'move_left',
        [curses.KEY_LEFT, ord('h')],
        Point(-1, 0)
    ),

    Command(
        'move_right',
        [curses.KEY_RIGHT, ord('l')],
        Point(1, 0)
    ),

    Command(
        'move_up',
        [curses.KEY_UP, ord('k')],
        Point(0,-1)
    ),

    Command(
        'move_down',
        [curses.KEY_DOWN, ord('j')],
        Point(0, 1)
    ),

    Command(
        'move_diag_upleft',
        [curses.KEY_A1, ord('y')],
        Point(-1, -1)
    ),

    Command(
        'move_diag_upright',
        [curses.KEY_A3, ord('u')],
        Point(1, -1)
    ),

    Command(
        'move_diag_downright',
        [curses.KEY_C3, ord('m')],
        Point(1, 1)
    ),

    Command(
        'move_diag_downleft',
        [curses.KEY_C1, ord('n')],
        Point(-1, 1)
    ),

]

SYSTEM_COMMANDS = [
    Command(
        'exit_program',
        [ord('Q')],
        None),

    Command(
        'print_map',
        [ord('p')],
        None),
]

