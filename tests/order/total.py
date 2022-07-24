import unittest
from src.order.total import WorkerPool, TotalWorker
from multiprocessing import Array


result1 = Array('i', range(3))
result2 = Array('i', range(3))
result3 = Array('i', range(3))


class TotalOrderTest(unittest.TestCase):

    @staticmethod
    def execute_processes():
        pool = WorkerPool(3)

        targets = [process_one, process_two, process_three]

        for i, worker in enumerate(pool.workers):
            pool.processes[i] = worker.process(target=targets[i], args=(worker,))

        pool.start()
        pool.join()

        return result1, result2, result3

    def test_total_order(self):
        exec_results = self.execute_processes()

        def test_total_order_for_process1():
            self.assertTrue([5, 3, 1], exec_results[0])
        test_total_order_for_process1()

        def test_total_order_for_process2():
            self.assertTrue([2, 3, 1], exec_results[1])
        test_total_order_for_process2()

        def test_total_order_for_process3():
            self.assertTrue([5, 3, 3], exec_results[2])
        test_total_order_for_process3()


def process_one(worker0: TotalWorker):
    worker0.event()
    worker0.send('Hello!', worker0.pipes[1])
    worker0.event()
    worker0.deliver(worker0.pipes[1])
    worker0.send('Yes.', worker0.pipes[2])

    global result1
    result1 = [counter for counter in worker0.counter]


def process_two(worker1: TotalWorker):
    worker1.deliver(worker1.pipes[2])
    worker1.deliver(worker1.pipes[0])
    worker1.send('A!', worker1.pipes[0])

    global result2
    result2 = [counter for counter in worker1.counter]


def process_three(worker2: TotalWorker):
    worker2.send('Hell yeah!', worker2.pipes[1])
    worker2.event()
    worker2.deliver(worker2.pipes[0])

    global result3
    result3 = [counter for counter in worker2.counter]


if __name__ == '__main__':
    unittest.main()
