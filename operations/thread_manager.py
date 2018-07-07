import threading
from queue import Queue


class WorkManager(object):
    """管理类"""
    def __init__(self, thread_num=5):
        self.__sync_id = 0
        self.__threads = []
        self.__work_queue = Queue(maxsize=10000)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self, thread_num):
        """初始化一定数量的线程"""
        for i in range(thread_num):
            self.__threads.append(Work(self.__work_queue))

    def get_queue(self):
        return self.__work_queue

    def add_job(self, func, args):
        self.__work_queue.put((func, list(args)))

    def check_queue(self):
        return self.__work_queue.qsize()

    def get_sync_id(self):
        return self.__sync_id

    def set_sync_id(self, _id):
        self.__sync_id = _id

    def wait_all_complete(self):
        for item in self.__threads:
            if item.isAlive():
                item.join()


class Work(threading.Thread):
    """工作的类"""
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            do, args = self.work_queue.get()
            do(args)
