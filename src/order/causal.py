from multiprocessing import Process
from datetime import datetime
from src.parsing.parser import read_configs_from


class PartialWorker:

    def __init__(self, serial_id):
        self.serial = serial_id
        self.counter = 0

    @staticmethod
    def process(target, args):
        return Process(target=target, args=args)

    def local_time(self):
        """:returns: a concatenation of strings stating the logical and physical times for a process."""
        process_info = 'Process {}\n'.format(self.serial)
        logical_time = '> Logical time = {}\n'.format(self.counter)
        physical_time = '> Physical time = {}ms'.format(datetime.now())
        return process_info + logical_time + physical_time

    def sync_time_to(self, time_stamp):
        """Upon receiving a message, compares its internal clock with the sender's :param timestamp
        and :returns the biggest value between both."""
        return max(time_stamp, self.counter) + 1

    def event(self):
        """Abstract event, as some internal operation only known by the process that executes it.
        Updates its clock."""
        self.counter += 1
        print('Event has happened in {}! Time = {}u\n'.format(self.serial, self.counter))

    def send(self, content, pipe):
        """Sends :param content through a :param pipe for another process. Its identifier
        is appended in order to be easier to observe which process sent the message. Updates
        the internal clock."""
        self.counter += 1

        pipe.send((content, self.serial, self.counter))

        print('Message \'{}\' from {}! Time: {}\n'.format(content, self.serial, self.counter))

    def receive(self, pipe):
        """Receives a message through a :param pipe. Updates the internal clock."""
        message, sender_pid, timestamp = pipe.recv()

        self.counter = self.sync_time_to(timestamp)

        print('\'{}\' from {} to {}! Time: {}\n'.format(message, sender_pid, self.serial, self.counter))
        return

    def process_one(self, pipe12, pipe13):
        self.event()
        self.send('Hello!', pipe12)
        self.event()
        self.receive(pipe12)
        self.send('Yes.', pipe13)
        return

    def process_two(self, pipe21, pipe23):
        self.receive(pipe23)
        self.receive(pipe21)
        self.send('A!', pipe21)
        return

    def process_three(self, pipe32, pipe31):
        self.send('Hell yeah!', pipe32)
        self.event()
        self.receive(pipe31)
        return


if __name__ == '__main__':
    qtt, pipes = read_configs_from('config.txt')

    one_and_two, two_and_one = pipes[(0, 1)]
    two_and_three, three_and_two = pipes[(1, 2)]
    one_and_three, three_and_one = pipes[(0, 2)]

    worker1 = PartialWorker(0)
    worker2 = PartialWorker(1)
    worker3 = PartialWorker(2)

    process1 = worker1.process(target=worker1.process_one, args=(one_and_two, one_and_three))
    process2 = worker2.process(target=worker2.process_two, args=(two_and_one, two_and_three))
    process3 = worker3.process(target=worker3.process_three, args=(three_and_two, three_and_one))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
