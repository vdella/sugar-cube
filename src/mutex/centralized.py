from src.order.total import WorkerPool
from random import randint

batom = 0  # As the index of the actual process to be looked upon in a list.
process_qtt = 0


def batom_pass():
    """Updates the batom value as it's an index of a circular list."""
    global batom
    batom += (batom + 1) % process_qtt


if __name__ == '__main__':
    pool = WorkerPool(7)
    process_qtt = pool.process_qtt

    # Two processes want to utilize the shared resource. We get them by randint(), but...
    wanted1 = randint(0, process_qtt - 1)
    wanted2 = randint(0, process_qtt - 1)

    # ... If both processes are the same, we need to change one of them to ensure they are different.
    while wanted1 == wanted2:
        wanted2 = randint(0, process_qtt - 1)

    pool.workers[wanted1].state = 'WANTED'
    pool.workers[wanted2].state = 'WANTED'

    # Creates a simple list as the shared resource between processes.
    shared_resource = [i for i in range(process_qtt)]
