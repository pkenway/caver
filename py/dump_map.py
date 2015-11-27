from environment.cave_generator import generate_map, dump_map

tile_map = generate_map(width=100, height=100, layer_count=10)
dump_map(tile_map)
