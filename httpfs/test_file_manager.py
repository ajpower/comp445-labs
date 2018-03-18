from file_manager import get_file, write_file
from threading import Thread


t_count = 0

def get_increment():
    global t_count
    t_count += 1
    return t_count

def test_threads():
    global t_count
    threads = []
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=writer, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))
    threads.append(Thread(target=reader, args=(get_increment(),)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


def reader(name):
    get_file(str(name))


def writer(name):
    write_file(str(name), "mooooooo")


test_threads()
