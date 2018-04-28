# encoding=utf-8
import gevent
# Create your tests here.
import requests
import time
from gevent import monkey
monkey.patch_all()

def p():
    res = requests.get(url)
    print(res.status_code)

url = 'http://122.152.195.174/cbg/role'
while True:
    l = []
    for i in range(100):
        l.append(gevent.spawn(p))
    gevent.joinall(l)
    print('一轮请求完成')


