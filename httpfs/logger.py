"""Logging library"""

from threading import Thread
from queue import Queue
import sys


log_queue = None
log_verbose = False


def set_logger(verbose: bool = True):
    global log_queue, log_verbose
    log_verbose = verbose

    if not log_queue:
        log_thread = LogThread(sys.stdout)
        log_thread.setDaemon(True)
        log_thread.start()
        log_queue = log_thread.queue


def write(msg: str):
    if not log_queue:
        set_logger()
    if log_verbose:
        log_queue.put(msg)


class LogThread(Thread):
    def __init__(self, log_destination):
        super().__init__()
        self.log_destination = log_destination
        self.queue = Queue()

    def run(self):
        while True:
            self.log_destination.write(str(self.queue.get()) + '\n')
            self.log_destination.flush()
            self.queue.task_done()
