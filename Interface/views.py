from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from watchdog.events import FileSystemEventHandler
import json
import threading
import socket
import logging
import random

"""
配置logging模块
"""
from Interface.logconfig import config

config()
logging.info("The django server is started!")
# monkey.patch_socket()


"""
    观察者集合
"""
observers = {5052: 0, 5053: 0}

observer_lock = threading.Lock()


class MyHandler(FileSystemEventHandler):

    def on_modified(self, event):
        global is_done
        if event.src_path == r"C:\Users\Firefox\PycharmProjects\E\Interface\result.txt":
            is_done = True


# Create your views here.
@csrf_exempt
def detect(request):
    global is_done
    if not request.body:
        logging.error("请求体为空")
        return JsonResponse({"ERROR": "The request body is empty!"})
    logging.info("New request: {}".format(request.body))
    s = socket.socket()
    port = -1
    most_vacant_port = -1  # 最空闲的端口
    zeros_port = []  # 空闲端口
    min = 100
    for k, v in observers.items():
        if v == 0:
            zeros_port.append(k)
        elif v < min:
            min = v
            most_vacant_port = k
    if zeros_port:
        port = random.randint(zeros_port[0], zeros_port[len(zeros_port) - 1])
    else:
        port = most_vacant_port
    print("using port", port)
    print("Observers:", observers)
    # +1
    observer_lock.acquire()
    observers[port] += 1
    observer_lock.release()

    # 套接字配置发送
    s.connect((socket.gethostname(), port))
    s.send(request.body)
    response = s.recv(10000)

    # -1
    observer_lock.acquire()
    observers[port] -= 1
    observer_lock.release()

    if response:
        return JsonResponse(json.loads(bytes.decode(response)))
    else:
        return JsonResponse({"ERROR:": "InnerError"})
