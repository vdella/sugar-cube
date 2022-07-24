def notify_send(func):
    def wrapper(*args):
        func(args)

        worker = args[0]
        content = args[1]
        print('Sent \'{}\' from {}! Time: {}\n'.format(content, worker.serial, worker.counter))
    return wrapper


def notify_event(event):
    def wrapper(*args):
        worker = args[0]
        event(worker)

        print('Event has happened in {}! Time = {}\n'.format(worker.serial, worker.counter))
    return wrapper


def notify_message_arrival(func):
    def wrapper(*args):
        worker = args[0]
        pipe = args[1]
        message, sender_pid = func(worker, pipe)  # Works for both 'receive' and 'deliver'.

        print('\'{}\' from {} to {}! Time: {}\n'.format(message, sender_pid, worker.serial, worker.counter))
    return wrapper
