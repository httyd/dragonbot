import socket
import re

class IRCClient:

    def __init__(self, host, port, password, nick, ident, name):

        self.host = host
        self.port = port
        self.password = password
        self.nick = nick
        self.ident = ident
        self.name = name

        self._handlers = {}

        self._socket = socket.socket()
        self._buffer = ""


    def send(self, *args):

        self._socket.send((" ".join(args) + "\r\n").encode())


    def handler(self, command, function):

        try:
            
            self._handlers[command].add(function)

        except:

            self._handlers[command] = set()
            self._handlers[command].add(function)


    def start(self):

        self._socket.connect((self.host, self.port))

        self.send("PASS", self.password)
        self.send("NICK", self.nick)
        self.send("USER", self.ident, self.host, "*", ":" + self.name)

        self.loop()


    def loop(self):

        while True:

            self._buffer += (self._socket.recv(1024)).decode()
            lines = self._buffer.split("\n")
            self._buffer = lines.pop()

            for line in lines:

                split = line.strip().split()

                if split[0] == "PING":

                    self.send("PONG", split[1])

                else:

                    parsed = Line(line.strip())

                    if self.nick != parsed.nick and parsed.command in self._handlers:
                        for handler in self._handlers[parsed.command]:
                            handler(self, parsed)

class Line:

    def __init__(self, raw):

        pattern = re.compile("^:(.*?)!.*?@[^\s]*? (.*?)(?: :(.*))$")
        match = pattern.match(str(raw))

        self.nick = None
        self.command = None
        self.parameters = None

        if match:

            groups = match.groups()
            self.nick = groups[0]

            args = groups[1].split()
            self.command = args[0]
            self.parameters = args[1:]

            if len(groups) == 3:
                self.parameters.append(groups[2])
