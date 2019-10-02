"""
God Commands!

These are the commands that the Gods of Ithir can use
to spend their mana. Mana is spent on things such as
sending visions, performing miracle, etc. Gods recieve
mana every time one of their followers prays to them.
"""

from commands.base import ArxCommand, ArxPlayerCommand
from world import miracles
from server.utils.arx_utils import inform_staff


class CmdUseMana(ArxCommand):
    """
    xp
    Usage:
        miracle
        miracle/spend  <act name>
        miracle/cost   <act name>

    Displays how much mana you have available to spend. /spend
    will allow you to keep track of how many godly acts you have
    performed. /cost will show you how much each type of miracle
    costs to perform.

    """
    key = "miracle"
    aliases = ["lifewell", "miracles"]
    locks = "cmd:perm(builders)"
    help_category = "Admin"

    def display_traits(self):
        caller = self.caller
        caller.msg("{wUnspent Mana:{n %s" % caller.db.mana)
        caller.msg("{wLifetime Earned Mana:{n %s" % caller.db.total_mana)
        all_miracles = ", ".join(stats for stats in miracles.VALID_MIRACLES)
        caller.msg("\n{wMiracle names:{n")
        caller.msg(all_miracles)

    # noinspection PyUnresolvedReferences
    def func(self):
        """
        Allows the character to check their xp, and spend it if they use
        the /spend switch and meet the requirements.
        """
        caller = self.caller
        if self.cmdstring == "learn":
            self.switches.append("spend")
        if not self.args:
            # Just display our xp
            self.display_traits()
            return
        args = self.args.lower()
        # get cost already factors in if we have a trainer, so no need to check
        if args in miracles.VALID_MIRACLES:
            cost = miracles.get_miracles_cost(caller, args)
            current = caller.attributes.get(args)
            stype = "miracle"
        else:
            caller.msg("'%s' wasn't identified as a miracle type." % self.args)
            return
        if "cost" in self.switches:
            caller.msg("Cost for %s: %s" % (self.args, cost))
            return
        if "spend" in self.switches:
            if cost > caller.db.mana:
                caller.msg("Unable to raise %s. The cost is %s, and you have %s mana." % (args, cost, caller.db.mana))
                return
            elif stype == "miracle":
                caller.adjust_xp(-cost)
                stats_and_skills.adjust_stat(caller, args)
                caller.msg("You have increased your %s to %s." % (args, current + 1))
                return
            return
        # invalid or no switch + arguments
        caller.msg("Usage: miracle/spend <miracle type>")
