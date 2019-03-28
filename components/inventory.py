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

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(
                self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        item.x_pos = self.owner.x_pos
        item.y_pos = self.owner.y_pos

        self.remove_item(item)
        results.append({
            'item_dropped':
            item,
            'message':
            Message(f'You dropped the {item.name}', tcod.yellow)
        })

        return results
