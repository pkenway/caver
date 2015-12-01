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
        if tiles:
            self.tiles = tiles
            self.width = len(tiles[0])
            self.height = len(tiles)
        elif width and height:
            self.width = width
            self.height = height
            self.create_tiles(default_terrain)
        else:
            raise Error('Tile map must have dimensions or an array of tiles')
        self.logger = logger

    def create_tiles(self, default_terrain):
        self.tiles = []
        for _ in range(0, self.height):
            new_row = []
            for __ in range(0, self.width):
                new_row.append(Tile(default_terrain))
            self.tiles.append(new_row)

    @property
    def size(self):
        return Point(self.width, self.height)

    def iterate(self):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                yield Point(x, y), tile

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

    def __init__(self, composition=None, **kwargs):
        self.composition = composition
        self.props = kwargs
        self.entities = []


