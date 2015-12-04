from message_bus import MType

class ActionListener():

    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.message_bus.register(MType.NAVIGATE, self.on_navigate)

        def on_navigate(self, move_vector):
            



def check_commands(pad, input_buffer, tile_map):
    if len(input_buffer) == 0:
        return

    input_char = input_buffer[0]
    command = commands.get_first_command(commands.SYSTEM_COMMANDS, input_char)
    if not command:
        return

    if command.name == 'exit_program':
        exit_program()
        return True

    if command.name == 'print_map':
        log('dumping map to file')
        with open('map_dump.log', 'w') as f:
            cave_generator.dump_map(tile_map, f)
        return True
        
    return False


# watch the input stream for map navigation commands
def check_navigate(current_coords, input_buffer, screen_size, map_size):
    
    if len(input_buffer) == 0:
        return current_coords

    input_char = input_buffer[0]

    actions = [a for a in commands.NAVIGATION_MOVES if input_char in a.keys]

    if not actions:
        return current_coords
    
    move_vector = sum([a.target for a in actions])

    rate = SCREEN_ZOOM_FACTOR if key_held_down(input_buffer, input_char) else 1

    # apply movement
    new_coords = current_coords + (move_vector * rate)

    # constraints
    new_coords = Point(*[ max(p, 0) for p in new_coords])
    new_coords = Point(*[ min(p, map_size[i] - screen_size[i] - 1) for i, p in enumerate(new_coords)])

    return new_coords
