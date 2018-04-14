"""TODO"""
from threading import Thread
from receiver import receiver
from sender import sender
import time

username = input('Enter your name:')
receiveThread = Thread(target=receiver, kwargs={'port': 8000, 'username' : username, 'broadcast_ip' : '255.255.255.255'})
receiveThread.start()
time.sleep(1) # Just make sure the receiver is listening before starting to send
sender(username=username, ip_address='255.255.255.255', port=8000)
