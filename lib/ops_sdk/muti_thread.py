# coding:utf-8

# from datetime import datetime
import threading
from queue import Queue


class ThreadWorker(threading.Thread):
    def __init__(self, queue, func, kwargs={}):
        threading.Thread.__init__(self)
        self._queue = queue
        self.func = func
        self.kwargs = kwargs

    def run(self):
        while not self._queue.empty():
            item = self._queue.get()
            try:
                self.func(item, **self.kwargs)
            except Exception as e:
                print(e)


def muti_run(func, kwargs={},  iters=range(10), thread_count=10):
    """
    多线程任务脚本。
    例如 print(111,22,333);
    :param func: 单个线程需要执行的方法
    :param kwargs: 线程中函数传递的参数内容（静态的参数内容）;
    :param iters: 动态传递的迭代内容；
    :param thread_count: 线程数
    :return:
    """
    queue = Queue()
    for x in iters:
        queue.put(x)
    threads = [ThreadWorker(queue, func=func, kwargs=kwargs) for i in range(thread_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return None
