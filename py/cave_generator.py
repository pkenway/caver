from enum import Enum
import random
import math
# generate a tiled 2D cave map
# goal is for the map to be immutable
# update functions will return a new copy of the map

# constants
MAX_LAYERS = 3

class TileTypes(Enum):
    #types of filled-in tiles
    rock = 1
    sand = 2
    mud = 3

    stone_floor = 4
    sand_floor = 5
    mud_floor = 6
    water = 7

class TileMap():

    def __init__(self, tiles=None, width=None, height=None):
        if tiles is not None:
            self.tiles = tiles
            self.width = len(tiles[0])
            self.height = len(tiles)
        elif width is not None and height is not None:
            self.tiles = []
            for _ in range(0, height):
                self.tiles.append([Tile()] * width)
            print(len(self.tiles))
            print(len(self.tiles[0]))
            self.width = width
            self.height = height
        else:
            raise Error('Tile map must have dimensions or an array of tiles')

    def alter_tile(self, x, y, change_func):
        return TileMap(tiles=[
            [change_func(tile) if tilex == x and tiley == y else tile for tilex, tile in enumerate(row)]
        for tiley, row in enumerate(self.tiles)])

    def enumerate(self):
        # return [(x, tup[0], tup[1]) for x, tup in enumerate([(y, row) for y, row in enumerate(self.tiles)])]
        rv = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rv.append((x, y, tile))

        return rv
        
    def list_tiles(self):
        return [ tup[0] for tup in self.enumerate() ]

    def get_tile_at(self, coords):    
        return self.tiles[coords[1]][coords[0]]
    def set_tile_at(self, coords, tile):
        self.tiles[coords[1]][coords[0]] = tile

class Tile():
    composition = None
    objects = []

    def __init__(self, composition=TileTypes.rock):
        self.composition = composition

    def display_char(self):
        if self.composition == TileTypes.rock:
            return '#'
        if self.composition == TileTypes.sand:
            return '*'
        if self.composition == TileTypes.mud:
            return '.'
        return ' '


def generate_map(width, height, layer_count=3):
    tile_map = TileMap(width=width, height=height)
    
    # add splashes of mud and sand
    add_layers(tile_map, layer_count=layer_count)

    return tile_map


def add_layers(tile_map, layer_count= None, layer_types=None, layer_size_avg=None, layer_size_deviation=None):
    
    if layer_count is None:
        layer_count = random.randint(1, layer_count or MAX_LAYERS)

    if layer_types is None:
        layer_types = list(range(2,3))

    if layer_size_avg is None:
        layer_size_avg = int( (tile_map.width + tile_map.height) / 2)

    if layer_size_deviation is None:
        layer_size_deviation = int(math.sqrt(layer_size_avg))

    print('generating %d layers' % layer_count)

    for i in range(layer_count):
        # choose a tile type
        stratum = TileTypes(random.choice(layer_types))
        layer_size = random.randint(layer_size_avg - layer_size_deviation, layer_size_avg + layer_size_deviation)

        print('new layer - type: %s, size: %d' % (stratum, layer_size))
        add_layer(tile_map, stratum, layer_size)        


def add_layer(tile_map, layer_type, layer_size):
    random_spread(tile_map, lambda tile: Tile(composition=layer_type), layer_size)


def random_spread(tile_map, change_tile_func, tiles_to_change):
    changed_coords = []
    border_tiles = []
    for _ in range(0, tiles_to_change):
        if border_tiles == []:
            coords = (random.randrange(0, tile_map.width), random.randrange(0, tile_map.height))
            border_tiles = adjacent_coords(tile_map, coords)
            print(coords)
        else:
            coords = border_tiles[random.randrange(0, len(border_tiles))]
            border_tiles.remove(coords)
        tile_map.set_tile_at(coords, change_tile_func(tile_map.get_tile_at(coords)))
        changed_coords.append(coords)
        adjacent_tiles = adjacent_coords(tile_map, coords)
        # add to the ppol of border tiles
        border_tiles += [coords for coords in adjacent_tiles if coords not in border_tiles and coords not in changed_coords]
    print(changed_coords)


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


if __name__ == '__main__':
    tile_map = generate_map(width=100, height=100, layer_count=10)
    dump_map(tile_map)

