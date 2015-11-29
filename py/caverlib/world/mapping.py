import pickle
from . import terrain
from collections import namedtuple

class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = ()

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other, self.y + other)

    def __radd__(self, other):
        return Point(self.x + other, self.y + other)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        return Point(self.x * other, self.y * other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return Point(self.x - other, self.y - other)

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
        self.logger = logger


    def enumerate(self):
        # return [(x, tup[0], tup[1]) for x, tup in enumerate([(y, row) for y, row in enumerate(self.tiles)])]
        rv = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rv.append((Point(x, y), tile))
        return rv

    def list_tiles(self):
        return [ tup[0] for tup in self.enumerate() ]

    def valid_coords(self, coords):
        return ( 0 <= coords.x < self.width) and (0 <= coords.y < self.height)

    def get_tile_at(self, coords):    
        if not self.valid_coords(coords):
            exc_args = tuple(coords) + (self.width, self.height)
            raise ValueError('coordinates (%d, %d) out of bounds. Map size: (%d, %d)' % exc_args)

        return self.tiles[coords.y][coords.x]

    def set_tile_at(self, coords, tile):
        self.tiles[coords.y][coords.x] = tile

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

    def __init__(self, composition=None, **kwargs):
        self.composition = composition
        self.props = kwargs

    def display_char(self):
        if self.composition == terrain.LayerTypes.Rock:
            return '#'
        if self.composition == terrain.LayerTypes.Sand:
            return '*'
        if self.composition == terrain.LayerTypes.Mud:
            return '.'
        return ' '
