import shlex
import re

class decorator:

    """Basic template decorator that has useful built-in checks for correct room
    and admin users. Should not be used in actual skills."""

    def __init__(self):

        pass


    def correct_room(self, room):

        return self.room == None or self.room == room.name


    def correct_user_type(self, admin):

        return self.admin == None or self.admin == admin


class command(decorator):
    
    """Decorator that treats the bot as a mini shell, allowing the user to
    specify a multi-word command and word-split arguments."""

    def __init__(self, keyphrase, room = None, admin = None):

        self.keyphrase = shlex.split(keyphrase)
        self.room = room
        self.admin = admin


    def __call__(self, action):

        def result(obj, message):

            try:

                args = shlex.split(message.body)

            except:

                return

            bot = args.pop(0).lower()
            if args[:len(self.keyphrase)] == self.keyphrase \
                    and bot == "@" + message.bot.name().lower() \
                    and self.correct_room(message.room) \
                    and self.correct_user_type(message.admin):

                action(obj, message, args[len(self.keyphrase):])

        return result


class match(decorator):

    """Decorator that searches for a regular expression pattern and returns to
    the user its named capturing groups as arguments to the decorated method."""

    def __init__(self, regex, room = None, admin = None):

        self.pattern = re.compile(regex)
        self.room = room
        self.admin = admin


    def __call__(self, action):

        def result(obj, message):

            match = self.pattern.search(message.body)

            if match and self.correct_room(message.room) \
                    and self.correct_user_type(message.admin):

                action(obj, message, **match.groupdict())

        return result
