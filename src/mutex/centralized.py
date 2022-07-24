from src.order.total import TotalWorker, WorkerPool


def atomize_for(worker: TotalWorker):
    worker.state = 'WANTED'
    message = (worker.counter, worker.serial)

    worker.broadcast(message)

    worker.state = 'HELD'


if __name__ == '__main__':
    pool = WorkerPool(3)

    for t_worker in pool.workers:
        t_worker.state = 'RELEASED'
