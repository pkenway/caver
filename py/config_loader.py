import os
import simplejson as json


def get_config(config_directory, config_name):
    if not os.path.exists(config_directory):
        raise Exception('config directory %s not found' % config_directory)

    data = None
    with open('%s/%s.json' % (config_directory, config_name)) as cfile:
        data = json.load(cfile)
    return data
