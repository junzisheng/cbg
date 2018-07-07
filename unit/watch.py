import psutil
import time

def main():
    net = psutil.net_io_counters()
    sent = net.bytes_sent / 1024 * 8
    recv = net.bytes_sent / 1024 * 8
    time.sleep(1)
    _net = psutil.net_io_counters()
    _sent = _net.bytes_sent / 1024 * 8
    _recv = _net.bytes_sent / 1024 * 8
    print('发送:%skbps 接收:%skbps, cpu: %s' % (_sent-sent, _recv-recv, psutil.cpu_percent()))

if __name__ == '__main__':
    while True:
        main()

