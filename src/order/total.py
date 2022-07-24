from multiprocessing import Process, Pipe
from src.patterns.decorators import *


class TotalWorker:

    def __init__(self, serial, process_qtt, pipes):
        self.counter = [0 for _ in range(process_qtt)]
        self.serial = serial
        self.pipes = pipes

    @staticmethod
    def process(target, args):
        return Process(target=target, args=args)

    def sync_time_to(self, timestamps: list):
        """Upon receiving a message, compares its internal clock with the sender's :param timestamps
        and :returns the biggest values from both lists. Updates its internal clock."""
        for i, _ in enumerate(self.counter):
            self.counter[i] = max(self.counter[i], timestamps[i])

            if i == self.serial:
                self.counter[i] += 1

        return self.counter

    @notify_event
    def event(self):
        """Abstract event, as some internal operation only known by the process that executes it.
        Updates its clock."""
        self.counter[self.serial] += 1

    @notify_send
    def send(self, content, pipe):
        """Sends :param content through a :param pipe for another process. Its identifier
        is appended in order to be easier to observe which process sent the message. Updates
        the counter at its own serial position."""
        self.counter[self.serial] += 1
        pipe.send((content, self.serial, self.counter))

    def broadcast(self, content):
        """Sends the :param content through all accessible pipes."""
        self.counter[self.serial] += 1

        for pipe in self.pipes:
            if pipe:
                pipe.send((content, self.serial, self.counter))

    @notify_arrival
    def deliver(self, pipe):
        """Receives a message through a :param pipe. Updates the internal clock."""
        message, sender_pid, timestamp = pipe.recv()
        self.counter = self.sync_time_to(timestamp)

        return message, sender_pid


class WorkerPool:

    def __init__(self, process_qtt):
        self.process_qtt = process_qtt
        pipes = WorkerPool.pipes_for(self.process_qtt)
        self.workers = [TotalWorker(i, self.process_qtt, pipes[i]) for i in range(self.process_qtt)]
        self.processes = [Process() for _ in range(self.process_qtt)]

    def __getitem__(self, index):
        """Overrides [] operator, hence pool.workers[index] <=> pool[index]."""
        return self.workers[index]

    @staticmethod
    def pipes_for(process_qtt):
        """Creates a squared-matrix according to :param process_qtt to store processes pipes.
        If the line index is the same as the column, None is put instead, as a process should not
        be connected to itself."""
        pipes = [[None for _ in range(process_qtt)] for _ in range(process_qtt)]

        for i in range(process_qtt):
            for j in range(process_qtt):
                if i != j:
                    pipes[i][j], pipes[j][i] = Pipe()

        return pipes

    def start(self):
        [process.start() for process in self.processes]

    def join(self):
        [process.join() for process in self.processes]


if __name__ == '__main__':
    print(WorkerPool.pipes_for(3))
