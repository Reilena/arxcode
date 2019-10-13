"""
This is the list of mericles that the Gods
can choose from. When they spend mana on a
mericle, the tally of how many of that type
of mericle goes up.
"""
from .roll import Roll


MINOR_MIRACLES = ("send vision", "play trick")
MEDIUM_MIRACLES = ("boon", "intervention")
MASSIVE_MIRACLES = ("favored", "physical appearance")
VALID_MIRACLES = MINOR_MIRACLES + MEDIUM_MIRACLES + MASSIVE_MIRACLES

MINOR_MIRACLES_COST = 10
MEDIUM_MIRACLES_COST = 50
MASSIVE_MIRACLES_COST = 100


def get_partial_match(args, s_type):
    # helper function for finding partial string match of stat/skills
    if s_type == "miracle":
        word_list = VALID_MIRACLES
    else:
        return
    matches = []
    for word in word_list:
        if word.startswith(args):
            matches.append(word)
    return matches


def do_dice_check(*args, **kwargs):
    """
    Sending stuff to Roll class for dice checks; assumed to already be run through get_partial_match.
    """
    roll = Roll(*args, **kwargs)
    roll.roll()
    return roll.result


def get_minor_cost():
    """Currently minor mericles cost 10 mana"""
    cost = MINOR_MIRACLES_COST
    return int(cost)


def get_medium_cost():
    """Currently medium mericles cost 50 mana"""
    cost = MEDIUM_MIRACLES_COST
    return int(cost)


def get_massive_cost():
    """Currently massive mericles cost 100 mana"""
    cost = MASSIVE_MIRACLES_COST
    return int(cost)


def get_miracles_cost(caller, field):
    if field in MINOR_MIRACLES:
        cost = MINOR_MIRACLES_COST
        return int(cost)
    elif field in MEDIUM_MIRACLES:
        cost = MEDIUM_MIRACLES_COST
        return int(cost)
    elif field in MASSIVE_MIRACLES:
        cost = MASSIVE_MIRACLES_COST
        return int(cost)


def adjust_miracles(caller, field, value=1):
    if field not in VALID_MIRACLES:
        raise Exception("Error in adjust_skill: %s not found as a valid skill." % field)
    try:
        caller.db.skills[field] += value
    except KeyError:
        caller.db.skills[field] = value
    caller.db.trainer = None
