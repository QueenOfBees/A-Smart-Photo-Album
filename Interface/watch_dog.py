"""
    通过文件进行进程通讯，已经弃用
"""

from gevent import monkey;

monkey.patch_socket()
import gevent
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Interface.detection import run
import threading
import time

flag = False
last_time = 0


class OnModified(FileSystemEventHandler):
    def on_modified(self, event):
        global flag
        global last_time
        if event.src_path == r"C:\Users\Firefox\PycharmProjects\E\Interface\record.txt" and time.time() - last_time > 0.1:
            print("log file %s changed" % event.src_path)
            while flag:
                time.sleep(0)
            flag = True
            last_time = time.time()


if __name__ == "__main__":
    handler = OnModified()
    observer = Observer()
    watch = observer.schedule(event_handler=handler, path=r"C:\Users\Firefox\PycharmProjects\E\Interface",
                              recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
            if flag:
                gevent.spawn(run).join()
                flag = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
