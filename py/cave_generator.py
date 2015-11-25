from enum import Enum
# generate a tiled 2D cave map


class TileTypes(Enum):
	#types of filled-in tiles
	rock = 1
	sand = 2
	mud = 3

	stone_floor = 4
	sand_floor = 5
	mud_floor = 6
	water = 7



class Tile():
	composition = TileTypes.rock
	objects = []


def generate_map(width, height, seed=1):
	tile_map = [[Tile()] * height] * width


	return tile_map


