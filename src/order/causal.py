from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from src.parsing.parser import read_configs_from


counter = 0


def local_time():
    """:returns: a concatenation of strings stating the logical and physical times for a process."""
    process_info = 'Process {}\n'.format(getpid())
    logical_time = '> Logical time = {}u\n'.format(counter)
    physical_time = '> Physical time = {}ms'.format(datetime.now())
    return process_info + logical_time + physical_time


def update_time_according_to(time_stamp):
    """Upon receiving a message, compares its internal clock with the sender's :param timestamp
    and :returns the biggest value between both.
    :return:
    """
    return max(time_stamp, counter) + 1


def event(idenfier):
    """Abstract event, as some internal operation only known by the process that executes it.
    Updates its clock."""
    global counter
    counter += 1
    print('Event has happened in {}! Time = {}u\n'.format(idenfier, counter))


def send(content, pipe: Pipe, identifier):
    """Sends :param content through a :param pipe for another process. Its identifier
    is appended in order to be easier to observe which process sent the message. Updates
    the internal clock."""
    global counter
    counter += 1

    pipe.send((content, identifier, counter))

    print('Message \'{}\' from {}! Time: {}\n'.format(content, identifier, counter))


def receive(pipe, identifier):
    """Receives a message through a :param pipe. Updates the internal clock.

    :param pipe:
    :param identifier:
    """
    message, sender_pid, timestamp = pipe.recv()

    global counter
    counter = update_time_according_to(timestamp)

    print('\'{}\' from {} to {}! Time: {}\n'.format(message, sender_pid, identifier, counter))
    return

# !!!


def process_one(pipe12, pipe13, identifier):
    event(identifier)
    send('Hello!', pipe12, identifier)
    event(identifier)
    receive(pipe12, identifier)
    send('Yes.', pipe13, identifier)


def process_two(pipe21, pipe23, identifier):
    receive(pipe23, identifier)
    receive(pipe21, identifier)
    send('A!', pipe21, identifier)


def process_three(pipe32, pipe13, identifier):
    send('Hell yeah!', pipe32, identifier)
    event(identifier)
    receive(pipe13, identifier)


if __name__ == '__main__':
    qtt, pipes, operations = read_configs_from('config.txt')

    one_and_two, two_and_one = pipes[(0, 1)]
    two_and_three, three_and_two = pipes[(1, 2)]
    one_and_three, three_and_one = pipes[(0, 2)]

    process1 = Process(target=process_one,
                       args=(one_and_two, one_and_three, 1))
    process2 = Process(target=process_two,
                       args=(two_and_one, two_and_three, 2))
    process3 = Process(target=process_three,
                       args=(three_and_two, three_and_one, 3))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
