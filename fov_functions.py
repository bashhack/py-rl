""" Fov Functions:

- create field of view

"""

import tcod


def initialize_fov(game_map):
    """ Initialize the field of view

    """

    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y_pos in range(game_map.height):
        for x_pos in range(game_map.width):
            tcod.map_set_properties(
                fov_map,
                x_pos,
                y_pos,
                not game_map.tiles[x_pos][y_pos].block_sight,
                not game_map.tiles[x_pos][y_pos].blocked,
            )

    return fov_map


def recompute_fov(fov_map, x_pos, y_pos, radius, light_walls=True, algorithm=0):
    """ Triggers a recompute of the field of view

    """

    tcod.map_compute_fov(fov_map, x_pos, y_pos, radius, light_walls, algorithm)
