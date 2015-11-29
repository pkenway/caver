################
#  
# Taxonomy of entities in the world
# including active creaturs and items
# each entity is created with a set of properties
# that define it's behaviors
#
##################

from properties import props

class Entity():

    def __init__(name, props={}, **kwargs):
        self.props = kwargs

    def prop(propname, value=None):
        if value:
            self.props[propname] = value
        return self.props.get(propname, None)


def stick(**kwargs):
    return Entity('stick', props= {
        props.HITPOINTS : 1,
        props.HARDNESS: 4,
        props.CARRYABLE: True,
        props.THROWABLE: True
        })

def rock(**kwargs):
    return Entity('rock', props={
        props.HITPOINTS: 10,
        props.HARDNESS:  10,
        props.CARRYABLE: True
        props.THROWABLE: True
        })
