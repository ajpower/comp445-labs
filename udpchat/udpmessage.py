"""Message format between sender and receiver.

Used to build or parse a message to send or a message received.
"""


class Message:
    """Represents a chat message.

    Attributes:
        user (str): User attached to this message.
        command (str): Command for a message.
        message (str): Message payload.
        broadcast (bool): True if this is intended for broadcast (Default True)
    """

    def __init__(self, user: str, command: str, message: str = '', broadcast: bool = True):
        """Creates a new message."""
        self.user = user
        self.message = message
        self.command = command
        self.broadcast = broadcast

    def __str__(self):
        """Return a string representation of the message to transmit."""
        message = "user:{}\ncommand:{}\nmessage:{}\n\n".format(
            self.user, self.command, self.message)
        return message

    @staticmethod
    def parse(message: str):
        """Parse the input string and return a Message instance."""
        parts = message.split('\n', maxsplit=3)
        user = parts[0][len('user:'):]
        command = parts[1][len('command:'):]
        message = parts[2][len('message:'):]
        return Message(user, command, message)
