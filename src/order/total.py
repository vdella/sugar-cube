from multiprocessing import Process
from src.patterns.decorators import *


class TotalWorker:

    def __init__(self, serial, process_qtt):
        self.counter = [0 for _ in range(process_qtt)]
        self.serial = serial

    @staticmethod
    def process(target, args):
        return Process(target=target, args=args)

    def sync_time_to(self, timestamps: list):
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
    def send(self, content, pipes):
        self.counter[self.serial] += 1

        for pipe in pipes:
            pipe.send((content, self.serial, self.counter))

    @notify_message_arrival
    def deliver(self, pipe):
        """Receives a message through a :param pipe. Updates the internal clock."""
        message, sender_pid, timestamp = pipe.recv()
        self.counter = self.sync_time_to(timestamp)

        return message, sender_pid


class WorkerPool:

    def __init__(self, process_qtt):
        self.process_qtt = process_qtt
        self.workers = [TotalWorker(i, self.process_qtt) for i in range(self.process_qtt)]
