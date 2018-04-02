"""Message format between sender and receiver.

Used to build or parse a message to send or a message received.
"""


class Message:
    """Represents a chat message.

    Attributes:
        user (str): User attached to this message.
        command (str): Command for a message.
        message (str): Message payload.
    """

    def __init__(self, response: str):
        """Parse a received string into a message."""
        # TODO Parsing of a received message
        pass

    def __init__(self, user: str, message: str, command: str):
        """Creates a new message."""
        self.user = user
        self.message = message
        self.command = command

    def __str__(self):
        """Return a string representation of the message to transmit."""
        message = "user:{}\ncommand:{}\nmessage:{}\n\n".format(self.user, self.command,
                                        self.message)
        return message
