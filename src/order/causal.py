from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from src.parsing.parser import read_configs_from


counter = 0


def local_time():
    process_info = 'Process {}\n'.format(getpid())
    logical_time = '> Logical time = {}u\n'.format(counter)
    physical_time = '> Physical time = {}ms'.format(datetime.now())
    return process_info + logical_time + physical_time


def update_time_according_to(time_stamp):
    return max(time_stamp, counter) + 1


def event(idenfier):
    global counter
    counter += 1
    print('Event has happened in {}! Time = {}u'.format(idenfier, counter))


def send(content, pipe: Pipe, identifier):
    global counter
    counter += 1

    pipe.send((identifier, counter))

    print('Message from {}! Time: {}\n'.format(identifier, counter))
    return


# TODO fix logical time. Communication works.

def receive(pipe, identifier):
    message, timestamp = pipe.recv()

    global counter
    counter = update_time_according_to(timestamp)

    print('{} to {}! Time: {}\n'.format(message, identifier, counter))
    return

# !!!


def process_one(pipe12, pipe13, identifier):
    pid = identifier
    event(identifier)
    send('Hello!', pipe12, identifier)
    event(identifier)
    receive(pipe12, identifier)
    send('Yes.', pipe13, identifier)


def process_two(pipe21, pipe23, identifier):
    pid = identifier
    receive(pipe23, identifier)
    receive(pipe21, identifier)
    send('A!', pipe21, identifier)


def process_three(pipe32, pipe13, identifier):
    pid = identifier

    send('Hell yeah!', pipe32, identifier)
    event(identifier)
    receive(pipe13, identifier)


if __name__ == '__main__':
    qtt, pipes = read_configs_from('config.txt')

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
