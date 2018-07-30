import json
import itchat
import sys
sys.path.insert(0, r'C:\Users\namibox\Desktop\project\cbg\cbg_backup')
from cbg_backup import settings
from libraries.cbg_logging import get_logger
logger = get_logger('weixin.log')


def send_msg(msg):
    try:
        author = itchat.search_friends(nickName='顾1234')[0]
        author.send(msg)
    except:
        logger.exception('发生了错误')


if __name__ == '__main__':
    # itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.auto_login(hotReload=True)
    itchat.run(blockThread=False)
    p = settings.redis2.pubsub()
    p.subscribe(['weixin_notic'])

    for item in p.listen():
        print(item)
        if item['type'] == 'message':
            data_dict = json.loads(item['data'].decode())
            if item['channel'] == b'weixin_notic':   # 数据结构  {'insert': [(game_ordersn, serverid)], 'down': [(,)]}
                msg = ""
                insert_list = data_dict['insert']
                down_list = data_dict['down']
                if insert_list:
                    msg = "您有%s条符合条件的通知：\n" % len(insert_list)
                    for game_ordersn, serverid in insert_list:
                        msg += 'http://xyq-m.cbg.163.com/cgi/mweb/product/detail/{0}/{1}'.format(serverid, game_ordersn)
                        msg += '\n'
                if down_list:
                    msg += '您有%s条降价通知：\n'
                    for game_ordersn, serverid in down_list:
                        msg += 'http://xyq-m.cbg.163.com/cgi/mweb/product/detail/{0}/{1}'.format(serverid, game_ordersn)
                        msg += '\n'
                r = send_msg(msg)
                logger.info(r)

