import pickle
from . import terrain

class TileMap():

    def __init__(self, tiles=None, width=None, height=None, default_terrain=None, logger=None):
        if tiles is not None:
            self.tiles = tiles
            self.width = len(tiles[0])
            self.height = len(tiles)
        elif width is not None and height is not None:
            self.tiles = []
            for _ in range(0, height):
                self.tiles.append([Tile(default_terrain)] * width)
            self.width = width
            self.height = height
        else:
            raise Error('Tile map must have dimensions or an array of tiles')
        self.size = (self.width, self.height)

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

    def valid_coords(self, coords):
        return ( 0 <= coords[0] < self.width) and (0 <= coords[1] < self.height)

    def get_tile_at(self, coords):    
        if not self.valid_coords(coords):
            exc_args = coords + (self.width, self.height)
            raise ValueError('coordinates (%d, %d) out of bounds. Map size: (%d, %d)' % exc_args)

        return self.tiles[coords[1]][coords[0]]

    def set_tile_at(self, coords, tile):
        self.tiles[coords[1]][coords[0]] = tile

    def save(self, file_obj):
        if not isinstance(file_obj, File):
            raise ValueError('Invalid file parameter')
        p = pickle.Pickler(file_obj)
        p.dump(self)

    @staticmethod
    def load(file_obj):
        if not isinstance(file_obj, File):
            raise ValueError('Invalid file parameter')

        p = pickle.Pickler(file_obj)
        return p.load()


class Tile():
    composition = None
    objects = []

    def __init__(self, composition=None):
        self.composition = composition

    def display_char(self):
        if self.composition == terrain.LayerTypes.Rock:
            return '#'
        if self.composition == terrain.LayerTypes.Sand:
            return '*'
        if self.composition == terrain.LayerTypes.Mud:
            return '.'
        return ' '
