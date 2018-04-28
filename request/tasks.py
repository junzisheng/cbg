#encoding=utf-8
from __future__ import absolute_import
from request.celery_init import app
import sys
import os
crawl_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(crawl_dir, 'crawl'))
import crawl_class
import time
# celery = Celery('tasks', broker='redis://:Xj3.14164@122.152.195.174:6379/1')

@app.task
def crawl_task(url, order_id, memo):
    """
    完成爬取的工作
    """
    # 一. 组建HEADERS
    # 1. 获取UA(内存获取)
    # 2. 如果没有IP代理池 则从远程数据库获取最新IP代理  IP代理池的维护  选择及时可用的 以及挂起超过一定时间的IP

    # 二.开始爬取数据
    """
    可能出现的情况:
    1. 没有获取数据
        1).访问超时>>>>删除代理ip 日志记录 重新爬取这一页的数据
        2).代理连接数满了>>>挂起代理 选择新的代理 日志记录 重新爬取这一页的数据
        # 3).IP被封 >>> 删除代理 日志记录 重新爬取这一页的数据
    2. 获取到了数据
        1).返回是代理回复的无效数据>>>删除代理ip 日志记录 重新爬取这一页的数据
        2).返回的是cbg数据：
            ①封禁信息>>>挂起代理 >>>日志记录 重新爬取这一页的数据
            ②有效信息
                ps:特性操作前的统一数据处理
                    1.数据入库
                    2.记录日志
                1.调度新的task处理信息(推送信息)
    3. 报错
        1) 记录日志
        2） 发送短信到我的手机
        3) 搭建错误查看的站点 可以使用admin?
    4. 爬取完成：
        记录爬取了几轮
        共获取了多少数据  效率多少  有多少无效ip  有多少挂满ip  有多少封禁ip  多少有效ip
    """
    c = crawl_class.Crawl(url, order_id, memo, 4, 5)
    start = time.time()
    print('start>>>>>%s' % start)
    try:
        c.run()
    except KeyboardInterrupt:
        print('*' * 100)
        print('end>>>>消耗了%s' % (time.time()-start))
        print('总共失败了%s次' % c.fail_times)
        print('总共成功%s次' % c.success_times)
        print('使用了%s自己的ip' % c.self_ip)
        print('connect timeout' ,'>>>>>>', c.connect_timeout)
        print('connect error','>>>>>>', c.connect_error)
        print('read timeout','>>>>>>', c.read_timeout)
        print('chunkendocingerror','>>>>>>', c.chunk_error)
        print('to many redirect','>>>>>>', c.to_many)
        print('not 200','>>>>>>', c.not_200)
        print('not targe','>>>>>>', c.not_target)
        print('banned','>>>>>>', c.ip_banned)
        print('json wrong', '  ', c.json_wrong)
        print('proxy error', c.proxy_error)
        print('system busy', c.system_busy)
        print('other', c.other_wrong)
        print('fail info', c.fail_info)

if __name__ == '__main__':
    import time

    c = crawl_class.Crawl(1, 2, 3, 4, 5)
    start = time.time()
    print('start>>>>>%s' % start)
    try:
        c.run()
    except KeyboardInterrupt:
        print('*' * 100)
        print('end>>>>消耗了%s' % (time.time()-start))
        print('总共失败了%s次' % c.fail_times)
        print('总共成功%s次' % c.success_times)
        print('使用了%s自己的ip' % c.self_ip)
        print('connect timeout' ,'>>>>>>', c.connect_timeout)
        print('connect error','>>>>>>', c.connect_error)
        print('read timeout','>>>>>>', c.read_timeout)
        print('chunkendocingerror','>>>>>>', c.chunk_error)
        print('to many redirect','>>>>>>', c.to_many)
        print('not 200','>>>>>>', c.not_200)
        print('not targe','>>>>>>', c.not_target)
        print('banned','>>>>>>', c.ip_banned)
        print('json wrong', '  ', c.json_wrong)
        print('proxy error', c.proxy_error)
        print('system busy', c.system_busy)
        print('other', c.other_wrong)
        print('fail info', c.fail_info)


















