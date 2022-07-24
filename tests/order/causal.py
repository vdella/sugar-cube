import unittest
from src.order.causal import PartialWorker
from multiprocessing import Value, Pipe


class CausalOrderTest(unittest.TestCase):

    @staticmethod
    def execute_processes():
        one_and_two, two_and_one = Pipe()
        two_and_three, three_and_two = Pipe()
        one_and_three, three_and_one = Pipe()

        worker1, result1 = PartialWorker(0), Value('i', 0)
        worker2, result2 = PartialWorker(1), Value('i', 0)
        worker3, result3 = PartialWorker(2), Value('i', 0)

        process1 = worker1.process(target=process_one, args=(worker1, one_and_two, one_and_three, result1))
        process2 = worker2.process(target=process_two, args=(worker2, two_and_one, two_and_three, result2))
        process3 = worker3.process(target=process_three, args=(worker3, three_and_two, three_and_one, result3))

        process1.start()
        process2.start()
        process3.start()

        process1.join()
        process2.join()
        process3.join()

        return result1.value, result2.value, result3.value

    def test_causal_order(self):
        exec_results = self.execute_processes()

        def test_causal_order_for_process1():
            self.assertTrue(6, exec_results[0])
        test_causal_order_for_process1()

        def test_causal_order_for_process2():
            self.assertTrue(4, exec_results[1])
        test_causal_order_for_process2()

        def test_causal_order_for_process3():
            self.assertTrue(7, exec_results[2])
        test_causal_order_for_process3()


def process_one(worker1, pipe12, pipe13, result):
    worker1.event()
    worker1.send('Hello!', pipe12)
    worker1.event()
    worker1.receive(pipe12)
    worker1.send('Yes.', pipe13)

    result.value = worker1.counter


def process_two(worker2, pipe21, pipe23, result):
    worker2.receive(pipe23)
    worker2.receive(pipe21)
    worker2.send('A!', pipe21)

    result.value = worker2.counter


def process_three(worker3, pipe32, pipe31, result):
    worker3.send('Hell yeah!', pipe32)
    worker3.event()
    worker3.receive(pipe31)

    result.value = worker3.counter


if __name__ == '__main__':
    unittest.main()
