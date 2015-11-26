from enum import Enum
import random
# generate a tiled 2D cave map

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
            self.tiles = [[Tile()] * width] * height
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


def generate_map(width, height, seed=1):
    tile_map = TileMap(width=width, height=height)
    
    # add splashes of mud and sand
    tile_map = add_layers(tile_map)

    return tile_map



def add_layer(tile_map, layer_type, layer_size):
    return random_spread(tile_map, lambda tile: Tile(composition=layer_type), layer_size)
    
def add_layers(tile_map, layer_count= None, layer_types=None):
    
    if layer_count is None:
        layer_count = random.randint(1, layer_count or MAX_LAYERS)

    if layer_types is None:
        layer_types = list(range(2,3))

    print('generating %d layers' % layer_count)

    for i in range(layer_count):
        # choose a tile type
        stratum = TileTypes(random.choice(layer_types))
        layer_size = random.randint(4, 10)
        print('new layer - type: %s, size: %d' % (stratum, layer_size))
        tile_map = add_layer(tile_map, stratum, layer_size)        
    return tile_map

def random_spread(tile_map, change_tile, tiles_to_change, coords=None, changed_coords=None):
    """
    tile_map: the tile map to be udpated
    change_tile: a function to operate on tiles having the change applied
    tiles_to_change: number of tiles to operate on
    coords: current position
    """
    if tiles_to_change == 0:
        return tile_map

    if coords is None:
        # choose a starting point
        coords = (random.randrange(0, tile_map.width), random.randrange(0, tile_map.height))
        changed_coords = []
    else:
        # get a random bordering point
        borders = border_coords(tile_map, changed_coords)
        if len(borders) == 0:

            raise Exception('No border tiles found. Number of changed tiles : %d, total tiles: %d' 
                % (len(changed_coords), tile_map.width * tile_map.height))
        coords = borders[random.randrange(0, len(borders))]
    
    new_tiles = tile_map.alter_tile(coords[0], coords[1], change_tile)

    return random_spread(
        new_tiles,
        change_tile,
        tiles_to_change - 1,
        coords,
        changed_coords + [coords])


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


# get coordinates for an extension of set of tiles
def random_growth(tile_map, active_coords):
    #get the set of tiles 
    borderCoords = border_coords(tile_map, selected_tiles)

    return borderCoords(random.randrange(0, len(borderCoords)))

def dump_map(tileset):
    for row in tileset.tiles:
        agg_tiles = ''
        for tile in row:
            agg_tiles += tile.display_char()
        print(agg_tiles)


if __name__ == '__main__':
    tile_map = generate_map(width=10, height=10)
    dump_map(tile_map)

