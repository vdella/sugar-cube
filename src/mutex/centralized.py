from src.order.total import WorkerPool, TotalWorker
from random import randint
from multiprocessing import Value
from src.patterns.decorators.mutex import notify_baton_pass


baton = Value('i', 0)  # As the index of the actual process to be looked upon in a list.
process_qtt = 0
shared_resource = 0  # Creates a simple value as the shared resource between processes.


@notify_baton_pass
def baton_pass(total_worker: TotalWorker):
    """Updates the batom value as it's an index of a circular list."""
    global baton
    baton.value = (baton.value + 1) % process_qtt
    total_worker.broadcast('Baton value = {}'.format(baton.value - 1))


def target(total_worker: TotalWorker):
    """A target function for a process. Its :param total_worker
    will wait for messages while it cannot obtain the critical region and,
    when it does, will call an event()."""
    while baton.value != total_worker.serial:
        total_worker.deliver(total_worker.pipes[baton.value])

    if baton.value == total_worker.serial:
        if total_worker.state == 'WANTED':
            global shared_resource
            shared_resource = total_worker.serial

            total_worker.state = 'RELEASED'
            print('{} obtained the resource! Time: {}'.format(total_worker.serial, total_worker.counter))
            total_worker.event()
        baton_pass(total_worker)


if __name__ == '__main__':
    pool = WorkerPool(7)
    process_qtt = pool.process_qtt

    for i, worker in enumerate(pool.workers):
        worker.state = 'RELEASED'
        pool.processes[i] = worker.process(target=target, args=(worker,))

    # Two processes want to utilize the shared resource. We get them by randint(), but...
    wanted1 = randint(0, process_qtt - 1)
    wanted2 = randint(0, process_qtt - 1)

    # ... If both processes are the same, we need to change one of them to ensure they are different.
    while wanted1 == wanted2:
        wanted2 = randint(0, process_qtt - 1)

    pool.workers[wanted1].state = 'WANTED'
    pool.workers[wanted2].state = 'WANTED'

    print('{} and {} want the resource!\n'.format(wanted1, wanted2))

    pool.start()

    pool.join()
