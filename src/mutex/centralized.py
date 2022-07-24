from src.order.total import TotalWorker


def atomize_for(worker: TotalWorker):
    worker.state = 'WANTED'
    message = (worker.counter, worker.serial)

    worker.send(message, list())  # TODO gather all pipe entries and broadcast through them.

    worker.state = 'HELD'
