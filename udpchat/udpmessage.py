"""Message format between sender and receiver.

Used to build or parse a message to send or a message received.
"""


class Message:
    """Represents a chat message.

    Attributes:
        user (str): User attached to this message.
        command (str): Command for a message.
        message (str): Message payload.
        args (str): Command arguments (Default None)
        dest (str): Ip Address to send this message.
    """

    def __init__(self, user: str, command: str, message: str = '', args: str = None, dest: str = None):
        """Creates a new message."""
        self.user = user
        self.message = message
        self.command = command
        self.args = args
        self.dest = dest

    def __str__(self):
        """Return a string representation of the message to transmit."""
        message = "user:{}\ncommand:{}\nargs:{}\nmessage:{}\n\n".format(
            self.user, self.command, self.args, self.message)
        return message

    @staticmethod
    def parse(message: str):
        """Parse the input string and return a Message instance."""
        parts = message.split('\n', maxsplit=4)
        user = parts[0][len('user:'):]
        command = parts[1][len('command:'):]
        args = parts[2][len('args:'):]
        message = parts[3][len('message:'):]
        return Message(user, command, message, args)
