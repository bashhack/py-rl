""" Engine:

- main game loop

"""

import tcod

from entity import Entity, get_blocking_entities_at_location
from exception_handlers import EntityError
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from key_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

# Display
OPEN_GL_2_RENDERER = 4
SDL_2_RENDERER = 3
SCREEN = {"width": 80, "height": 50}

# Map
MAP = {"width": 80, "height": 45}
COLORS = {
    "dark_wall": tcod.Color(0, 0, 100),  # dark blue
    "dark_ground": tcod.Color(50, 50, 150),  # light blue
    "light_wall": tcod.Color(130, 110, 50),
    "light_ground": tcod.Color(200, 180, 50),
}

# Room
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# Field of View
FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

# Monsters
MAX_MONSTERS_PER_ROOM = 3


def create_player(char="@", color=tcod.white, screen=None):
    """ Creates a single player entity

    """

    if not screen:
        raise EntityError("Player entity must be rendered " "with screen context (w/h)")

    player_x = int(screen.get("width") / 2)
    player_y = int(screen.get("height") / 2)
    player = Entity(player_x, player_y, char, color, "Player", blocks=True)
    return player


def main():
    """ Main game loop

    Init console + wraps key events

    """

    player = create_player(screen=SCREEN)

    entities = [player]

    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    )
    tcod.console_init_root(
        SCREEN["width"], SCREEN["height"], "rl first", False, SDL_2_RENDERER
    )

    console = tcod.console.Console(SCREEN["width"], SCREEN["height"])

    game_map = GameMap(MAP["width"], MAP["height"])
    game_map.make_map(
        MAX_ROOMS,
        ROOM_MIN_SIZE,
        ROOM_MIN_SIZE,
        MAP["width"],
        MAP["height"],
        player,
        entities,
        MAX_MONSTERS_PER_ROOM,
    )

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(
                fov_map,
                player.x_pos,
                player.y_pos,
                FOV_RADIUS,
                FOV_LIGHT_WALLS,
                FOV_ALGORITHM,
            )

        render_all(
            console,
            entities,
            game_map,
            fov_map,
            fov_recompute,
            SCREEN["width"],
            SCREEN["height"],
            COLORS,
        )

        fov_recompute = False

        tcod.console_flush()

        clear_all(console, entities)

        action = handle_keys(key)
        move = action.get("move")
        exit_game = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move and game_state == GameStates.PLAYERS_TURN:
            d_x, d_y = move
            destination_x = player.x_pos + d_x
            destination_y = player.y_pos + d_y

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y
                )

                if target:
                    print(
                        f"You kick the {target.name} in the shins, much to its annoyance!"
                    )
                else:
                    player.move(d_x, d_y)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print(f"The {entity.name} ponders the meaning of its existence.")

            game_state = GameStates.PLAYERS_TURN

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if exit_game:
            return True


if __name__ == "__main__":
    main()
