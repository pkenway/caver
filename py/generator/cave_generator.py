import random
import math
from . import terrain
from .cave_map import TileMap, Tile

# generate a tiled 2D cave map

def generate_map(width, height, layer_count=10):
    tile_map = TileMap(width=width, height=height, default_terrain=terrain.LayerTypes.Rock)
    
    # add splashes of mud and sand
    add_rock_layers(tile_map, layer_count=layer_count)

    # add a drainage point and create rivers
    drainage_coords = (random.randint(0, tile_map.width), random.randint(0, tile_map.height))
    river_count = random.randint(3,10)

    for _ in range(0, river_count):
        add_river(tile_map, drainage_coords)


    return tile_map


def add_rock_layers(tile_map, layer_count= None, layer_types=None, layer_size_avg=None, layer_size_deviation=None):
    
    if layer_count is None:
        layer_count = random.randint(1, layer_count or MAX_LAYERS)

    if layer_types is None:

        layer_types = list(range(1,4))

    if layer_size_avg is None:
        layer_size_avg = int( (tile_map.width + tile_map.height))

    if layer_size_deviation is None:
        layer_size_deviation = int(math.sqrt(layer_size_avg))

    for i in range(layer_count):
        # choose a tile type
        layer_type = terrain.LayerTypes(random.choice(layer_types))
        layer_size = random.randint(layer_size_avg - layer_size_deviation, layer_size_avg + layer_size_deviation)
        add_rock_layer(tile_map, layer_type, layer_size)        


def add_rock_layer(tile_map, layer_type, layer_size):
    random_spread(tile_map, lambda tile: Tile(composition=layer_type), layer_size)


def add_river(tileset, drainage_coords):
    # randomly generate a river, from a point on the edge of the map to the drainage
    start_location = random_edge_point(tileset)
    scale = tileset.width * tileset.height

    # move a random distance towards the drainage point
    walk_length = random.randint(0, int(scale / 5))

    current_location = start_location

    while current_location != drainage_coords:


        vector = (
            drainage_coords[0] - current_location[0] * scale,
            drainage_coords[1] - current_location[1] * scale)

        new_location = (
            current_location[0] + random.randint(0, vector[0]) if vector[0] > 0 else 0, 
            current_location[1] + random.randint(0,vector[1]) if vector[1] > 0 else 0)
        draw_river_section(tileset, current_location, new_location)
        current_location = new_location


def draw_river_section(tileset, start_location, end_location):
    #move from point A to point B by the straightest line
    current_location = start_location
    while current_location != end_location:
        current_location = advance_towards(current_location, end_location)
        tileset.set_tile_at(current_location, Tile(terrain.WaterTypes.Still))


def random_spread(tile_map, change_tile_func, tiles_to_change):
    changed_coords = []
    border_tiles = []
    for _ in range(0, tiles_to_change):
        if border_tiles == []:
            coords = (random.randrange(0, tile_map.width), random.randrange(0, tile_map.height))
            border_tiles = adjacent_coords(tile_map, coords)        
        else:
            coords = border_tiles[random.randrange(0, len(border_tiles))]
            border_tiles.remove(coords)
        tile_map.set_tile_at(coords, change_tile_func(tile_map.get_tile_at(coords)))
        changed_coords.append(coords)
        adjacent_tiles = adjacent_coords(tile_map, coords)
        # add to the ppol of border tiles
        border_tiles += [coords for coords in adjacent_tiles if coords not in border_tiles and coords not in changed_coords]
    

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


def dump_map(tileset, outfile):
    for row in tileset.tiles:
        tile_display = ''.join([tile.display_char() for tile in row ])
        outfile.write(tile_display + '\n')

def random_edge_point(tileset):
    # choose an edge
    edge = random.randint(0, 3)

    if edge == 0:
        return (0, random.randint(0, tileset.height))
    elif edge == 1:
        return (tileset.width -1, random.randint(0, tileset.height))
    elif edge == 2:
        return (random.randint(0, tileset.width), 0)
    elif edge == 3:
        return (random.randint(0, tileset.width), tileset.height - 1)

    raise ValueError('%d is not a valid edge index' % edge)


def advance_towards(start_location, end_location, skip=1):
    delta = (end_location[0] - start_location[0], end_location[1] - start_location[1])
    if delta[0] > delta[1]:
        if delta[0] > 0:
            return (start_location[0] -skip, start_location[1])
        else:
            return (start_location[0] +skip, start_location[1])
    else:
        if delta[1] > 0:
            return (start_location[0], start_location[1] -skip)
        else:
            return (start_location[0], start_location[1] +skip)












