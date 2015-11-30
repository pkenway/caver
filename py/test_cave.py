
from caverlib.world import terrain, entities
from caverlib.world.mapping import Point
from caverlib.mapgen import tools
from screen import check_navigate
import cave_generator
import curses
import display

def test_make_cave():
	cave = cave_generator.generate_map(10,7)

	assert len(cave.tiles) == 7
	assert len(cave.tiles[0]) == 10


def test_layer_generation():
    for _ in range(0, 1000):
        tile_map = cave_generator.TileMap(width=10, height=10)
        cave_generator.add_rock_layer(tile_map, terrain.LayerTypes.Sand, 5)
        assert len([tile for (point, tile) in tile_map.iterate() if tile.composition == terrain.LayerTypes.Sand]) == 5

        cave_generator.add_rock_layer(tile_map, terrain.LayerTypes.Mud, 5)
        assert len([tile for (point, tile) in tile_map.iterate() if tile.composition == terrain.LayerTypes.Mud]) == 5
        assert len([tile for (point, tile) in tile_map.iterate() if tile.composition == terrain.LayerTypes.Sand]) <= 5


class PrintLogger():

    def write(self, text):
        print(text)

def test_river_generation():

    for _ in range(0, 1000):
        tile_map = cave_generator.TileMap(width=10, height=10, logger=PrintLogger())

        cave_generator.add_river(tile_map, Point(5,5))
        assert len([tile for point, tile in tile_map.iterate() if tile.composition == terrain.FloorTypes.Water])
    
def test_screen_navigate():

    initial_coords = Point(0,0)
    screen = (50, 50)
    map_size = (100, 100)

    new_coords = check_navigate(initial_coords, [curses.KEY_UP], screen, map_size)
    assert new_coords == initial_coords

    new_coords = check_navigate(initial_coords, [curses.KEY_DOWN], screen, map_size)
    assert new_coords == Point(0, 1)

    new_coords = check_navigate(initial_coords, [curses.KEY_LEFT], screen, map_size)
    assert new_coords == initial_coords

    new_coords = check_navigate(initial_coords, [curses.KEY_RIGHT], screen, map_size)
    assert new_coords == Point(1, 0)

def test_random_edge():
    for _ in range(0, 100):
        edge_point = tools.random_edge_point(10, 10)
        is_edge = False

        if edge_point[0] == 0 or edge_point[0] == 9:
            is_edge = True

        if edge_point[1] ==0 or edge_point[1] == 9:
            is_edge = True

        assert is_edge

def test_advance():
    assert tools.advance_towards(Point(0,0), Point(1,0)) == Point(1,0)
    assert tools.advance_towards(Point(10,0), Point(0,0)) == Point(9, 0)
    assert tools.advance_towards(Point(0,0), Point(0,1)) == Point(0,1)

    assert tools.advance_towards(Point(10,10), Point(10, 0)) == Point(10, 9)



    # ((terrain.Dir.UP, terrain.Dir.DOWN), '║'),
    # ((terrain.Dir.UP, terrain.Dir.LEFT), '╝'),
    # ((terrain.Dir.UP, terrain.Dir.RIGHT), '╚'),
    # ((terrain.Dir.LEFT, terrain.Dir.RIGHT), '═'),
    # ((terrain.Dir.LEFT, terrain.Dir.DOWN), '╗'),
    # ((terrain.Dir.DOWN, terrain.Dir.RIGHT), '╔'),

def test_river_display():

    assert display.get_pipe_display((terrain.Dir.LEFT, terrain.Dir.UP)) == '╝'


# def test_add_entities():


if __name__ == '__main__':
    test_river_generation()

