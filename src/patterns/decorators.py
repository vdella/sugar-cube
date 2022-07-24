def notify_send(func):
    def wrapper(*args):
        worker = args[0]
        content = args[1]
        pipe = args[2]
        func(worker, content, pipe)  # Works for 'send' and 'broadcast'.

        print('Message \'{}\' from {}! Time: {}\n'.format(content, worker.serial, worker.counter))
    return wrapper


def notify_event(event):
    def wrapper(*args):
        worker = args[0]
        event(worker)

        print('Event has happened in {}! Time = {}\n'.format(worker.serial, worker.counter))
    return wrapper


def notify_receive(func):
    def wrapper(*args):
        worker = args[0]
        pipe = args[1]
        message, sender_pid = func(worker, pipe)  # Works for 'receive' and 'deliver'.

        print('\'{}\' from {} to {}! Time: {}\n'.format(message, sender_pid, worker.serial, worker.counter))
    return wrapper
