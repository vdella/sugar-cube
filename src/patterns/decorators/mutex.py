def notify_baton_pass(func):
    def wrapper(*args):
        worker = args[0]
        func(worker)

        print('Baton passed from {}\n'.format(worker.serial))
    return wrapper
