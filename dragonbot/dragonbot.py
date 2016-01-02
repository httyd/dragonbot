import sleekxmpp
import datetime
import time
import os

from .skills import load_skills, save_skills, run_skills
from .util import Message, Room

class DragonBot:

    def __init__(self):

        """Initialize default values for the bot."""

        self._jabber_id = None
        self._jabber_password = None
        self._jabber_port = 5222
        self._jabber_rooms = {}

        self._name = "DragonBot"
        self._admins = {}
        self._skills = {}
        self._data = None

        self._test_mode = False


    def jabber_id(self, jid):

        """Set the Jabber ID, including the domain."""

        self._jabber_id = jid


    def jabber_password(self, password):

        """Set the Jabber password."""

        self._jabber_password = password

    
    def jabber_port(self, port):

        """Set the Jabber port, with 5222 as default."""

        self._jabber_port = port


    def jabber_rooms(self, rooms):

        """Provide a dictionary of rooms with the keys being the human-readable
        room name and the value being the Jabber address."""

        self._jabber_rooms = rooms


    def jabber_room_names(self):

        """Provide a list of room names."""

        return self._jabber_rooms.keys()


    def jabber_room_id(self, name):

        """Provide a Jabber address for a given room name."""

        return self._jabber_rooms[name]


    def set_name(self, name):

        """Set the name of the bot, which is DragonBot by default."""

        self._name = name


    def name(self):

        """Receive the name of the bot."""

        return self._name


    def admins(self, admin_list):

        """Set the list of admin users by accepting an iterable collection of
        username nick strings for each admin user."""

        self._admins = admin_list


    def skills(self, skill_directory, data_file):

        """Set the skills for the bot by accepting a skill directory, where the
        actual skill python code is stored, and a data file where the plugin
        data are stored to maintain state across reloads."""

        self._data = data_file
        self._skills = load_skills(self, skill_directory, data_file)


    def is_admin(self, user):

        """Check if a user is an admin."""

        return user in self._admins


    def _receive(self, message):

        """Provide a message for the bot to parse and run using its skills."""

        run_skills(self._skills, message)
        save_skills(self, self._skills, self._data)


    def send(self, room, text):

        """Send a message, either in test mode using the REPL or in Jabber mode
        using the Jabber client."""

        if self._test_mode:

            print(text)

        else:

            self._client.send_message(mto = room.room_id,
                    mbody = text, mtype = "groupchat")

    
    def start_shell(self):

        """Start the DragonBot REPL."""

        self._test_mode = True
        nick = input("Your Nick: ")
        room = Room("Dragon Shell", "dragon_shell")

        while True:

            try:

                body = input("> ")
                time = datetime.datetime.now()

                message = Message(self, nick, room, time, body)

                self._receive(message)

            except EOFError:

                print()
                break


    def start_client(self):

        """Start the Jabber client."""

        self._client = sleekxmpp.ClientXMPP(self._jabber_id, self._jabber_password)
        self._client.register_plugin("xep_0045")

        self._client.add_event_handler("session_start", self._client_startup)
        self._client.add_event_handler("groupchat_message", self._client_receive)

        self._client.connect()
        self._client.process(threaded = True)


    def _client_startup(self, event):

        """Set up the Jabber client, join each room."""

        self._client.get_roster()
        self._client.send_presence()

        for room in self._jabber_rooms.values():
            self._client.plugin["xep_0045"].joinMUC(room, self.name(), wait = True)


    def _client_receive(self, msg):

        """Receive and parse message from the Jabber client."""

        time = datetime.datetime.fromtimestamp(float(msg.xml.attrib["ts"]))
        now = datetime.datetime.now()
        nick = msg["mucnick"]

        if now - time > datetime.timedelta(seconds = 5) or nick == self._name:
            return

        room_id = msg["mucroom"]
        room_name = list(self._jabber_rooms.keys())[list(self._jabber_rooms.values()).index(room_id)]
        room = Room(room_name, room_id)
        body = msg["body"]

        message = Message(self, nick, room, time, body)
        self._receive(message)


    def __getstate__(self):

        """Prevent pickling the bot."""

        return {}


    def __setstate__(self, d):

        """Prevent restoring the bot from pickle."""

        return
