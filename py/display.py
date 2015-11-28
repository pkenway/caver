# how to display elements in the game world

from generator import terrain
import curses

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
    terrain.LayerTypes.Rock: ('#',WHITE),
    terrain.LayerTypes.Sand: ('.', YELLOW),
    terrain.LayerTypes.Mud: ('*', RED),
    terrain.WaterTypes.Still: ('.', BLUE)
}

TILE_DISPLAYS 

def get_tile_display(tile):
    if tile.composition not in TILE_DISPLAYS:
        raise ValueError('Tile type not found %s', tile_type)
    return TILE_DISPLAYS[tile.composition]
