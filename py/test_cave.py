import cave_generator


def test_make_cave():
	cave = cave_generator.generate_map(10,7)

	assert len(cave) == 10
	assert len(cave[0]) == 7