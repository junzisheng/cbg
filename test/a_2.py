import requests
import gevent
from gevent import monkey
import random
monkey.patch_all()
url = 'http://127.0.0.1:8080/proxy/insert/?proxy_list=[{%22ip%22:%221%22},%20{%22ip%22:%222%22}]'
x = []
def c():
    try:
        r =requests.get(url)
    except Exception as e:
        print(e)
        return
    print(r.content)
    if r.content in x:
        print('wrong>>>>>>>>>>>>')
        exit()
    x.append(r.content)
while 1:
    l = []
    for i in range(1000):
        l.append(gevent.spawn(c))
    gevent.joinall(l)
    # for i in range(1000):
    #     c()


