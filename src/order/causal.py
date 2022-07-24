from multiprocessing import Process
from src.patterns.decorators import *


class PartialWorker:

    def __init__(self, serial_id):
        self.serial = serial_id
        self.counter = 0

    @staticmethod
    def process(target, args):
        return Process(target=target, args=args)

    def sync_time_to(self, time_stamp):
        """Upon receiving a message, compares its internal clock with the sender's :param timestamp
        and :returns the biggest value between both. Updates its internal clock."""
        return max(time_stamp, self.counter) + 1

    @notify_event
    def event(self):
        """Abstract event, as some internal operation only known by the process that executes it.
        Updates its clock."""
        self.counter += 1

    @notify_send
    def send(self, content, pipe):
        """Sends :param content through a :param pipe for another process. Its identifier
        is appended in order to be easier to observe which process sent the message. Updates
        the internal clock."""
        self.counter += 1
        pipe.send((content, self.serial, self.counter))

    @notify_arrival
    def receive(self, pipe):
        """Receives a message through a :param pipe. Updates the internal clock."""
        message, sender_pid, timestamp = pipe.recv()
        self.counter = self.sync_time_to(timestamp)

        return message, sender_pid
