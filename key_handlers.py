""" Key Handlers:

- bind keys to keymap for given game states

"""

import tcod

from game_states import GameStates


def handle_keys(key, game_state):
    """ Given a game state and key, calls appropriate key handler

    """

    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    if game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    if game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    if game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    return {}


def handle_player_turn_keys(key):
    """ Binds keys to keymap for player turn

    """

    key_char = chr(key.c)

    keymap = {}

    # Movement keys
    if key.vk == tcod.KEY_UP or key_char == "k":
        keymap["move"] = (0, -1)
    if key.vk == tcod.KEY_DOWN or key_char == "j":
        keymap["move"] = (0, 1)
    if key.vk == tcod.KEY_LEFT or key_char == "h":
        keymap["move"] = (-1, 0)
    if key.vk == tcod.KEY_RIGHT or key_char == "l":
        keymap["move"] = (1, 0)
    if key_char == "y":
        keymap["move"] = (-1, -1)
    if key_char == "u":
        keymap["move"] = (1, -1)
    if key_char == "b":
        keymap["move"] = (-1, 1)
    if key_char == "n":
        keymap["move"] = (1, 1)

    if key_char == "g":
        # Pickup item
        keymap["pickup"] = True

    if key_char == "i":
        # Show inventory
        keymap["show_inventory"] = True

    if key_char == "d":
        # Drop item from inventory
        keymap["drop_inventory"] = True

    if key.vk == tcod.KEY_ENTER:
        # Navigate the stairs
        keymap['take_stairs'] = True

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True
    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap


def handle_player_dead_keys(key):
    """ Binds keys to keymap for valid actions if player dead

    """

    key_char = chr(key.c)

    keymap = {}

    if key_char == "i":
        # Show inventory
        return {"show_inventory": True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True
    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap


def handle_inventory_keys(key):
    """ Binds keys to keymap for inventory actions

    """

    index = key.c - ord("a")

    keymap = {}

    if index >= 0:
        keymap["inventory_index"] = index

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True

    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap


def handle_targeting_keys(key):
    """ Binds keys to keymap if targeting

    """

    keymap = {}

    if key.vk == tcod.KEY_ESCAPE:
        keymap["exit"] = True

    return keymap


def handle_mouse(mouse):
    """ Binds mouse movement to left and right click actions

    """

    (x_pos, y_pos) = (mouse.cx, mouse.cy)

    keymap = {}

    if mouse.lbutton_pressed:
        keymap["left_click"] = (x_pos, y_pos)
    elif mouse.rbutton_pressed:
        keymap["right_click"] = (x_pos, y_pos)

    return keymap


def handle_level_up_menu(key):
    """ Binds keys to keymap for level up menu

    """

    key_char = chr(key.c)

    keymap = {}

    if key_char == 'a':
        keymap['level_up'] = 'hp'
    if key_char == 'a':
        keymap['level_up'] = 'str'
    if key_char == 'a':
        keymap['level_up'] = 'def'

    return keymap


def handle_main_menu(key):
    """ Binds keys to keymap for main menu

    """

    keymap = {}

    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            keymap['new_game'] = True
        elif key_char == 'b':
            keymap['load_game'] = True
        elif key_char == 'c' or key.vk == tcod.KEY_ESCAPE:
            keymap['exit'] = True

    return keymap
