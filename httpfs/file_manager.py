"""File Server Manager - Cheap Thread safety

TODO Add Thread Safety at file level
Thread safety is handled at the directory level:
    Only one thread can write to any file in the directory at a time
    Multiple read can be active at a time.
    No Reader/Writer Priority
"""

import os
from queue import Queue
from threading import Lock
from rwlock import FileManagerLock


file_manager_directory = '.'
file_manager_lock = FileManagerLock()


def set_dir(path: str = '.'):
    """Sets the directory for the file manager
    :param path: Path to the directory
    """
    global file_manager_directory
    if os.path.isdir(path):
        file_manager_directory = path
    else:
        raise RuntimeError('The given path is not a directory')


def list_dir():
    """Returns a list of all files in the directory
    :return: List of files in the directory
    """
    return [f for f in os.listdir(file_manager_directory) if os.path.isfile("/".join(file_manager_directory, f))]


def get_file(filename: str):
    """Retrieve the data from a file
    :param filename: File name
    :return: (str) Data of the file
    """
    file_manager_lock.read_acquire()
    print('acquired read lock')
    file_manager_lock.read_release()
    print('released read lock')


def write_file(filename: str, data: str):
    """Writes the data to the given file
    :param filename: File name
    :param data: (str) Data to write, txt only.
    """
    file_manager_lock.write_acquire()
    print('acquired write lock')
    file_manager_lock.write_release()
    print('released write lock')
