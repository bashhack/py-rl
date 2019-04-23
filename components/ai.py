""" AI:

- define enemy AI

"""

import tcod

from random import randint
from game_messages import Message


class BasicMonster:
    """ Simple AI for an enemy

    """

    def take_turn(self, target, fov_map, game_map, entities):
        """ Determines if monster moves or attacks

        """

        results = []

        monster = self.owner

        if tcod.map_is_in_fov(fov_map, monster.x_pos, monster.y_pos):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results


class ConfusedMonster:
    """ AI for a state confusion, acting temporarily upon a monster

    """

    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        """ Takes a turn for a confused monster, randomly moving about

        """

        results = []

        if self.number_of_turns > 0:
            random_x_pos = self.owner.x_pos + randint(0, 2) - 1
            random_y_pos = self.owner.y_pos + randint(0, 2) - 1

            if random_x_pos != self.owner.x_pos and random_y_pos != self.owner.y_pos:
                self.owner.move_towards(random_x_pos, random_y_pos, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message(f'The {self.owner.name} is no longer confused!', tcod.red)})

        return results
