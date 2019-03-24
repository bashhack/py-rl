""" Game Map:

- creates the tile container

"""
from random import randint

import tcod

from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    """ Creates a game map (contains Tile objects)

    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        """ Creates 2D array of tiles

        """

        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(
        self,
        max_rooms,
        room_min_size,
        room_max_size,
        map_width,
        map_height,
        player,
        entities,
        max_monsters_per_room,
    ):
        """ Given max num of rooms: create them + connect with tunnels

        """

        rooms = []
        num_rooms = 0

        for _ in range(max_rooms):
            width = randint(room_min_size, room_max_size)
            height = randint(room_min_size, room_max_size)
            x_pos = randint(0, map_width - width - 1)
            y_pos = randint(0, map_height - height - 1)

            new_room = Rect(x_pos, y_pos, width, height)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # valid room
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts
                    player.x_pos = new_x
                    player.y_pos = new_y
                else:
                    # all rooms after the first
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin
                    if randint(0, 1) == 1:
                        # move horizontally, then vertically
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y)
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                    else:
                        # move vertically, then horizontally
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y)

                # add monsters
                self.place_entities(new_room, entities, max_monsters_per_room)

                # append new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        """ Iterate over tiles in a rectangle, make passable

        """

        for x_pos in range(room.x_1 + 1, room.x_2):
            for y_pos in range(room.y_1 + 1, room.y_2):
                self.tiles[x_pos][y_pos].blocked = False
                self.tiles[x_pos][y_pos].block_sight = False

    def create_horizontal_tunnel(self, prev_x, new_x, prev_y_pos):
        """ Creates an x-axis tunnel given a prev_x, new_x, and prev_y position

        """

        for x_pos in range(min(prev_x, new_x), max(prev_x, new_x) + 1):
            self.tiles[x_pos][prev_y_pos].blocked = False
            self.tiles[x_pos][prev_y_pos].block_sight = False

    def create_vertical_tunnel(self, prev_y, new_y, prev_x_pos):
        """ Creates an y-axis tunnel given a prev_y, new_y, and prev_x position

        """

        for y_pos in range(min(prev_y, new_y), max(prev_y, new_y) + 1):
            self.tiles[prev_x_pos][y_pos].blocked = False
            self.tiles[prev_x_pos][y_pos].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        """ Places a random number of monsters in a room

        """

        number_of_monsters = randint(0, max_monsters_per_room)

        for _ in range(number_of_monsters):
            x_pos = randint(room.x_1 + 1, room.x_2 - 1)
            y_pos = randint(room.y_1 + 1, room.y_2 - 1)

            if not any(
                [
                    entity
                    for entity in entities
                    if entity.x_pos == x_pos and entity.y_pos == y_pos
                ]
            ):
                if randint(0, 100) < 80:
                    monster = Entity(
                        x_pos, y_pos, "o", tcod.desaturated_green, "Orc", blocks=True
                    )
                else:
                    monster = Entity(
                        x_pos, y_pos, "T", tcod.darker_green, "Troll", blocks=True
                    )

                entities.append(monster)

    def is_blocked(self, x_pos, y_pos):
        """ Check if coordinate is blocked

        """

        if self.tiles[x_pos][y_pos].blocked:
            return True

        return False
