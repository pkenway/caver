import curses
from curses import wrapper
import cave_generator
from caverlib.logging import log
from caverlib.world.mapping import Point
from caverlib.world.entities import entities
from enum import Enum
import display
import commands

#constants
MAX_INPUT_BUFFER = 1024

#interactively browse a generated map
def browse_map(stdscr, tile_map):
    display.init_color_pairs()
    screen_size = tuple(reversed(stdscr.getmaxyx()))
    log('Browsing map. screen dimensions: %d x %d' % screen_size)
    
    pad = curses.newpad(tile_map.height, tile_map.width)

    screen_coords = Point(0, 0)
    input_buffer = []
    write_map_to_pad(tile_map, pad, *(tuple(screen_coords) + screen_size))
    while True:
        write_map_to_pad(tile_map, pad, *(tuple(screen_coords) + screen_size))
        
        input_buffer.insert(0,stdscr.getch())

        if len(input_buffer) > MAX_INPUT_BUFFER:
            del input_buffer[-1]

        screen_coords = check_navigate(screen_coords, input_buffer, screen_size, tile_map.size)
        # log(' - %d, %d -' % screen_coords)
        if check_commands(pad, input_buffer, tile_map):
            continue


def exit_program():
    exit()


SCREEN_ZOOM_DELAY = 5
SCREEN_ZOOM_FACTOR = 10


def check_commands(pad, input_buffer, tile_map):
    if len(input_buffer) == 0:
        return

    input_char = input_buffer[0]
    command = commands.get_first_command(commands.SYSTEM_COMMANDS, input_char)
    if not command:
        return

    if command.name == 'exit_program':
        exit_program()
        return True

    if command.name == 'print_map':
        log('dumping map to file')
        with open('map_dump.log', 'w') as f:
            cave_generator.dump_map(tile_map, f)
        return True
        
    return False


# watch the input stream for map navigation commands
def check_navigate(current_coords, input_buffer, screen_size, map_size):
    
    if len(input_buffer) == 0:
        return current_coords

    input_char = input_buffer[0]

    actions = [a for a in commands.NAVIGATION_MOVES if input_char in a.keys]

    if not actions:
        return current_coords
    
    move_vector = sum([a.target for a in actions])

    rate = SCREEN_ZOOM_FACTOR if key_held_down(input_buffer, input_char) else 1

    # apply movement
    new_coords = current_coords + (move_vector * rate)

    # constraints
    new_coords = Point(*[ max(p, 0) for p in new_coords])
    new_coords = Point(*[ min(p, map_size[i] - screen_size[i] - 1) for i, p in enumerate(new_coords)])

    return new_coords


def key_held_down(input_buffer, input_char):
    if len(input_buffer) < SCREEN_ZOOM_DELAY:
        return False

    for cchar in input_buffer[:SCREEN_ZOOM_DELAY]:
        if cchar != input_char:
            return False
    return True
 

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




