from multiprocessing import Process
from datetime import datetime
from src.parsing.parser import read_configs_from


def counters_for(process_qtt: int):
    return [0 * process_qtt]


def local_time_for(pid):
    """:returns: a concatenation of strings stating the logical and physical times for a process."""
    process_info = 'Process {}\n'.format(pid)
    logical_time = '> Logical time = {}u\n'.format(counters)
    physical_time = '> Physical time = {}ms'.format(datetime.now())
    return process_info + logical_time + physical_time


def sync_time_to(timestamps: list):
    global counters

    for i, _ in enumerate(counters):
        counters[i] = max(counters[i], timestamps[i])

    return counters


def event(idenfier):
    """Abstract event, as some internal operation only known by the process that executes it.
    Updates its clock."""
    global counters
    counters[idenfier] += 1
    print('Event has happened in {}! Time = {}u\n'.format(idenfier, counters))


def broadcast(content, pipes, identifier):
    global counters
    counters[identifier] += 1

    for pipe in pipes:
        pipe.send((content, identifier, counters))

    print('Message \'{}\' from {}! Time: {}\n'.format(content, identifier, counters))


def deliver(pipe, identifier):
    """Receives a message through a :param pipe. Updates the internal clock."""
    message, sender_pid, timestamp = pipe.recv()

    global counters
    counters = sync_time_to(timestamp)

    print('\'{}\' from {} to {}! Time: {}\n'.format(message, sender_pid, identifier, counters))
    return


# !!!

def process_one(pipe12, pipe13, identifier):
    event(identifier)
    broadcast('Hello!', [pipe12], identifier)
    event(identifier)
    deliver(pipe12, identifier)
    broadcast('Yes.', [pipe13], identifier)


def process_two(pipe21, pipe23, identifier):
    deliver(pipe23, identifier)
    deliver(pipe21, identifier)
    broadcast('A!', [pipe21], identifier)


def process_three(pipe32, pipe13, identifier):
    broadcast('Hell yeah!', [pipe32], identifier)
    event(identifier)
    deliver(pipe13, identifier)


if __name__ == '__main__':
    qtt, pipes, operations = read_configs_from('config.txt')

    counters = counters_for(qtt)

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



