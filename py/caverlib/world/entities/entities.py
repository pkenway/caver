################
#  
# Taxonomy of entities in the world
# including active creaturs and items
# each entity is created with a set of properties
# that define it's behaviors
#
##################

from .properties import props
from collections import defaultdict
from itertools import chain
class Entity():

    def __init__(self, name, defaultprops={}, props={}, **kwargs):
        self.defaultprops = defaultprops
        self.props = props.update(kwargs)

    def prop(propname, value=None):
        if value:
            self.props[propname] = value
            return value
        return self.props.get(propname, self.defaultprops.get(propname, None))

_prop_tags = defaultdict(list)


def tags(*args):
    def tags_decorator(func):
        for tag in args:
            _prop_tags[tag].append(func)
        return func

    return tags_decorator

def tag_search(*args):
    return list(chain([ _prop_tags[tag] for tag in args]))


@tags('common', 'natural')
def stick(**kwargs):
    return Entity('stick', props= {
        props.WEIGHT: 2,
        props.HITPOINTS : 1,
        props.HARDNESS: 4,
        props.CARRYABLE: True,
        props.THROWABLE: True,
        props.FLOATS: True
        })

@tags('common', 'natural')
def rock(**kwargs):
    return Entity('rock', props={
        props.WEIGHT: 3,
        props.HITPOINTS: 10,
        props.HARDNESS:  10,
        props.CARRYABLE: True,
        props.THROWABLE: True,
        })





# topmost entity has the lowest index
def visible_entity(entity_list, truesight=False):
    if not entity_list:
        return None

    if truesight:
        return entity_list[0]

    for entity in entity_list:
        # check invisibility
        if entity.prop(props.INVISIBLE):
            continue
        return entity
    return None
