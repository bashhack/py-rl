""" Render Functions:

- entity rendering

"""

import tcod


def draw_entity(console, entity, fov_map):
    """ Draws an entity on the console

    """

    if tcod.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos):
        tcod.console_set_default_foreground(console, entity.color)
        tcod.console_put_char(
            console, entity.x_pos, entity.y_pos, entity.char, tcod.BKGND_NONE
        )


def clear_entity(console, entity):
    """ Erases the character that represents this entity

    """

    tcod.console_put_char(console, entity.x_pos, entity.y_pos, " ", tcod.BKGND_NONE)


def render_all(
    console,
    entities,
    game_map,
    fov_map,
    fov_recompute,
    screen_width,
    screen_height,
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
    for entity in entities:
        draw_entity(console, entity, fov_map)

    tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console, entities):
    """ Clears all entities

    """

    for entity in entities:
        clear_entity(console, entity)
