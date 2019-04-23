""" Menu:

- create menu functions for inventory

"""

import tcod


def menu(console, header, options, width, screen_width, screen_height):
    """ Main game menu (displays options available for selection)

    """

    if len(options) > 26:
        raise ValueError("Cannot have a menu with more than 26 options")

    # total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(console, 0, 0, width,
                                                 screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)

    # print the header, with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE,
                               tcod.LEFT, header)

    # print all the options
    y_pos = header_height
    letter_index = ord("a")
    for option_text in options:
        text = f"({chr(letter_index)})" + option_text
        tcod.console_print_ex(window, 0, y_pos, tcod.BKGND_NONE, tcod.LEFT,
                              text)
        y_pos += 1
        letter_index += 1

    # blit the contents of 'window' to the root console
    x_pos = int(screen_width / 2 - width / 2)
    y_pos = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x_pos, y_pos, 1.0, 0.7)


def inventory_menu(console, header, inventory, inventory_width, screen_width,
                   screen_height):
    """ Add inventory items to in-game menu

    """

    # show a menu with each item of the inventory as an option
    if not inventory.items:
        options = ["Inventory is empty."]
    else:
        options = [item.name for item in inventory.items]

    menu(console, header, options, inventory_width, screen_width,
         screen_height)


def main_menu(console, background_image, screen_width, screen_height):
    """ Main game splash menu

    """

    tcod.image_blit_2x(background_image, 0, 0, 0)

    tcod.console_set_default_foreground(0, tcod.light_yellow)
    tcod.console_print_ex(0, int(screen_width / 2),
                          int(screen_height / 2) - 4, tcod.BKGND_NONE,
                          tcod.CENTER, 'TOMBS OF THE ANCIENT KINGS')
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2),
                          tcod.BKGND_NONE, tcod.CENTER, 'By bashhack')

    menu(console, '', ['Play new game', 'Continue last game', 'Quit'], 24,
         screen_width, screen_height)


def level_up_menu(console, header, player, menu_width, screen_width,
                  screen_height):
    """ Menu for leveling up options

    """

    options = [
        f'Consitution (+20 HP, from {player.fighter.max_hp})',
        f'Strength (+1 attack, from {player.fighter.power})',
        f'Agility (+1 defense, from {player.fighter.defense})'
    ]
    menu(console, header, options, menu_width, screen_width, screen_height)


def message_box(console, header, width, screen_width, screen_height):
    """ General purpose menu for displaying messages

    """

    menu(console, header, [], width, screen_width, screen_height)
