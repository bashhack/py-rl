""" Entity:

- creation
- movement
- pathfinding
- helpers

"""

from math import sqrt

import tcod

from render_functions import RenderOrder


class Entity:
    """ A generic object to represent layers, enemies, items, etc.

    """

    def __init__(self,
                 x_pos,
                 y_pos,
                 char,
                 color,
                 name,
                 blocks=False,
                 render_order=RenderOrder.CORPSE,
                 fighter=None,
                 ai=None,
                 item=None,
                 inventory=None,
                 stairs=None,
                 level=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

    def move(self, d_x, d_y):
        """ Move the entity by a given amount

        """

        self.x_pos += d_x
        self.y_pos += d_y

    def move_towards(self, target_x, target_y, game_map, entities):
        """ Moves a non-player entity towards a target coordinate

        """

        dx = target_x - self.x_pos
        dy = target_y - self.y_pos
        distance = sqrt(dx**2 + dy**2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x_pos + dx, self.y_pos + dy)
                or get_blocking_entities_at_location(entities, self.x_pos + dx,
                                                     self.y_pos + dy)):
            self.move(dx, dy)

    def distance_to(self, other):
        """ Get distance between the Entity and its target

        """

        dx = other.x_pos - self.x_pos
        dy = other.y_pos - self.y_pos
        return sqrt(dx**2 + dy**2)

    def distance(self, x_pos, y_pos):
        """ Get distance between the Entity and an arbitrary point

        """

        return sqrt((x_pos - self.x_pos)**2 + (y_pos - self.y_pos)**2)

    def move_astar(self, target, entities, game_map):
        """ A-star pathfinding algorithm

        """

        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y_1 in range(game_map.height):
            for x_1 in range(game_map.width):
                tcod.map_set_properties(
                    fov,
                    x_1,
                    y_1,
                    not game_map.tiles[x_1][y_1].block_sight,
                    not game_map.tiles[x_1][y_1].blocked,
                )

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x_pos, entity.y_pos, True,
                                        False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x_pos, self.y_pos, target.x_pos,
                          target.y_pos)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x_pos, y_pos = tcod.path_walk(my_path, True)
            if x_pos or y_pos:
                # Set self's coordinates to the next path tile
                self.x_pos = x_pos
                self.y_pos = y_pos
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x_pos, target.y_pos, game_map, entities)

        # Delete the path to free memory
        tcod.path_delete(my_path)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """ Return entity at target destination if the entity blocks

    """

    for entity in entities:
        entity_at_position = (entity.x_pos == destination_x
                              and entity.y_pos == destination_y)
        if entity.blocks and entity_at_position:
            return entity

    return None
