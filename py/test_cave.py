from generator import terrain, cave_generator
from screen import check_navigate
import curses
def test_make_cave():
	cave = cave_generator.generate_map(10,7)

	assert len(cave.tiles) == 7
	assert len(cave.tiles[0]) == 10


def test_layer_generation():
    for _ in range(0, 1000):
        tile_map = cave_generator.TileMap(width=10, height=10)
        cave_generator.add_rock_layer(tile_map, terrain.LayerTypes.Sand, 5)
        assert len([tile for (x, y, tile) in tile_map.enumerate() if tile.composition == terrain.LayerTypes.Sand]) == 5

        cave_generator.add_rock_layer(tile_map, terrain.LayerTypes.Mud, 5)
        assert len([tile for (x, y, tile) in tile_map.enumerate() if tile.composition == terrain.LayerTypes.Mud]) == 5
        assert len([tile for (x, y, tile) in tile_map.enumerate() if tile.composition == terrain.LayerTypes.Sand]) <= 5

    
def test_screen_navigate():

    initial_coords = (0,0)
    screen = (50, 50)
    map_size = (100, 100)
    print(initial_coords)

    new_coords = check_navigate(initial_coords, [curses.KEY_UP], screen, map_size)
    print(new_coords)
    assert new_coords == initial_coords

    new_coords = check_navigate(initial_coords, [curses.KEY_DOWN], screen, map_size)
    assert new_coords == (0, 1)

    new_coords = check_navigate(initial_coords, [curses.KEY_LEFT], screen, map_size)
    assert new_coords == initial_coords

    new_coords = check_navigate(initial_coords, [curses.KEY_RIGHT], screen, map_size)
    assert new_coords == (1, 0)


if __name__ == '__main__':
    test_screen_navigate()
