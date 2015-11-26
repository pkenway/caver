import cave_generator


def test_make_cave():
	cave = cave_generator.generate_map(10,7)

	assert len(cave.tiles) == 7
	assert len(cave.tiles[0]) == 10

def test_layer_generation():
    for _ in range(0, 1000):
        tile_map = cave_generator.TileMap(width=10, height=10)
        tile_map = cave_generator.add_layer(tile_map, cave_generator.TileTypes.sand, 5)
        assert len([tile for (x, y, tile) in tile_map.enumerate() if tile.composition == cave_generator.TileTypes.sand]) == 5

        tile_map = cave_generator.add_layer(tile_map, cave_generator.TileTypes.mud, 5)
        assert len([tile for (x, y, tile) in tile_map.enumerate() if tile.composition == cave_generator.TileTypes.mud]) == 5
        assert len([tile for (x, y, tile) in tile_map.enumerate() if tile.composition == cave_generator.TileTypes.sand]) <= 5

    
