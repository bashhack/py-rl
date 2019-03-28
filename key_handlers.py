""" Key Handlers

- binds key input to keymap

"""

import tcod

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key, game_state)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    return {}


def handle_player_turn_keys(key, game_state):
    """ Maps key to keymap

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

    if key_char == 'g':
        # Pickup item
        keymap['pickup'] = True

    if key_char == 'i':
        # Show inventory
        keymap['show_inventory'] = True

    if key_char == 'd':
        # Drop item from inventory
        keymap['drop_inventory'] = True

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True
    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    keymap = {}

    if key_char == 'i':
        # Show inventory
        return {'show_inventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True
    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap


def handle_inventory_keys(key):
    index = key.c - ord('a')

    keymap = {}

    if index >= 0:
        keymap['inventory_index'] = index

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True

    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap
