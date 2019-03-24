""" Entity:

- creation

"""


class Entity:
    """ A generic object to represent layers, enemies, items, etc.

    """

    def __init__(self, x_pos, y_pos, char, color, name, blocks=False):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, d_x, d_y):
        """ Move the entity by a given amount

        """
        self.x_pos += d_x
        self.y_pos += d_y


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """ Return entity at target destination if the entity blocks

    """

    for entity in entities:
        entity_at_position = (
            entity.x_pos == destination_x and entity.y_pos == destination_y
        )
        if entity.blocks and entity_at_position:
            return entity

    return None
