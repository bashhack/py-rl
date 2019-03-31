""" Engine:

- main game loop

"""

import tcod

from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message, MessageLog
from game_states import GameStates
from key_handlers import handle_keys, handle_mouse
from map_objects.game_map import GameMap
from render_functions import RenderOrder, clear_all, render_all

# Display
OPEN_GL_2_RENDERER = 4
SDL_2_RENDERER = 3
SCREEN = {"width": 80, "height": 50}

# Map
MAP = {"width": 80, "height": 43}
COLORS = {
    "dark_wall": tcod.Color(0, 0, 100),  # dark blue
    "dark_ground": tcod.Color(50, 50, 150),  # light blue
    "light_wall": tcod.Color(130, 110, 50),  # dark yellow
    "light_ground": tcod.Color(200, 180, 50),  # light yellow
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
MAX_ITEMS_PER_ROOM = 2

# UI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN["height"] - PANEL_HEIGHT

# Messages
MESSAGE_X = BAR_WIDTH + 2
MESSAGE_WIDTH = SCREEN["width"] - BAR_WIDTH - 2
MESSAGE_HEIGHT = PANEL_HEIGHT - 1


def main():
    """ Main game loop

    Init console + wraps key events

    """

    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(
        0,
        0,
        "@",
        tcod.white,
        "Player",
        blocks=True,
        render_order=RenderOrder.ACTOR,
        fighter=fighter_component,
        inventory=inventory_component,
    )

    entities = [player]

    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    )
    tcod.console_init_root(
        SCREEN["width"], SCREEN["height"], "rl first", False, SDL_2_RENDERER
    )

    console = tcod.console.Console(SCREEN["width"], SCREEN["height"])
    panel = tcod.console_new(SCREEN["width"], PANEL_HEIGHT)

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
        MAX_ITEMS_PER_ROOM,
    )

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(MESSAGE_X, MESSAGE_WIDTH, MESSAGE_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

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
            panel,
            entities,
            player,
            game_map,
            fov_map,
            fov_recompute,
            message_log,
            SCREEN["width"],
            SCREEN["height"],
            BAR_WIDTH,
            PANEL_HEIGHT,
            PANEL_Y,
            mouse,
            COLORS,
            game_state,
        )

        fov_recompute = False

        tcod.console_flush()

        clear_all(console, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get("move")
        pickup = action.get("pickup")
        show_inventory = action.get("show_inventory")
        drop_inventory = action.get("drop_inventory")
        inventory_index = action.get("inventory_index")
        exit_game = action.get("exit")
        fullscreen = action.get("fullscreen")

        left_click = mouse_action.get("left_click")
        right_click = mouse_action.get("right_click")

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            d_x, d_y = move
            destination_x = player.x_pos + d_x
            destination_y = player.y_pos + d_y

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y
                )

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(d_x, d_y)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if (
                    entity.item
                    and entity.x_pos == player.x_pos
                    and entity.y_pos == player.y_pos
                ):
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(
                    Message("There is nothing here to pick up.", tcod.yellow)
                )

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if (
            inventory_index is not None
            and previous_game_state != GameStates.PLAYER_DEAD
            and inventory_index < len(player.inventory.items)
        ):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(
                    player.inventory.use(item, entities=entities, fov_map=fov_map)
                )
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x_pos, target_y_pos = left_click

                print(left_click)

                item_use_results = player.inventory.use(
                    targeting_item,
                    entities=entities,
                    fov_map=fov_map,
                    target_x_pos=target_x_pos,
                    target_y_pos=target_y_pos,
                )
                player_turn_results.extend(item_use_results)
            elif right_click:
                print(right_click)
                player_turn_results.append({"targeting_cancelled": True})

        if exit_game:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({"targeting_cancelled": True})
            else:
                return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")
            item_added = player_turn_result.get("item_added")
            item_consumed = player_turn_result.get("consumed")
            item_dropped = player_turn_result.get("item_dropped")
            targeting = player_turn_result.get("targeting")
            targeting_cancelled = player_turn_result.get("targeting_cancelled")

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message("Targeting cancelled"))

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, fov_map, game_map, entities
                    )

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == "__main__":
    main()
