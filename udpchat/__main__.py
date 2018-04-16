"""TODO"""
import argparse
from threading import Thread
from receiver import receiver
from sender import sender
import time

DEFAULT_PORT = 8000
DEFAULT_BROADCAST_IP = '255.255.255.255'

parser = argparse.ArgumentParser(
    description='udpchat is a simple local network chat based on broadcasted udp datagrams.')

parser.add_argument(
    '-p',
    dest='port',
    type=int,
    help=(
        'Specifies the port number that the chat will listen and send at. '
        'Default is {}.'.format(DEFAULT_PORT)),
    default=DEFAULT_PORT,
    metavar='PORT')
parser.add_argument(
    '-d',
    dest='dest',
    help=
    ('Specifies the broadcast ip address. '
     'Default is the local subnetwork {}.'.format(DEFAULT_BROADCAST_IP)
     ),
    default=DEFAULT_BROADCAST_IP,
    metavar='BROADCAST-IP')

args = parser.parse_args()

username = input('Enter your name:')

receiveThread = Thread(target=receiver, kwargs={'port': args.port, 'username': username, 'broadcast_ip': args.dest})
receiveThread.start()
time.sleep(1)  # Make sure the receiver is listening before starting to send
sender(username=username, ip_address=args.dest, port=args.port)
