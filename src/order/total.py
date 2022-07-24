from multiprocessing import Process
from datetime import datetime


class TotalWorker:

    def __init__(self, serial, process_qtt):
        self.counters = [0 for _ in range(process_qtt)]
        self.serial = serial

    @staticmethod
    def process(target, args):
        return Process(target=target, args=args)

    def local_time(self):
        """:returns: a concatenation of strings stating the logical and physical times for a process."""
        process_info = 'Process {}\n'.format(self.serial)
        logical_time = '> Logical time = {}\n'.format(self.counters)
        physical_time = '> Physical time = {}ms'.format(datetime.now())
        return process_info + logical_time + physical_time

    def sync_time_to(self, timestamps: list):
        for i, _ in enumerate(self.counters):
            self.counters[i] = max(self.counters[i], timestamps[i])

            if i == self.serial:
                self.counters[i] += 1

        return self.counters

    def event(self):
        """Abstract event, as some internal operation only known by the process that executes it.
        Updates its clock."""
        self.counters[self.serial] += 1
        print('Event has happened in {}! Time = {}\n'.format(self.serial + 1, self.counters))

    def broadcast(self, content, pipes):
        self.counters[self.serial] += 1

        for pipe in pipes:
            pipe.send((content, self.serial, self.counters))

        print('Message \'{}\' from {}! Time: {}\n'.format(content, self.serial + 1, self.counters))

    def deliver(self, pipe):
        """Receives a message through a :param pipe. Updates the internal clock."""
        message, sender_pid, timestamp = pipe.recv()

        self.counters = self.sync_time_to(timestamp)

        print('\'{}\' from {} to {}! Time: {}\n'.format(message, sender_pid + 1, self.serial + 1, self.counters))
        return


class WorkerPool:

    def __init__(self, process_qtt):
        self.process_qtt = process_qtt
        self.workers = [TotalWorker(i, self.process_qtt) for i in range(self.process_qtt)]
