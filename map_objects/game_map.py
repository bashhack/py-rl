""" Game Map:

- creates the tile container

"""
from random import randint

import tcod

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from render_functions import RenderOrder


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

        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width,
                 map_height, player, entities, max_monsters_per_room,
                 max_items_per_room):
        """ Given max num of rooms: create them + connect with tunnels

        """

        rooms = []
        num_rooms = 0

        for _ in range(max_rooms):
            # random width and height
            width = randint(room_min_size, room_max_size)
            height = randint(room_min_size, room_max_size)
            # random position without going out of the bounds of the map
            x_pos = randint(0, map_width - width - 1)
            y_pos = randint(0, map_height - height - 1)

            new_room = Rect(x_pos, y_pos, width, height)

            # run through other rooms to see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # valid room
                self.create_room(new_room)

                # center the coordinates of the new room
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
                        self.create_vertical_tunnel(prev_y, new_y, new_x)
                    else:
                        # move vertically, then horizontally
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                        self.create_horizontal_tunnel(prev_x, new_x, new_y)

                # add monsters
                self.place_entities(new_room, entities, max_monsters_per_room,
                                    max_items_per_room)

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

    def create_horizontal_tunnel(self, prev_x, new_x, y_pos):
        """ Creates an x-axis tunnel given a prev_x, new_x, and y position

        """

        for x_pos in range(min(prev_x, new_x), max(prev_x, new_x) + 1):
            self.tiles[x_pos][y_pos].blocked = False
            self.tiles[x_pos][y_pos].block_sight = False

    def create_vertical_tunnel(self, prev_y, new_y, x_pos):
        """ Creates an y-axis tunnel given a prev_y, new_y, and x position

        """

        for y_pos in range(min(prev_y, new_y), max(prev_y, new_y) + 1):
            self.tiles[x_pos][y_pos].blocked = False
            self.tiles[x_pos][y_pos].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room,
                       max_items_per_room):
        """ Places a random number of monsters in a room

        """

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for _ in range(number_of_monsters):
            x_pos = randint(room.x_1 + 1, room.x_2 - 1)
            y_pos = randint(room.y_1 + 1, room.y_2 - 1)

            if not any([
                    entity for entity in entities
                    if entity.x_pos == x_pos and entity.y_pos == y_pos
            ]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x_pos,
                        y_pos,
                        "o",
                        tcod.desaturated_green,
                        "Orc",
                        blocks=True,
                        fighter=fighter_component,
                        render_order=RenderOrder.ACTOR,
                        ai=ai_component,
                    )
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x_pos,
                        y_pos,
                        "T",
                        tcod.darker_green,
                        "Troll",
                        blocks=True,
                        fighter=fighter_component,
                        render_order=RenderOrder.ACTOR,
                        ai=ai_component,
                    )

                entities.append(monster)
        for _ in range(number_of_items):
            x_pos = randint(room.x_1 + 1, room.x_2 - 1)
            y_pos = randint(room.y_1 + 1, room.y_2 - 1)

            if not any([
                    entity for entity in entities
                    if entity.x_pos == x_pos and entity.y_pos == y_pos
            ]):
                item_component = Item()
                item = Entity(
                    x_pos,
                    y_pos,
                    '!',
                    tcod.violet,
                    'Healing Potion',
                    render_order=RenderOrder.ITEM,
                    item=item_component)
                entities.append(item)

    def is_blocked(self, x_pos, y_pos):
        """ Check if coordinate is blocked

        """

        if self.tiles[x_pos][y_pos].blocked:
            return True

        return False
