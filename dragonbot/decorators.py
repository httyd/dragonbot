import shlex
import re

class decorator:

    """Basic template decorator that has useful built-in checks for correct
    channel and admin users. Should not be used in actual skills."""

    def __init__(self):

        pass


    def is_channel(self, channel):

        return self.channel == None or self.channel == channel


    def is_admin(self, admin):

        return self.admin == None or self.admin == admin


    def is_dev(self, dev):

        return self.dev == None or self.dev == dev


class command(decorator):
    
    """Decorator that treats the bot as a mini shell, allowing the user to
    specify a multi-word command and word-split arguments."""

    def __init__(self, keyphrase, channel = None, admin = None, dev = None):

        self.keyphrase = shlex.split(keyphrase)
        self.channel = channel
        self.admin = admin
        self.dev = dev


    def __call__(self, action):

        def result(obj, message):

            try:

                args = shlex.split(message.body)

            except:

                return

            bot = args.pop(0).lower()
            if args[:len(self.keyphrase)] == self.keyphrase \
                    and bot == message.bot.nick().lower() + "," \
                    and self.is_channel(message.channel) \
                    and self.is_admin(message.admin) \
                    and self.is_dev(message.dev):

                action(obj, message, args[len(self.keyphrase):])

        return result


class match(decorator):

    """Decorator that searches for a regular expression pattern and returns to
    the user its named capturing groups as arguments to the decorated method."""

    def __init__(self, regex, channel = None, admin = None, dev = None):

        self.pattern = re.compile(regex)
        self.channel = channel
        self.admin = admin
        self.dev = dev


    def __call__(self, action):

        def result(obj, message):

            match = self.pattern.search(message.body)

            if match and self.is_channel(message.channel) \
                    and self.is_admin(message.admin) \
                    and self.is_dev(message.dev):

                action(obj, message, **match.groupdict())

        return result
