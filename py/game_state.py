from caverlib.mapgen import cave_generator
from caverlib.world.mapping import Point
from message_bus import MType
class GameState():

    time = 0

    def __init__(self, message_bus):
        self.message_bus = message_bus
        message_bus.register(MType.TICK, self.tick)
        message_bus.register(MType.NAVIGATE, self.navigate)

    def tick(self, data):
        self.time += 1

    def navigate(self, vector):
        new_coords = self.view_coords + vector
        if not self.tile_map.valid_coords(new_coords):
            return
        self.view_coords = new_coords

        self.message_bus.send(MType.SET_VIEW_COORDS, new_coords)

    def new_game(self):
        self.tile_map = cave_generator.generate_map(width=100, height=100, layer_count=10)
        self.view_coords = Point(0, 0)
        self.message_bus.send(MType.SET_MAP, self.tile_map)
        self.message_bus.send(MType.SET_VIEW_COORDS, self.view_coords)

