import random
import math
from ..world.mapping import Point

def is_adjacent(coords, coordset):
    if coords in coordset:
        return False
    for c in coordset:
        if c.x == coords.x and abs(c.y - coords.y) == 1:
            return True
        if abs(c.x - coords.x) == 1 and c.y == coords.y:
            return True
    return False


# def border_coords(tile_map, selected_tiles):
#     return [point for (point, tile) in tile_map.enumerate() if is_adjacent(point, selected_tiles)]


def adjacent_coords(map_size, coords):
    adjacents = []
    if coords.x > 0:
        adjacents.append(Point(coords.x -1, coords.y))
    if coords.x < map_size.x - 1:
        adjacents.append(Point(coords.x +1, coords.y))
    if coords.y > 0:
        adjacents.append(Point(coords.x, coords.y - 1))
    if coords.y < map_size.y - 1:
        adjacents.append(Point(coords.x, coords.y + 1))
    return adjacents


def create_direct_path(a, b):
    step_count = 0
    tiles = []
    while a != b:
        a = advance_towards(a, b)    
        tiles.append(a)
        step_count += 1
    return tiles


def advance_towards(a, b, step=1):
    delta = b - a
    if abs(delta.x) > abs(delta.y):
        if delta.x > 0:
            return Point(a.x + step, a.y)
        else:
            return Point(a.x - step, a.y)
    else:
        if delta.y > 0:
            return Point(a.x, a.y + step)
        else:
            return Point(a.x, a.y - step)


def distort_path(path_coords, distoration_level=1):
    path_start = path_coords[0]
    path_end = path_coords[-1]

    path_vector = path_end - path_start

    waypoints = []
    for _ in range(0, distoration_level):
        # add in a waypoint
        rand_vector = Point(rand_to(path_vector.x), rand_to(path_vector.y))
        waypoints.append( path_start + rand_vector)
    current_point = path_start
    new_path = [current_point]
    for w in waypoints:
        new_path += create_direct_path(current_point, w)
        current_point = w

    new_path += create_direct_path(new_path[-1], path_end)
    return new_path


# return a random number between 0 and the integer
def rand_to(num) :
    if num > 0:
        return random.randint(0, num)
    elif num < 0:
        return random.randint(num, 0)
    return 0

def random_point(size):
    return Point(
        rand_to(size.x - 1),
        rand_to(size.y -  1))

def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) **2)


def random_edge_point(width, height):
    # choose an edge
    edge = random.randint(0, 3)

    if edge == 0:
        return Point(0, random.randint(0, height - 1))
    elif edge == 1:
        return Point(width -1, random.randint(0, height -1))
    elif edge == 2:
        return Point(random.randint(0, width - 1), 0)
    elif edge == 3:
        return Point(random.randint(0, width - 1), height - 1)

    raise ValueError('%d is not a valid edge index' % edge)
