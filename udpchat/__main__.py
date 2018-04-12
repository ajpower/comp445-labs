"""TODO"""
from threading import Thread
from receiver import receiver
from sender import sender

receiveThread = Thread(target=receiver, kwargs={'port': 8000})
receiveThread.start()
sender(username='Alex', ip_address='255.255.255.255', port=8000)
