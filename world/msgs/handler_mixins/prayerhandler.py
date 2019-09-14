"""
Handler for Prayers
"""

from .msg_utils import get_initial_queryset, lazy_import_from_str
from .handler_base import MsgHandlerBase
from world.msgs.managers import q_search_text_body, q_receiver_character_name, PRAYER_TAG

from server.utils.arx_utils import get_date, create_arx_message


class PrayerHandler(MsgHandlerBase):
    def __init__(self, obj=None):
        """
        We'll be doing a series of delayed calls to set up the various
        attributes in the MessageHandler, since we can't have ObjectDB
        refer to Msg during the loading-up process.
        """
        super(PrayerHandler, self).__init__(obj)
        # White Journal entries that obj has written
        self._prayer = None

    @property
    def prayer(self):
        if self._prayer is None:
            self.build_prayer()
        return self._prayer

    @prayer.setter
    def prayer(self, value):
        self._prayer = value

    def build_prayerdict(self):
        """
        Builds a dictionary of names of people we have prayers to into a list
        of prayer Msgs we've made about that God.
        """
        rels = get_initial_queryset("Prayer").prayers().written_by(self.obj)
        #rels = rels.prayers()
        relsdict = {}
        for rel in rels:
            if rel.db_receivers_objects.all():
                name = rel.db_receivers_objects.all()[0].key.lower()
                relslist = relsdict.get(name, [])
                relslist.append(rel)
                relsdict[name] = relslist
            self._prayer = relsdict
        return relsdict

    def build_prayer(self):
        """
        Returns a list of all 'white journal' entries our character has written.
        """
        self._prayer = list(get_initial_queryset("Prayer").written_by(self.obj))
        return self._prayer

    def add_to_prayer(self, msg):
        """adds message to our prayer"""
        msg.add_prayer_locks()
        self.prayer.insert(0, msg)
        return msg

    def add_prayer(self, msg, targ, date=""):
        """creates a new prayer message and returns it"""
        cls = lazy_import_from_str("Prayer")
        if not date:
            date = get_date()
        header = self.create_date_header(date)
        # name = targ.key.lower()
        receivers = [targ, self.obj.player_ob]
        tags = PRAYER_TAG
        msg = create_arx_message(self.obj, msg, receivers=receivers, header=header, cls=cls, tags=tags)
        msg = self.add_to_prayer(msg)
        # prayers = self.prayer
        # prayerlist = prayers.get(name, [])
        # targ[name] = prayerlist
        # prayerlist.insert(0, msg)
        # prayers made this week, for mana purposes
        self.num_prayers += 1
        return msg

    def search_prayer(self, text):
        """
        Returns all matches for text in character's prayers
        """
        Prayer = lazy_import_from_str("Prayer")
        matches = Prayer.objects.written_by(self.obj).filter(q_receiver_character_name(text) |
                                                             q_search_text_body(text)).distinct()

        return list(matches)

    def size(self):
        return len(self.prayer)

    @property
    def num_prayers(self):
        return self.obj.db.num_prayers or 0

    @num_prayers.setter
    def num_prayers(self, val):
        self.obj.db.num_prayers = val

    def delete_prayers(self, msg):
        self.prayer.remove(msg)
        msg.delete()

    def disp_entry_by_num(self, num=1, caller=None):
        prayer = self.prayer
        pname = "prayer"
        msg = "Message {w#%s{n for {c%s{n's %s:\n" % (num, self.obj, pname)
        num -= 1
        entry = prayer[num]
        if not caller:
            if entry.access(caller, 'read'):
                return False
        # noinspection PyBroadException
        try:
            subjects = entry.db_receivers_objects.all()
            if subjects:
                msg += "Prayer to: {c%s{n\n" % ", ".join(ob.key for ob in subjects)
            msg += self.disp_entry(entry)
            # mark the player as having read this
            if caller:
                if caller.player_ob:
                    caller = caller.player_ob
                entry.receivers = caller
        except Exception:  # Catch possible database errors, or bad formatting, etc
            import traceback
            traceback.print_exc()
            msg = "Error in retrieving prayer. It may have been deleted and the server has not yet synchronized."
        return msg