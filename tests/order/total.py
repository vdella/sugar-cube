import unittest
from src.order.total import WorkerPool
from multiprocessing import Array


result1 = Array('i', range(3))
result2 = Array('i', range(3))
result3 = Array('i', range(3))


class TotalOrderTest(unittest.TestCase):

    @staticmethod
    def execute_processes():
        one_and_two, two_and_one = channels[(0, 1)]
        two_and_three, three_and_two = channels[(1, 2)]
        one_and_three, three_and_one = channels[(0, 2)]

        pool = WorkerPool(3)
        worker1 = pool.workers[0]
        worker2 = pool.workers[1]
        worker3 = pool.workers[2]

        process1 = worker1.process(target=process_one, args=(worker1, one_and_two, one_and_three))
        process2 = worker2.process(target=process_two, args=(worker2, two_and_one, two_and_three))
        process3 = worker3.process(target=process_three, args=(worker3, three_and_two, three_and_one))

        process1.start()
        process2.start()
        process3.start()

        process1.join()
        process2.join()
        process3.join()

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


def process_one(worker1, pipe12, pipe13):
    worker1.event()
    worker1.send('Hello!', [pipe12])
    worker1.event()
    worker1.deliver(pipe12)
    worker1.send('Yes.', [pipe13])

    global result1
    result1 = [counter for counter in worker1.counter]


def process_two(worker2, pipe21, pipe23):
    worker2.deliver(pipe23)
    worker2.deliver(pipe21)
    worker2.send('A!', [pipe21])

    global result2
    result2 = [counter for counter in worker2.counter]


def process_three(worker3, pipe32, pipe13):
    worker3.send('Hell yeah!', [pipe32])
    worker3.event()
    worker3.deliver(pipe13)

    global result3
    result3 = [counter for counter in worker3.counter]


if __name__ == '__main__':
    unittest.main()
