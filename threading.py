import threading
import time
import os
import sys


class Watcher(object):
    running = True

    def __init__(self, watch_file, refresh_delay=1, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.filename = watch_file
        self.refresh_delay = refresh_delay
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    def look(self):
        statinfo = os.stat(self.filename)
        if statinfo.st_mtime != self._cached_stamp:
            self._cached_stamp = statinfo.st_mtime
            # File has changed, so do something...
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    def watch(self):
        while self.running:
            self.look()  # Look for changes
            time.sleep(self.refresh_delay)


class MyThread(threading.Thread):
    """My Own Thread class."""

    def __init__(self):
        super().__init__()
        self._signal = threading.Event()

    def run(self):
        print('%s running' % self.name)
        self._signal.wait()
        print('%s exiting' % self.name)

    def stop(self):
        self._signal.set()


class MainThread(threading.Thread):
    """Main Thread."""

    def __init__(self):
        super().__init__()
        self.signal = threading.Event()
        self.threads = []

    def run(self):

        while True:
            with open('myfile', 'r') as f:
                n = int(f.readline())

            for i in range(n):
                t = MyThread()
                self.threads.append(t)

            for t in self.threads:
                t.start()

            self.signal.wait()

            for t in self.threads:
                t.stop()
                t.join()

            self.threads.clear()
            self.signal.clear()

    def reset(self):
        self.signal.set()


def event_on_file_change(*args, **kwargs):
    t = kwargs['thread']
    if not t.is_alive():
        t.start()
    else:
        t.reset()


if __name__ == "__main__":
    watch_file = 'myfile'

    t = MainThread()

    watcher = Watcher(
        watch_file, call_func_on_change=event_on_file_change, thread=t)

    while True:
        try:
            watcher.watch()  # start the watch going
        except KeyboardInterrupt:
            break
        except FileNotFoundError:
            print('File not found.')
            time.sleep(1)  # Give some time for the file to be created.
        except:
            break
