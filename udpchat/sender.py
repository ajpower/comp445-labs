"""Sender module for the udp chat

This handles broadcasting data entered on the command line to the network attached receivers.
"""
import socket
from udpmessage import Message
from queue import Queue
from receiver import chat_context


def sender(username: str, ip_address: str, port: int):
    """Start the sender loop to handle cmd line input from the user.

    Process user commands and sends the appropriate message through UDP to the ip:port given.

    :param username: Username of the user.
    :param ip_address: Destination Ip Address (Should be a broadcast ip).
    :param port: Destination port
    """
    hostname = socket.gethostbyname(socket.gethostname())

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_addr = ip_address
    local_addr = '127.0.0.1'

    # Join the server
    join_message = Message(user=username, command='JOIN', channel=chat_context['channel'], args=hostname,
                           dest=broadcast_addr)
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
            if peer_name in chat_context['users']:
                message_queue.put(get_pm(from_user=username, to_user=peer_name))
            else:
                print('Invalid Username: use /who to see connected users')

        elif user_input.casefold().startswith('/channel'.casefold()):
            parts = user_input.split(maxsplit=2)
            if len(parts) < 2:
                print('You must select a channel to join /channel <name>')
            else:
                channel = parts[1]
                message_queue.put(Message(user=username, command='CHANNEL', channel=channel, dest=local_addr))

        else:
            message_queue.put(
                Message(user=username, command='TALK', channel=chat_context['channel'], message=user_input,
                        dest=broadcast_addr))

        # print("sending {}".format(str(udp_message)))
        while not message_queue.empty():
            message = message_queue.get()
            client_socket.sendto(str(message).encode('UTF-8'), (message.dest, port))


def get_pm(from_user: str, to_user: str):
    user_input = input('Private message to {}: '.format(to_user))
    return Message(user=from_user, command='PRIVATE-TALK', message=user_input, dest=chat_context['users'][to_user])
