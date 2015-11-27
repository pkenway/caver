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
    Stone = 4
    Sand = 5
    Mud = 6
    Water = 7

