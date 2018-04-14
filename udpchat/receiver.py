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
        last_buff = sock.recv(BUFFER_SIZE, socket.MSG_WAITALL)
        data += last_buff
        if len(last_buff) < BUFFER_SIZE:
            break
    return data


def receiver(username: str, port: int, broadcast_ip: str, connected_users: dict):
    """Start the receiver loop to accept incoming connections and extract their
    message.

    :param username: Username of this peer
    :param port: Source port.
    :param broadcast_ip: Address for broadcast of PING
    :param connected_users: Dict of users to ip
    """
    hostname = socket.gethostbyname(socket.gethostname())

    server_sock = socket.socket(type=socket.SOCK_DGRAM)
    server_sock.bind(('', port))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_addr = (broadcast_ip, port)

    while True:
        data = _recvall(server_sock)
        message = Message.parse(data.decode('UTF-8'))
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if message.command == 'JOIN':
            connected_users[message.user] = message.args
            print('{} {} joined!'.format(dt, message.user))
            client_socket.sendto(str(Message(user=username, command='PING', args=hostname)).encode('UTF-8'),
                                 broadcast_addr)
        elif message.command == 'LEAVE':
            if message.user in connected_users:
                del connected_users[message.user]
            print('{} {} left!'.format(dt, message.user))
        elif message.command == 'TALK':
            print('{} [{}]: {}'.format(dt, message.user, message.message))
        elif message.command == 'PRIVATE-TALK':
            print('{} [{}] (PRIVATE): {}'.format(dt, message.user, message.message))
        elif message.command == 'WHO':
            print('{} Connected users: {}'.format(dt, list(connected_users.keys())))
        elif message.command == 'QUIT':
            break
        elif message.command == 'PING':
            connected_users[message.user] = message.args

    print('Bye now!')
