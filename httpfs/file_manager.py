"""File Server Manager - Cheap Thread safety

TODO Add Thread Safety at file level
Thread safety is handled at the directory level:
    Only one thread can write to any file in the directory at a time
    Multiple read can be active at a time.
    Writer Priority
"""

import os
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
    return [
        f for f in os.listdir(file_manager_directory)
        if os.path.isfile("/".join(file_manager_directory, f))
    ]


def get_file(filename: str):
    """Retrieve the data from a file
    Only files in the directory can be retrieved, no sub-folders.
    Throws an error if the file is a directory or a subdirectory exists

    :param filename: File name
    :return: (bytes) Data of the file
    """
    # Print contents of root directory if filename is "/".
    if filename == '/':
        files = os.listdir('/')
        return files.join('\n')

    # Do not continue if there's a directory or the name isn't a file
    if os.path.dirname(filename) or not os.path.isfile(filename):
        raise ValueError("Invalid filename")

    file_manager_lock.read_acquire()
    # print('acquired read lock' + filename)
    with open(filename, mode='r') as f:
        return f.read()

    # print('releasing read lock' + filename)
    file_manager_lock.read_release()


def write_file(filename: str, data: str):
    """Writes the data to the given file
    :param filename: File name
    :param data: (str) Data to write, txt only.
    """
    if os.path.dirname(filename):
        raise ValueError("Filename specifies an existing directory.")
    file_manager_lock.write_acquire()
    # print('acquired write lock' + filename)
    with open(filename, mode='w') as f:
        f.write(data)
    # print('releasing write lock' + filename)
    file_manager_lock.write_release()
