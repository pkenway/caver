import curses
from curses import wrapper
from caverlib.world.mapping import Point
from caverlib.world.entities import entities
from caverlib.logging import log
from enum import Enum
import display
import commands
from itertools import chain
from message_bus import MType
#constants
MAX_INPUT_BUFFER = 1024

# Renders the screen and handles keyboard input via curses

class Screen():

    def __init__(self, message_bus, game_state):
        self.message_bus = message_bus
        self.game_state = game_state
        self.message_bus.register(MType..EXIT_PROGRAM, self.exit)
        self.message_bus.register(MType.SET_VIEW_COORDS, self.set_coords)
        self.message_bus.register(MType.TICK, self.draw_screen)
        self.message_bus.register(MType.REQUST_INPUT, self.get_input)
        self.exit = False
        self.input_buffer = []

    def exit():
        self.exit = True

    def init_graphics(self):
        wrapper(self.on_screen_init)

    def on_screen_init(self, stdscr):
        self.stdscr = stdscr

    def set_coords(self, data):
        self.screen_coords = data

    def draw_screen(self, data):
        top_left, size = self.get_viewbox()
        if self.tile_map:
            write_map_to_pad(self.game_state.tile_map, pad, top_left.y, top_left.x, size.y, size.x)

    def get_input(self):
        new_key = self.stdscr.getch()
        self.message_bus.send('key_press', new_key)
 
    def screen_size(self):
        return Point(reversed(self.stdscr.getmaxyx()))

    def get_viewbox(self):
        topleft = self.game_state.view_coords - (self.screen_size() / 2)
        size = topleft + self.screen_size()
        return topleft, size


def write_map_to_pad(tile_map, pad, start_x, start_y, width, height):
    for y in range(start_y, start_y + height):  
        for x in range(start_x, start_x + width):
            coords = Point(x, y)          
            if not tile_map.valid_coords(coords):
                tile_display = display.BLANK
            else:
                tile_display = display.get_tile_display(tile_map.get_tile_at(coords))
            pad.addch(y, x, tile_display[0], curses.color_pair(tile_display[1]))
            
    pad.refresh(start_y, start_x,  0, 0, height - 1, width - 1)


if __name__ == '__main__':
    tile_map = cave_generator.generate_map(width=500, height=500, layer_count=30)
    wrapper(browse_map, tile_map)




