from threading import Event
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyEventHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')


if __name__ == "__main__":
    pattern = ['./dir/file']
    event_handler = MyEventHandler(patterns=pattern)
    observer = Observer()
    observer.schedule(event_handler, './dir', recursive=True)
    observer.start()

    try:
        Event().wait()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
