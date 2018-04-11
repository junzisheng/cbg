import gevent
# Create your tests here.
import requests
import time
from gevent import monkey
monkey.patch_all()

url = 'http://www.guwenjiang.com:8001/cbg/role/'
def test(x):
    print(x)
    time.sleep(1)

x = 0
while 1:
    r = gevent.spawn(test, x)

