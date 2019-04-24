import socket
from Interface.detection import run
from Interface.logconfig import config;

config()
import logging
import os
from multiprocessing import Process, Pool
import nt
import functools

my_cpu_counts = nt.cpu_count() // 2  # 8 / 2 = 4核

log_dir = os.environ["log"]
if not log_dir:
    if not os.path.exists("D:\\Log4py"):
        os.mkdir("D:\\Log4py")
        with open(os.path.join("D:\\Log4py", "misc.log"), "w") as f:
            f.close()
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=os.path.join(log_dir, "misc.log"), level=logging.DEBUG, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)
logging.info("[Observer] The observer server is started!")


# monkey.patch_socket()

def log_pid(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("[Observer] 子进程:<pid={}>开启".format(os.getpid()))
        func(*args, **kwargs)
        logging.info("[Observer] 子进程<pid=%s>执行完毕" % os.getcwd())

    return wrapper


@log_pid
def observer(port):
    print("waiting")
    sock = socket.socket()
    ip = socket.gethostname()
    port = port
    sock.bind((ip, port))
    logging.info("[Observer] Listening: {}".format(sock.getsockname()))

    sock.listen(my_cpu_counts)
    while True:
        c, addr = sock.accept()
        bytestr = c.recv(1024)
        image_url = bytes.decode(bytestr)
        import json
        urls = json.loads(image_url)
        ret = run(urls).encode("utf-8")
        c.send(ret)
        logging.info("[Observer] 预测结果：{}".format(ret))
        c.close()


if __name__ == "__main__":
    tasks = set()
    for i in range(my_cpu_counts // 2):
        p = Process(target=observer, args=(5052 + i,))
        p.start()
        tasks.add(p)
    for i in tasks:
        i.join()
