from multiprocessing import Process
from datetime import datetime


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
