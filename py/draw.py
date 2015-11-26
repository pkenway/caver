import curses
from curses import wrapper
import cave_generator

if __name__ == '__main__':
    wrapper.wrapper(draw_random_map)

def draw_random_map(stdscr):
    begin_x = 0; begin_y = 0
    height = 10; width = 10
    win = curses.newwin(height, width, begin_y, begin_x)

    



