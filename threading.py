import threading


class MyThread(threading.Thread):
    """My Own Thread class."""

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('It worked!')


t = MyThread()
t.start()
