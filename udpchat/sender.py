"""Sender module for the udp chat

This handles broadcasting data entered on the command line to the network attached receivers.
"""
import socket
from udpmessage import Message
from queue import Queue


def sender(username: str, ip_address: str, port: int, connected_users: dict):
    """Start the sender loop to handle cmd line input from the user.

    Process user commands and sends the appropriate message through UDP to the ip:port given.

    :param username: Username of the user.
    :param ip_address: Destination Ip Address (Should be a broadcast ip).
    :param port: Destination port
    :param connected_users: Dictionary of connected username to ip
    """
    hostname = socket.gethostbyname(socket.gethostname())

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_addr = ip_address
    local_addr = '127.0.0.1'

    # Join the server
    join_message = Message(user=username, command='JOIN', args=hostname, dest=broadcast_addr)
    client_socket.sendto(str(join_message).encode('UTF-8'), (join_message.dest, port))

    message_queue = Queue()
    leave = False
    while not leave:
        user_input = input()

        if user_input.casefold().startswith('/leave'.casefold()):
            message_queue.put(Message(user=username, command='LEAVE', dest=broadcast_addr))
            message_queue.put(Message(user=username, command='QUIT', dest=local_addr))
            leave = True

        elif user_input.casefold().startswith('/who'.casefold()):
            message_queue.put(Message(user=username, command='WHO', dest=local_addr))

        elif user_input.casefold().startswith('/private'.casefold()):
            parts = user_input.split(maxsplit=2)
            peer_name = parts[1] if len(parts) >= 2 else None
            if peer_name in connected_users:
                message_queue.put(get_pm(from_user=username, to_user=peer_name, connected_users=connected_users))
            else:
                print('Invalid Username: use /who to see connected users')

        else:
            message_queue.put(Message(user=username, command='TALK', message=user_input, dest=broadcast_addr))

        # print("sending {}".format(str(udp_message)))
        while not message_queue.empty():
            message = message_queue.get()
            client_socket.sendto(str(message).encode('UTF-8'), (message.dest, port))


def get_pm(from_user: str, to_user: str, connected_users: dict):
    user_input = input('Private message to {}: '.format(to_user))
    return Message(user=from_user, command='PRIVATE-TALK', message=user_input, dest=connected_users[to_user])
