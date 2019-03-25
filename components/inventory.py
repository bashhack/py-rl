""" Inventory:

- inventory component

"""

import tcod

from game_messages import Message


class Inventory:
    """ A component for Entities that hold information about inventory

    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                "item_added":
                None,
                "message":
                Message("You cannot carry any more, your inventory is full",
                        tcod.yellow),
            })
        else:
            results.append({
                'item_added':
                item,
                'message':
                Message(f'You pick up the {item.name}!', tcod.blue)
            })
            self.items.append(item)

        return results
