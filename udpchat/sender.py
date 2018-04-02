"""Sender module for the udp chat

This handles broadcasting data entered on the command line to the network attached receivers.
"""
import socket
from udpmessage import Message


def sender(username: str, ip_address: str, port: int):
    """Start the sender loop to handle cmd line input from the user.

    Process user commands and sends the appropriate message through UDP to the ip:port given.

    :param username: Username of the user.
    :param ip_address: Destination Ip Address (Should be a broadcast ip).
    :param port: Destination port
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    addr = (ip_address, port)

    # Join the server
    join_message = Message(username, 'JOIN')
    client_socket.sendto(str(join_message).encode('UTF-8'), addr)

    leave = False
    while not leave:
        user_input = input()

        if user_input.casefold().startswith('/leave'.casefold()):
            udp_message = Message(username, 'LEAVE')
            leave = True
        else:
            udp_message = Message(username, 'TALK', user_input)

        client_socket.sendto(str(udp_message).encode('UTF-8'), addr)
