import curses
from curses import wrapper
from environment import cave_generator
from user_input import Getch
from logging import log
from enum import Enum



def browse_map(stdscr, tile_map):
    screen_size = stdscr.getmaxyx()
    log('screen dimensions: %d x %d' % (screen_size[1], screen_size[0]))
    pad = curses.newpad(tile_map.height, tile_map.width)

    screen_x = 0
    screen_y = 0
    
    while True:
        write_map_to_pad(tile_map, pad, screen_x, screen_y, screen_size[1], screen_size[0])
        input_char = stdscr.getch()
        log(str(input_char))
        
        if input_char == curses.KEY_UP:
            if screen_y > 0:
                screen_y -= 1
            continue

        if input_char == curses.KEY_DOWN:
            if screen_y <= tile_map.height - screen_size[0] - 1:
                screen_y += 1
            continue

        if input_char == curses.KEY_LEFT:
            if screen_x > 0:
                screen_x -= 1
            continue

        if input_char == curses.KEY_RIGHT:
            if screen_x < tile_map.width - screen_size[1] - 1:
                screen_x += 1
            continue

        if input_char == ord('Q'):
           exit()


def write_map_to_pad(tile_map, pad, start_x, start_y, width, height):
    for y in range(start_y, start_y + height):
        for x in range(start_x, start_x + width):
            current_char = ord(tile_map.get_tile_at((x, y)).display_char())
            pad.addch(y, x, current_char)
    pad.refresh(start_y, start_x,  0, 0, height - 1, width - 1)


if __name__ == '__main__':
    tile_map = cave_generator.generate_map(width=200, height=100)
    wrapper(browse_map, tile_map)

