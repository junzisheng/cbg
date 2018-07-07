import gevent
from gevent import monkey
import sys
monkey.patch_all()
# for k in sys.modules.keys():
#     if 'process'


import multiprocessing
from importlib import reload
reload(multiprocessing)
reload(multiprocessing)

import os

a = 0

def test(q):
    # while 1:
    #     r = requests.get('https://namibox.com')
    #     print(r.status_code)
    while 1:
        print(q.get(), '*'*10)


def g_test(q, i):
    # while True:
    #     pass
    # print(os.getpid())
    global a
    while 1:
        a += 1
        print(q.qsize(), '协程%s' %i)
        q.put(a)
        print('放了123 %s' % i)
        # time.sleep(1)



if __name__ == '__main__':
    q = multiprocessing.Queue(maxsize=10000)
    multiprocessing.Process(target=test, args=(q,)).start()
    l = [gevent.spawn(g_test, q, i) for i in range(10)]
    gevent.joinall(l)
    # print(time.time() - s)


