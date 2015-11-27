import random
import math
from . import terrain
from .cave_map import TileMap, Tile

# generate a tiled 2D cave map

def generate_map(width, height, layer_count=10):
    tile_map = TileMap(width=width, height=height, default_terrain=terrain.LayerTypes.Rock)
    
    # add splashes of mud and sand
    add_rock_layers(tile_map, layer_count=layer_count)

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


def dump_map(tileset):
    for row in tileset.tiles:
        agg_tiles = ''
        for tile in row:
            agg_tiles += tile.display_char()
        print(agg_tiles)

# generate a path through the map. we can use this to make
# def random_path(tile_map, change_tile_func):



