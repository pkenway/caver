import random
import math
from caverlib.world import terrain, entities
from caverlib.mapgen import tools
from caverlib.world.mapping import TileMap, Tile, Point
from caverlib.logging import log

# generate a tiled 2D cave map

def generate_map(width, height, layer_count=10):
    tile_map = TileMap(width=width, height=height, default_terrain=terrain.LayerTypes.Rock)
    
    # add splashes of mud and sand
    add_rock_layers(tile_map, layer_count=layer_count)

    # add a drainage point and create rivers
    drainage_coords = Point(random.randint(0, tile_map.width - 1), random.randint(0, tile_map.height - 1))
    river_count = random.randint(3,10)

    for _ in range(0, river_count):
        add_river(tile_map, drainage_coords)

    # add random detritus
    entity_list = entities.tag_search('common', 'natural')
    if entity_list:
        for _ in range(0, 50):
            add_entity_at_random_location(tile_map, random.choice(entity_list))

    return tile_map


##########################
#
#    Soil composition functions
#
##########################
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


##########################
#
#    Water functions
#
###########################

def flow_direction(a, b):
    if a.x == b.x:
        if a.y > b.y:
            return terrain.Dir.UP
        else:
            return terrain.Dir.DOWN
    if a.x > b.x:
        return terrain.Dir.LEFT
    return terrain.Dir.RIGHT

# will modify the tileset
def add_river(tileset, drainage):
    new_river = create_river(tileset, drainage)
    for i, current_location in enumerate(new_river):
        out_direction = None
        in_direction = None
        if i < len(new_river) - 1:
            out_direction = flow_direction(current_location, new_river[i+1])
        if i > 0:
            in_direction = flow_direction(current_location, new_river[i-1])
    
        new_tile = Tile(terrain.FloorTypes.Water, direction=(in_direction, out_direction))
        tileset.set_tile_at(current_location, new_tile)


# randomly generate a river, from a point on the edge of the map to the drainage
# returns an ordered list of coordinates that the river flows through
def create_river(tileset, drainage):
    river_tiles = []
    start_location = tools.random_edge_point(tileset.width, tileset.height)
    
    scale = tileset.width * tileset.height

    # move a random distance towards the drainage point
    walk_length = random.randint(1, int(scale / 5))

    if walk_length == 0:
        raise ValueError('Could not generate a river of length 0 at location %d, %d' % start_location)

    current_location = start_location

    step_count = 0
    
    while current_location != drainage and step_count <tileset.width + tileset.height:
        # crate vector space between current point and drainage location
        vector =  drainage - current_location
        # scale down to our step
        magnitude = int(tools.distance(current_location, drainage))
        # magnitude = min(magnitude, int(distance(current_location, drainage)))


        if scale < magnitude:
            vector = Point(int(vector[0] * scale / magnitude), int(vector[1] * scale / magnitude))
        #choose a random point in the space

        rand_vector = Point(tools.rand_to(vector.x), tools.rand_to(vector.y))
        new_location = current_location  + rand_vector
        
        # draw a line to that point
        river_tiles += get_river_section(tileset, current_location, new_location)
        current_location = new_location
        step_count += 1
    return river_tiles


def get_river_section(tileset, start_location, end_location):
    if start_location == end_location:
        return []
    path = tools.create_direct_path(start_location, end_location)
    
    path = tools.distort_path(path, 2)
    return path


def random_spread(tile_map, change_tile_func, tiles_to_change):
    changed_coords = []
    border_tiles = []
    for _ in range(0, tiles_to_change):
        if border_tiles == []:
            coords = Point(random.randrange(0, tile_map.width), random.randrange(0, tile_map.height))
            border_tiles = tools.adjacent_coords(tile_map.size, coords)        
        else:
            coords = border_tiles[random.randrange(0, len(border_tiles))]
            border_tiles.remove(coords)
        tile_map.set_tile_at(coords, change_tile_func(tile_map.get_tile_at(coords)))
        changed_coords.append(coords)
        adjacent_tiles = tools.adjacent_coords(tile_map.size, coords)
        # add to the ppol of border tiles
        border_tiles += [coords for coords in adjacent_tiles if coords not in border_tiles and coords not in changed_coords]


##########################
#
#    Item generation
#
###########################


def add_entity_at_random_location(tile_map, entity):
    coords = tools.random_point(tile_map.size)
    tile_map.get_tile_at(coords).entities.append(entity())


def dump_map(tileset, outfile):
    for row in tileset.tiles:
        tile_display = ''.join([tile.display_char() for tile in row ])
        outfile.write(tile_display + '\n')

