# encoding:utf-8
import gevent
from gevent import monkey
import json
import smtplib
from email.mime.text import MIMEText
import logging
logger = logging.getLogger('root')
monkey.patch_all()
mail_host = 'smtp.126.com'
mail_user = 'cbg_crawl@126.com'
mail_pass = 'g527910351'
LOG = 0
log = print if LOG else logging.info
track_mssage = None

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper


@try_except
def send(sub, user_email, content):
    global server
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = '藏宝阁消息宝<cbg_crawl@126.com>'
    msg['To'] = user_email
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, user_email, msg.as_string())
        log('%s的邮件【%s】发送成功' % (user_email, sub))
        res = True
    except Exception as e:
        log('%s的邮件【%s】发送失败' % (user_email, sub))
        log(e)
        global track_mssage
        track_mssage = str(e)
        res = False
    finally:
        server.close()
        return res

# def test():
#     import time
#     s = time.time()
#     while True:
#         for i in range(100):
#             # r = send('您得设置有信的消息', 'guwenjiang@namibox.com', '请点击http://www.baidu.com')
#             s = gevent.spawn(send, '您得设置有信的消息', '527910351@qq.com', '请点击http://www.baidu.com')
#             s.join()
#     log('耗时%s' (time.time() - s))

if __name__ == '__main__':
    import redis
    # REDIS_2 = redis.StrictRedis(host='122.152.195.174', db=3, password='Xj3.14164')
    REDIS_2 = redis.StrictRedis(host='localhost', db=3, password='Xj3.14164')
    # REDIS_2.publish('send_email', '123123123')
    # r = send('您得设置有信的消息', 'guwenjiang@namibox.com', '请点击http://www.baidu.com')
    p = REDIS_2.pubsub()
    p.subscribe(['update_crawl_data', 'new_crawl_data'])
    for item in p.listen():
        if item['type'] == 'message':
            data = json.loads(item['data'].decode())
            if item['channel'] == b'new_crawl_data':  # 新爬取数据
                content = u'您设置的【%s】有新的商品上架了！' % data['memo']
                for info in data['data_list']:
                    content += '%s-%s区:\t 链接: %s 价格: %s\r\n' % (info['server_name'], info['area_name'], info['dest_url'], info['price'])
                send(u'新商品上架提醒', 'guwenjiang@namibox.com', content)
            if item['channel'] == b'update_crawl_data':  # 价格变动
                for info in data['data_list']:
                    content += '%s-%s区:\t 链接: %s 价格: %s\r\n' % (info['server_name'], info['area_name'], info['dest_url'], info['price'])
                send(u'商品降价提醒', 'guwenjiang@namibox.com', content)
            # if item['channel'] == b'send_email':
            #     data = item['data'].decode()
            #     sub, user_email, content = data.split('|||')
            #     if not send(sub, user_email, content):
            #         send('邮件发送出错', 'guwenjiang@namibox.com', '【%s】\r\n【%s】发现出现了错误\r\n%s' % (user_email, sub, track_mssage))
