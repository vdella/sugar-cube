def notify_baton_pass(func):
    def wrapper():
        func()
        print('Baton passed!')
    return wrapper
