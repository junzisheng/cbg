import gevent
import requests

def test():
    r = requests.get('http://ip.chinaz.com/getip.aspx')
    print(r.status_code, r.text)


if __name__ == '__main__':
    l = []
    for i in range(1000):
        l.append(gevent.spawn(test))
    gevent.joinall(l)
