""" Item Functions:

- healing
- cast lightning
- cast fireball

"""

import tcod

from game_messages import Message


def heal(*args, **kwargs):
    """ Given an entity, determines whether healing can occur

    """

    entity = args[0]
    amount = kwargs.get("amount")

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append(
            {
                "consumed": False,
                "message": Message("You are already at full health", tcod.yellow),
            }
        )
    else:
        entity.fighter.heal(amount)
        results.append(
            {
                "consumed": True,
                "message": Message("Your wounds start to feel better!", tcod.green),
            }
        )

    return results


def cast_lightning(*args, **kwargs):
    """ Area of effect spell - determine if damage occurs for target and apply

    """

    caster = args[0]
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if (
            entity.fighter
            and entity != caster
            and tcod.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos)
        ):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append(
            {
                "consumed": True,
                "target": target,
                "message": Message(
                    f"A lightning bolt strikes the {target.name} with a loud thunder! The damage is {damage}"
                ),
            }
        )
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append(
            {
                "consumed": False,
                "target": None,
                "message": Message("No enemy is close enough to strike.", tcod.red),
            }
        )

    return results


def cast_fireball(*args, **kwargs):
    """ Targeting spell - determine if damage occurs for target and apply

    """

    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x_pos = kwargs.get("target_x_pos")
    target_y_pos = kwargs.get("target_y_pos")

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x_pos, target_y_pos):
        results.append(
            {
                "consumed": False,
                "message": Message(
                    "You cannot target a tile outside your field of view.", tcod.yellow
                ),
            }
        )
        return results

    results.append(
        {
            "consumed": True,
            "message": Message(
                f"The fireball explodes, burning everything within {radius} tiles!",
                tcod.orange,
            ),
        }
    )

    for entity in entities:
        if entity.distance(target_x_pos, target_y_pos) <= radius and entity.fighter:
            results.append(
                {
                    "message": Message(
                        f"The {entity.name} gets burned for {damage} hit points.",
                        tcod.orange,
                    )
                }
            )
            results.extend(entity.fighter.take_damage(damage))

    return results
