""" Key Handlers

- binds key input to keymap

"""

import tcod


def handle_keys(key):
    """ Maps key to keymap

    """

    keymap = {"move": None, "fullscreen": None, "exit": None}

    # Movement keys
    if key.vk == tcod.KEY_UP:
        keymap["move"] = (0, -1)
    if key.vk == tcod.KEY_DOWN:
        keymap["move"] = (0, 1)
    if key.vk == tcod.KEY_LEFT:
        keymap["move"] = (-1, 0)
    if key.vk == tcod.KEY_RIGHT:
        keymap["move"] = (1, 0)
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        keymap["fullscreen"] = True
    if key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        keymap["exit"] = True

    return keymap
