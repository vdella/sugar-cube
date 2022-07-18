from multiprocessing import Process
from datetime import datetime
from src.parsing.parser import read_configs_from


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

    def process_one(self, pipe12, pipe13):
        self.event()
        self.broadcast('Hello!', [pipe12])
        self.event()
        self.deliver(pipe12)
        self.broadcast('Yes.', [pipe13])

    def process_two(self, pipe21, pipe23):
        self.deliver(pipe23)
        self.deliver(pipe21)
        self.broadcast('A!', [pipe21])

    def process_three(self, pipe32, pipe13):
        self.broadcast('Hell yeah!', [pipe32])
        self.event()
        self.deliver(pipe13)


if __name__ == '__main__':
    qtt, pipes = read_configs_from('config.txt')

    one_and_two, two_and_one = pipes[(0, 1)]
    two_and_three, three_and_two = pipes[(1, 2)]
    one_and_three, three_and_one = pipes[(0, 2)]

    worker1 = TotalWorker(0, 3)
    worker2 = TotalWorker(1, 3)
    worker3 = TotalWorker(2, 3)

    process1 = worker1.process(target=worker1.process_one, args=(one_and_two, one_and_three))
    process2 = worker2.process(target=worker2.process_two, args=(two_and_one, two_and_three))
    process3 = worker3.process(target=worker3.process_three, args=(three_and_two, three_and_one))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()



