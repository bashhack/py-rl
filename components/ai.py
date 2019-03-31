""" AI:

- define enemy AI

"""

import tcod


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
