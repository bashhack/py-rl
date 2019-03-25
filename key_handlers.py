""" Key Handlers

- binds key input to keymap

"""

import tcod


def handle_keys(key):
    """ Maps key to keymap

    """

    key_char = chr(key.c)

    keymap = {"move": None, "fullscreen": None, "exit": None}

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

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True
    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap
