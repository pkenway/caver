# how to display elements in the game world

from caverlib.world import terrain
import curses


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
def init_color_pairs():
    bg = curses.COLOR_BLACK
    # curses.init_pair(WHITE, curses.COLOR_WHITE, bg)

    curses.init_pair(RED, curses.COLOR_RED, bg)
    curses.init_pair(YELLOW, curses.COLOR_YELLOW, bg)
    curses.init_pair(BLUE, curses.COLOR_BLUE, bg)


# tile display

TILE_DISPLAYS = {
    terrain.LayerTypes.Rock: (ord('#'),WHITE),
    terrain.LayerTypes.Sand: (ord('.'), YELLOW),
    terrain.LayerTypes.Mud: (ord('*'), RED),
    terrain.WaterTypes.Still: (ord('.'), BLUE)
}

TILE_DISPLAYS 



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
    if tile.composition in TILE_DISPLAYS:
        return TILE_DISPLAYS[tile.composition]

    # water depends on direction
    if tile.composition == terrain.FloorTypes.Water:
        tile_char = get_pipe_display(tile.props['direction'])

        return(tile_char, BLUE)

    raise ValueError('Tile type not found %s', tile_type)
    
