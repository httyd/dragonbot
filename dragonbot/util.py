class Message:

    """Message date structure for bot and skill plugins."""

    def __init__(self, bot, nick, room, time, body):

        """Initialize a message object from Jabber message parameters."""

        self.bot = bot
        self.nick = nick
        self.room = room
        self.time = time
        self.body = body

        self.admin = bot.is_admin(nick)


    def reply(self, body):

        """Reply to a message by sending a new message containing a specified
        string to the room of the message."""

        self.bot.send(self.room, body)


    def __repr__(self):

        """Return a useful timestamp representation of the message."""

        return self.nick + " [" + str(self.time) + "]" + ": " + self.body


    def __str__(self):

        """Return the timestamp representation of the message."""

        return self.__repr__()


class Room:

    """Room data structure for bot and skill plugins."""

    def __init__(self, name, room_id):

        self.name = name
        self.room_id = room_id
