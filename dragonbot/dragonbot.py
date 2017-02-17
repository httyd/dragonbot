import datetime
import time
import os

from .ircclient import IRCClient
from .skills import load_skills, save_skills, run_skills
from .message import Message

class DragonBot:

    def __init__(self):

        """Initialize default values for the bot."""

        self._host = None
        self._port = None
        self._password = None
        self._nick = "DragonBot"

        self._admins = {}
        self._devs = {}
        self._skills = {}
        self._data = None

        self._test_mode = False


    def setup(self, host, port = 6667, password = "", nick = "DragonBot"):

        """Set the server host, port, password, and nick."""

        self._host = host
        self._port = port
        self._password = password
        self._nick = nick


    def nick(self):

        """Get the nick."""

        return self._nick


    def admins(self, admin_list):

        """Set the list of admin users by accepting an iterable collection of
        username nick strings for each admin user."""

        self._admins = admin_list


    def devs(self, dev_list):

        """Set the list of dev users by accepting an iterable collection of
        username nick strings for each dev user."""

        self._devs = dev_list


    def skills(self, skill_directory, data_file):

        """Set the skills for the bot by accepting a skill directory, where the
        actual skill python code is stored, and a data file where the plugin
        data are stored to maintain state across reloads."""

        self._data = data_file
        self._skills = load_skills(self, skill_directory, data_file)


    def is_admin(self, user):

        """Check if a user is an admin."""

        return user in self._admins


    def is_dev(self, user):

        """Check if a user is a dev."""

        return user in self._devs


    def _receive(self, message):

        """Provide a message for the bot to parse and run using its skills."""

        run_skills(self._skills, message)
        save_skills(self, self._skills, self._data)


    def send(self, channel, text):

        """Send a message, either in test mode using the REPL or in IRC mode
        using the IRC client."""

        if self._test_mode:

            print(text)

        else:

            self._client.send("PRIVMSG", channel, str(text))


    def action(self, channel, text):

        """Send a message, either in test mode using the REPL or in IRC mode
        using the IRC client."""

        if self._test_mode:

            print(self.nick(), text)

        else:

            self._client.send("PRIVMSG", channel,
                              "\x01ACTION "  + str(text) + "\x01")

    
    def start_shell(self):

        """Start the DragonBot REPL."""

        self._test_mode = True
        nick = input("Your Nick: ")
        channel = "#repl"

        while True:

            try:

                body = input("> ")
                time = datetime.datetime.now()

                message = Message(self, channel, nick, time, body)

                self._receive(message)

            except EOFError:

                print()
                break


    def start_client(self):

        """Start the IRC client."""

        self._client = IRCClient(self._host,
                           self._port,
                           self._password,
                           self._nick,
                           self._nick,
                           self._nick)

        self._client.handler("PRIVMSG", self._client_receive)
        self._client.start()


    def _client_receive(self, client, line):

        """Receive and parse message from the IRC client."""

        nick = line.nick
        channel = line.parameters[0]
        time = datetime.datetime.now()
        body = line.parameters[1]

        message = Message(self, channel, nick, time, body)
        self._receive(message)


    def __getstate__(self):

        """Prevent pickling the bot."""

        return {}


    def __setstate__(self, d):

        """Prevent restoring the bot from pickle."""

        return
