
from caverlib.world import terrain, entities, mapping
from caverlib.mapgen import tools, cave_generator
import curses
import display
import message_bus
import commands

# mock message receiver
class R():
    def __init__(self, key, expected_data):
        self.key = key
        self.expected_data = expected_data
        self.got_msg = False

    def receive(self, data):
        assert data == self.expected_data
        self.got_msg = True

    def reset(self):
        self.got_msg = False

    def register(self, msg_bus):
        msg_bus.register(self.key, self.receive)

    def unregister(self, msg_bus):
        msg_bus.unregister(self.key, self.receive)


def get_receiver(msg_bus, key, expected_data):
    r = R(key, expected_data)
    r.register(msg_bus)
    return r

def test_make_cave():
	cave = cave_generator.generate_map(10,7)

	assert len(cave.tiles) == 7
	assert len(cave.tiles[0]) == 10


def test_layer_generation():
    for _ in range(0, 1000):
        tile_map = mapping.TileMap(width=10, height=10)
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
        tile_map = mapping.TileMap(width=10, height=10, logger=PrintLogger())

        cave_generator.add_river(tile_map, mapping.Point(5,5))
        assert len([tile for point, tile in tile_map.iterate() if tile.composition == terrain.FloorTypes.Water])

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
    assert tools.advance_towards(mapping.Point(0,0), mapping.Point(1,0)) == mapping.Point(1,0)
    assert tools.advance_towards(mapping.Point(10,0), mapping.Point(0,0)) == mapping.Point(9, 0)
    assert tools.advance_towards(mapping.Point(0,0), mapping.Point(0,1)) == mapping.Point(0,1)

    assert tools.advance_towards(mapping.Point(10,10), mapping.Point(10, 0)) == mapping.Point(10, 9)


def test_message_bus():
    msg_bus = message_bus.MessageBus()
    mtype = message_bus.MType.NAVIGATE

    payload = mapping.Point(0,1)
    r= get_receiver(msg_bus, mtype, payload)
    r2 = get_receiver(msg_bus, mtype, payload)

    msg_bus.send(mtype, payload)
    assert r.got_msg and r2.got_msg
    
    assert len(msg_bus.listeners[mtype]) == 2

    r.reset()
    r2.reset()

    # unregister a listener
    r2.unregister(msg_bus)
    msg_bus.send(mtype, payload)
    assert r.got_msg and not r2.got_msg

    r.reset()
    r2.reset()

    #switch listeners
    r2.register(msg_bus)
    r.unregister(msg_bus)
    msg_bus.send(mtype, payload)
    assert not r.got_msg and r2.got_msg

    r.reset()
    r2.reset()

    r2.unregister(msg_bus)

    # no registered listeners
    msg_bus.send(mtype, payload)
    assert r.got_msg == r2.got_msg == False

    assert len(msg_bus.listeners[mtype]) == 0


def test_river_display():

    assert display.get_pipe_display((terrain.Dir.LEFT, terrain.Dir.UP)) == '╝'


def test_entity_tag_esarch():
    ent_list = entities.tag_search('common', 'natural')
    assert len(ent_list) > 0

    created_entity = ent_list[0]()
    assert isinstance(created_entity, entities.Entity)

def test_add_entities():
    tile_map = mapping.TileMap(width=10, height=10)
    # stick = entities.stick()
    cave_generator.add_entity_at_random_location(tile_map, entities.stick)

    occupied_tile = None
    coords = None
    for point, tile in tile_map.iterate():
        if tile.entities:
            occupied_tile = tile
            coords = point
            break

    for point, tile in tile_map.iterate():
        if point == coords:
            continue
        assert tile.entities == []


    assert occupied_tile

    assert entities.visible_entity(occupied_tile.entities).name == 'stick'

    rock = entities.rock()
    occupied_tile.entities.insert(0, rock)
    assert entities.visible_entity(occupied_tile.entities).name == 'rock'


def test_keyboard_commands():
    msg_bus = message_bus.MessageBus()
    cmd_list =[{
        "modes" : ["browse"],
        "bindings": {
            260: {'action': 'NAVIGATE', 'data': (-1, 0)},
        }
    }]
    cmd = commands.CommandInterpreter(msg_bus, cmd_list)
    cmd.set_mode('browse')

    r = get_receiver(msg_bus, 'NAVIGATE', mapping.Point(-1, 0))

    msg_bus.send(message_bus.MType.KEY_PRESS, 260)
    assert r.got_msg


if __name__ == '__main__':
    test_river_generation()

