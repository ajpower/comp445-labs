"""Receiver module for the UDP chat.

This handles the acceptance of incoming connections and extracting the data sent
from them.
"""
import datetime
import socket
from udpmessage import Message


def _recvall(sock: socket.socket):
    """Receive all data from the socket until EOF or close and return as a byte
    string.
    """
    BUFFER_SIZE = 8192

    data = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE)
        data += last_buff
        if not last_buff:
            break
    return data


def receiver(port: int):
    """Start the receiver loop to accept incoming connections and extract their
    message.
    
    :param port: Source port.
    """
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.bind(('', port))

    while True:
        data = _recvall(sock)
        message = Message.parse(str(data))

        dt = datetime.datetime.now()
        print('{} [{}]: {}'.format(dt, message.user, message.message))
