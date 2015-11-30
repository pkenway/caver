# how to display elements in the game world

from caverlib.world import terrain, entities
import curses

# displays consiste of an ascii value and a color scheme in a tuple


# Texture palette!
# ╔═╦═╗╓─╥─╖╒═╤═╕┌─┬─┐
# ║ ║ ║║ ║ ║│ │ ││ │ │
# ╠═╬═╣╟─╫─╢╞═╪═╡├─┼─┤
# ║ ║ ║║ ║ ║│ │ ││ │ │
# ╚═╩═╝╙─╨─╜╘═╧═╛└─┴─┘
# ░▒▓

# colors: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white

WHITE = 0 #white on black is always 0 in curses
RED = 1
YELLOW = 2
BLUE = 3
GREEN = 4




def init_color_pairs():
    bg = curses.COLOR_BLACK
    # curses.init_pair(WHITE, curses.COLOR_WHITE, bg)

    curses.init_pair(RED, curses.COLOR_RED, bg)
    curses.init_pair(YELLOW, curses.COLOR_YELLOW, bg)
    curses.init_pair(BLUE, curses.COLOR_BLUE, bg)
    curses.init_pair(GREEN, curses.COLOR_GREEN, bg)


# tile display

BLANK = (ord(' '), WHITE)

TILE_DISPLAYS = {
    terrain.LayerTypes.Rock: (ord('#'),WHITE),
    terrain.LayerTypes.Sand: (ord('.'), YELLOW),
    terrain.LayerTypes.Mud: (ord('*'), RED),
    terrain.WaterTypes.Still: (ord('.'), BLUE)
}

ENTITY_DISPLAYS = {
    'stick': (ord('|'), WHITE),
    'rock': (ord('*'), WHITE),
    'bear': (ord('B'), RED),
    'hero': (ord('@'), GREEN),
}


DOUBLE_PIPES = [
    ((terrain.Dir.UP, terrain.Dir.DOWN), '║'),
    ((terrain.Dir.UP, terrain.Dir.LEFT), '╝'),
    ((terrain.Dir.UP, terrain.Dir.RIGHT), '╚'),
    ((terrain.Dir.LEFT, terrain.Dir.RIGHT), '═'),
    ((terrain.Dir.LEFT, terrain.Dir.DOWN), '╗'),
    ((terrain.Dir.DOWN, terrain.Dir.RIGHT), '╔'),
]


def get_pipe_display(directions):
    if not directions[0] or not directions[1]:
        return '▓'

    if directions[0].value > directions[1].value:
        directions = tuple(reversed(directions))

    for dirs in DOUBLE_PIPES:
        if dirs[0] == directions:
            return dirs[1]
    return '▓'


def get_tile_display(tile):

    visible_entity = entities.visible_entity(tile.entities)
    if visible_entity:
        # display the uppermost visible entity
        # visible entities MUST have a display in ENTITY_DISPLAYS!
        return ENTITY_DISPLAYS[visible_entity[0]]

    if tile.composition in TILE_DISPLAYS:
        return TILE_DISPLAYS[tile.composition]

    # water depends on direction
    if tile.composition == terrain.FloorTypes.Water:
        tile_char = get_pipe_display(tile.props['direction'])

        return(tile_char, BLUE)

    raise ValueError('Tile type not found %s', tile_type)
    
