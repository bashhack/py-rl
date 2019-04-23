import tcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder


def get_constants():
    """ Constants used in initialization of a new game

    """

    WINDOW_TITLE = 'Py RL'

    # Display
    SDL_2_RENDERER = 3

    # Screen
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    # UI
    BAR_WIDTH = 20
    PANEL_HEIGHT = 7
    PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

    # Messages
    MESSAGE_X = BAR_WIDTH + 2
    MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
    MESSAGE_HEIGHT = PANEL_HEIGHT - 1

    # Field of View
    FOV_ALGORITHM = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    # Map
    MAP_WIDTH = 80
    MAP_HEIGHT = 43

    # Room
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30

    # Monsters
    MAX_MONSTERS_PER_ROOM = 3
    MAX_ITEMS_PER_ROOM = 2

    COLORS = {
        "dark_wall": tcod.Color(0, 0, 100),  # dark blue
        "dark_ground": tcod.Color(50, 50, 150),  # light blue
        "light_wall": tcod.Color(130, 110, 50),  # dark yellow
        "light_ground": tcod.Color(200, 180, 50),  # light yellow
    }

    constants = {
        'window_title': WINDOW_TITLE,
        'sdl_renderer': SDL_2_RENDERER,
        'screen_width': SCREEN_WIDTH,
        'screen_height': SCREEN_HEIGHT,
        'bar_width': BAR_WIDTH,
        'panel_height': PANEL_HEIGHT,
        'panel_y': PANEL_Y,
        'message_x': MESSAGE_X,
        'message_width': MESSAGE_WIDTH,
        'message_height': MESSAGE_HEIGHT,
        'map_width': MAP_WIDTH,
        'map_height': MAP_HEIGHT,
        'room_max_size': ROOM_MAX_SIZE,
        'room_min_size': ROOM_MIN_SIZE,
        'max_rooms': MAX_ROOMS,
        'fov_algorithm': FOV_ALGORITHM,
        'fov_light_walls': FOV_LIGHT_WALLS,
        'fov_radius': FOV_RADIUS,
        'max_monsters_per_room': MAX_MONSTERS_PER_ROOM,
        'max_items_per_room': MAX_ITEMS_PER_ROOM,
        'colors': COLORS,
    }

    return constants


def get_game_variables(constants):
    """ Initialize player, entities list, and game map

    """

    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    level_component = Level()
    player = Entity(
        0,
        0,
        '@',
        tcod.white,
        'Player',
        blocks=True,
        render_order=RenderOrder.ACTOR,
        fighter=fighter_component,
        inventory=inventory_component,
        level=level_component)
    entities = [player]

    game_map = GameMap(constants["map_width"], constants["map_height"])
    game_map.make_map(
        constants["max_rooms"],
        constants["room_min_size"],
        constants["room_max_size"],
        constants["map_width"],
        constants["map_height"],
        player,
        entities,
        constants["max_monsters_per_room"],
        constants["max_items_per_room"],
    )

    message_log = MessageLog(constants["message_x"],
                             constants["message_width"],
                             constants["message_height"])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
