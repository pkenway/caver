from enum import Enum

##################
#
# TERRAIN TYPES
#
##################

class LayerTypes(Enum):
    #types of filled-in tiles
    Rock = 1
    Sand = 2
    Mud = 3


class FloorTypes(Enum):
    Stone = 1
    Sand = 2
    Mud = 3
    Water = 4

class WaterTypes(Enum):
    North = 1
    South = 2
    East = 3
    West = 4
    Still = 5


class Dir(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
