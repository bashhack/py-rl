""" Fighter:

- fighter component

"""

import tcod

from game_messages import Message


class Fighter:
    """ A component for Entities that holds information for combat

    """

    def __init__(self, hp, defense, power, xp=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp

    def take_damage(self, amount):
        """ Reduces the HP of an entity

        """

        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({"dead": self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        """ Increases the HP of an entity

        """

        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        """ Tracks attack damage

        """

        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({
                "message":
                Message(
                    f"{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points",
                    tcod.white,
                )
            })
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({
                "message":
                Message(
                    f"{self.owner.name.capitalize()} attacks {target.name} but does no damage.",
                    tcod.white,
                )
            })

        return results
