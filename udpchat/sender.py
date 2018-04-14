"""Sender module for the udp chat

This handles broadcasting data entered on the command line to the network attached receivers.
"""
import socket
from udpmessage import Message
from queue import Queue


def sender(username: str, ip_address: str, port: int):
    """Start the sender loop to handle cmd line input from the user.

    Process user commands and sends the appropriate message through UDP to the ip:port given.

    :param username: Username of the user.
    :param ip_address: Destination Ip Address (Should be a broadcast ip).
    :param port: Destination port
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_addr = (ip_address, port)
    local_addr = ('127.0.0.1', port)

    # Join the server
    join_message = Message(username, 'JOIN')
    client_socket.sendto(str(join_message).encode('UTF-8'), broadcast_addr)

    message_queue = Queue()
    leave = False
    while not leave:
        user_input = input()

        if user_input.casefold().startswith('/leave'.casefold()):
            message_queue.put(Message(username, 'LEAVE'))
            message_queue.put(Message(username, 'QUIT', None, False))
            leave = True
        elif user_input.casefold().startswith('/who'.casefold()):
            message_queue.put(Message(username, 'WHO', None, False))
        else:
            message_queue.put(Message(username, 'TALK', user_input))

        # print("sending {}".format(str(udp_message)))
        while not message_queue.empty():
            message = message_queue.get()
            client_socket.sendto(str(message).encode('UTF-8'), broadcast_addr if message.broadcast else local_addr)
