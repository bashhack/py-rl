""" Game States:

- store game state identifiers

"""

from enum import Enum, auto


class GameStates(Enum):
    """ Static collection of game states

    """

    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()
    LEVEL_UP = auto()
