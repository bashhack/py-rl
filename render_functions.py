""" Render Functions:

- entity rendering

"""

from enum import Enum, auto

import tcod


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [
        entity.name for entity in entities
        if entity.x_pos == x and entity.y_pos == y
        and tcod.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos)
    ]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x_pos, y_pos, total_width, name, value, maximum,
               bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x_pos, y_pos, total_width, 1, False,
                      tcod.BKGND_SCREEN)
    tcod.console_set_default_background(panel, bar_color)

    if bar_width > 0:
        tcod.console_rect(panel, x_pos, y_pos, bar_width, 1, False,
                          tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(
        panel,
        int(x_pos + total_width / 2),
        y_pos,
        tcod.BKGND_NONE,
        tcod.CENTER,
        f"{name}: {value}/{maximum}",
    )


def draw_entity(console, entity, fov_map):
    """ Draws an entity on the console

    """

    if tcod.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos):
        tcod.console_set_default_foreground(console, entity.color)
        tcod.console_put_char(console, entity.x_pos, entity.y_pos, entity.char,
                              tcod.BKGND_NONE)


def clear_entity(console, entity):
    """ Erases the character that represents this entity

    """

    tcod.console_put_char(console, entity.x_pos, entity.y_pos, " ",
                          tcod.BKGND_NONE)


def render_all(
        console,
        panel,
        entities,
        player,
        game_map,
        fov_map,
        fov_recompute,
        message_log,
        screen_width,
        screen_height,
        bar_width,
        panel_height,
        panel_y,
        mouse,
        colors,
):
    """ Draw all entities

    """

    # Draw all tiles
    if fov_recompute:
        for y_pos in range(game_map.height):
            for x_pos in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x_pos, y_pos)
                wall = game_map.tiles[x_pos][y_pos].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(
                            console,
                            x_pos,
                            y_pos,
                            colors.get("light_wall"),
                            tcod.BKGND_SET,
                        )
                    else:
                        tcod.console_set_char_background(
                            console,
                            x_pos,
                            y_pos,
                            colors.get("light_ground"),
                            tcod.BKGND_SET,
                        )
                    game_map.tiles[x_pos][y_pos].explored = True
                elif game_map.tiles[x_pos][y_pos].explored:
                    if wall:
                        tcod.console_set_char_background(
                            console,
                            x_pos,
                            y_pos,
                            colors.get("dark_wall"),
                            tcod.BKGND_SET,
                        )
                    else:
                        tcod.console_set_char_background(
                            console,
                            x_pos,
                            y_pos,
                            colors.get("dark_ground"),
                            tcod.BKGND_SET,
                        )

    # Draw all entities
    entities_in_render_order = sorted(
        entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(console, entity, fov_map)

    tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE,
                              tcod.LEFT, message.text)
        y += 1

    render_bar(
        panel,
        1,
        1,
        bar_width,
        "HP",
        player.fighter.hp,
        player.fighter.max_hp,
        tcod.light_red,
        tcod.darker_red,
    )

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                          get_names_under_mouse(mouse, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)


def clear_all(console, entities):
    """ Clears all entities

    """

    for entity in entities:
        clear_entity(console, entity)
