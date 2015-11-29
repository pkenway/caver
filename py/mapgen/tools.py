import random
import math

def is_adjacent(coords, coordset):
    if coords in coordset:
        return False
    for c in coordset:
        if c[0] == coords[0] and abs(c[1] - coords[1]) == 1:
            return True
        if abs(c[0] - coords[0]) == 1 and c[1] == coords[1]:
            return True
    return False


def border_coords(tile_map, selected_tiles):
    return [(x, y) for (x, y, tile) in tile_map.enumerate() if is_adjacent((x,y), selected_tiles)]


def adjacent_coords(tile_map, coords):
    adjacents = []
    if coords[0] > 0:
        adjacents.append((coords[0] -1, coords[1]))
    if coords[0] < tile_map.width - 1:
        adjacents.append((coords[0] +1, coords[1]))
    if coords[1] > 0:
        adjacents.append((coords[0], coords[1] - 1))
    if coords[1] < tile_map.height - 1:
        adjacents.append((coords[0], coords[1] + 1))
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
    delta = (b[0] - a[0], b[1] - a[1])
    if abs(delta[0]) > abs(delta[1]):
        if delta[0] > 0:
            return (a[0] + step, a[1])
        else:
            return (a[0] - step, a[1])
    else:
        if delta[1] > 0:
            return (a[0], a[1] + step)
        else:
            return (a[0], a[1] - step)


def vector(a, b):
    return (b[0] - a[0], b[1] - a[1])

def distort_path(path_coords, distoration_level=1):
    path_start = path_coords[0]
    path_end = path_coords[-1]
    path_vector = vector(path_start, path_end)

    waypoints = []
    for _ in range(0, distoration_level):
        # add in a waypoint

        waypoints.append((
            path_start[0] + rand_to(path_vector[0]),
            path_start[1] + rand_to(path_vector[1])
            ))
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


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) **2)


def random_edge_point(width, height):
    # choose an edge
    edge = random.randint(0, 3)

    if edge == 0:
        return (0, random.randint(0, height - 1))
    elif edge == 1:
        return (width -1, random.randint(0, height -1))
    elif edge == 2:
        return (random.randint(0, width - 1), 0)
    elif edge == 3:
        return (random.randint(0, width - 1), height - 1)

    raise ValueError('%d is not a valid edge index' % edge)
