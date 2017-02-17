class Message:

    """Message date structure for bot and skill plugins."""

    def __init__(self, bot, channel, nick, time, body):

        """Initialize a message object from Jabber message parameters."""

        self.bot = bot
        self.channel = channel
        self.nick = nick
        self.time = time
        self.body = body

        self.admin = bot.is_admin(nick)
        self.dev = bot.is_dev(nick)


    def reply(self, body):

        """Reply to a message by sending a new message containing a specified
        string to the channel of the message."""

        if self.channel == self.bot.nick():

            self.bot.send(self.nick, body)

        else:

            self.bot.send(self.channel, body)


    def action(self, body):

        """Reply to a message by sending an action message."""

        if self.channel == self.bot.nick():

            self.bot.action(self.nick, body)

        else:

            self.bot.action(self.channel, body)


    def __repr__(self):

        """Return a useful timestamp representation of the message."""

        return self.nick + " [" + str(self.time) + "]" + ": " + self.body


    def __str__(self):

        """Return the timestamp representation of the message."""

        return self.__repr__()
