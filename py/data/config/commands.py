
# array of bindings groupings for use in different modes

COMMAND_LIST = [

    {
        'modes' : ['browse'],
        'bindings':  {
            260: {'action': 'NAVIGATE', 'data': (-1, 0)},
            'h': {'action': 'NAVIGATE', 'data': (-1, 0)},
            261: {'action': 'NAVIGATE', 'data': (1, 0)},
            'l': {'action': 'NAVIGATE', 'data': (1, 0)},
            259: {'action': 'NAVIGATE', 'data' : (0, -1)},
            'K': {'action': 'NAVIGATE', 'data' : (0, -1)},
            258: {'action': 'NAVIGATE', 'data': (0, 1)},
            'j': {'action': 'NAVIGATE', 'data': (0, 1)},
            348: {'action': 'NAVIGATE', 'data': (-1, -1)},
            349: {'action': 'NAVIGATE', 'data': (1, -1)},
            'u': {'action': 'NAVIGATE', 'data': (1, -1)},
            352: {'action': 'NAVIGATE', 'data' : (1, 1)},
            'm': {'action': 'NAVIGATE', 'data' : (1, 1)},
            351: {'action': 'NAVIGATE', 'data' : (-1 ,1)},
            'n': {'action': 'NAVIGATE', 'data' : (-1 ,1)},
        }
        
    },
    {
        'modes' : ['main_menu'],
        'bindings' : {
            'Q': {'action':'EXIT_PROGRAM'}
        }
    
    }
]
