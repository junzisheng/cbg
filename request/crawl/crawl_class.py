#encoding=utf-8
import datetime
import json
import time
import logging.config
import random
import re
import traceback

import redis
import requests
from SqlHelper import SqlHelper
from models import *
from requests.exceptions import *
try:
    from request.crawl import config
except:
    import config


logger = logging.getLogger("root")
_hostprog = re.compile('https?://([^/?]*)(.*)', re.DOTALL)
LOG = 1
# todo 第一轮爬取免打扰


log = print if LOG else logging.info

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            logger.error('请求ip池接口报错>>>>{0}'.format(traceback.format_exc()))
            return False
    return wrapper

# class Exception(Exception):
#     def __init__(self):
#         log(self.__class__.__name__)

class NotTarget(Exception):  # 返回数据但不是目标服务器
    pass

class IPBanned(Exception):
    pass

class DataMiss(Exception):
    pass

class StatusNot200(Exception):
    pass

class SystemBusy(Exception):
    pass


class Server(object):
    """和远程服务器通信的类"""
    def __init__(self):
        self.ip_api_select = config.PROXY_GET_API
        self.ip_api_delete = config.PROXY_DELETE_API

    def get_proxy_list(self, container):
        """
        从proxy分发处获取有效代理列表
        """
        while 1:
            response = requests.get(self.ip_api_select)
            proxy_list = json.loads(response.text)
            # 组装代理
            if not proxy_list:
                log('没有获取到代理！！！！')
                time.sleep(10)
                continue
            for proxy in proxy_list:
                container.append({
                    'http': 'http://{0}:{1}'.format(proxy['ip'], proxy['port']),
                    'https': 'https://{0}:{1}'.format(proxy['ip'],proxy['port']),
                    'id': proxy['_id'],
                })
            log('获取了%s个代理' % len(proxy_list))
            break

    @try_except
    def delet_proxy(self, id_list):
        id_list = [id_list] if type(id_list) != list else id_list
        log('删除了ip', id_list)
        requests.post(self.ip_api_delete, data={'id_list': id_list})


class Crawl(object):
    def __init__(self, url, order_id, memo, user_id, crawl_interval):
        # 用户设置相关
        # self.base_url = url + '&page={0}'
        self.server = Server()
        self.base_url = 'http://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py?act=overall_search_role&fang_yu=90&level_min=69&level_max=69&school=1&shang_hai=150&page={0}'
        self.user_id = user_id  # 用户的id
        self.order_id = order_id
        self.memo = memo
        self.push_2_users = []  # 用户设置的推送给其他人
        self.crawl_host = self.splithost(self.base_url)  # 爬取url的域名
        self.vaild_status = 0  # 正确的状态码
        self.max_restart_times = config.MAX_RESTART_TIMES
        # 每几条推送一次    (app or phone)
        self.crawl_interval = crawl_interval  # 爬取一轮的间隔时间
        self.crawled_eid_list = []  # 已经爬取的信息  以后爬到则不在给用户推送信息
        self.crawl_data_set = set()
        # 代理池相关
        self.ip_api_select = config.PROXY_GET_API
        self.ip_api_delete = config.PROXY_DELETE_API
        self.limit_proxy_count = config.MIN_PROXY_LIST_COUNT
        # self.ip_api_delete = '127.0.0.1:8888/delete?ip={0}'
        # 爬取相关
        self.next_page = 1
        self.localhost_ban = False  # 记录本地ip是否被封
        self.user_agent_list = config.USER_AGENTS
        self.proxy_list = []  # ip代理池
        self.ua_list = []  # UA
        self.cur_page = 0  # 当前爬取的页数
        self.end_page = 0
        self.dirty_ip_amount = 0  # 无效ip
        self.banned_ip_amount = 0  # 封禁ip
        self.full_ip = 0  # 挂载满的ip
        self.invaild_ip_list = []  # 全局可能可用，但是这个任务不能使用的ip  todo 一段时间需要将其清空
        # 数据库相关
        self.redis = None  # redis句柄
        self.session = None
        self.sql_tool = None
        # 价格变动多少进行提醒 todo

        self.set_dict = dict()  # 去重
        self.redis_3 = redis.StrictRedis(**config.REDIS3_CONFIG)  # 用来推送新消息或者价格变动的消息
        # 调试数据
        self.fail_times = 0
        self.success_times = 0
        self.self_ip = 0
        self.wrong = []
        self.connect_timeout = 0
        self.connect_error = 0
        self.read_timeout = 0
        self.chunk_error = 0
        self.to_many = 0
        self.not_200 = 0
        self.not_target = 0

        self.ip_banned = 0
        self.json_wrong = 0
        self.proxy_error = 0
        self.other_wrong = 0
        self.system_busy = 0
        self.fail_info = []
        self.init()


    def init(self):
        """
        初始化
        """
        self.server.get_proxy_list(self.proxy_list)
        self.sql_tool = SqlHelper()
        self.sql_tool.init_db()
        # self.get_crawled_eid_list()  # 获取已经爬取过
        self.log('爬取的url为%s' % self.base_url)
        time.sleep(5)

    def log(self, *args):
        log(args)
        log(self.memo)


    def __del__(self):
        pass

    def __str__(self):
        return ''  # 这里填写爬取的信息

    def run(self):
        """
        启动
        """
        while 1:
            self.crawl(self.base_url.format(self.next_page), self.parse, self.next_page)

    def crawl(self, url, parse_func, page):
        """
        爬取
        """
        restart_times = -1  # 重试次数
        while True:
            self.log('当前爬取第%s页' % page)
            restart_times += 1
            self.log('重试了第%s次%s' % (restart_times, url))
            
            if restart_times >= self.max_restart_times:
                self.fail_times += 1
                self.log('重试次数达到上限 已经停止第【%s】页的爬取' % self.next_page)
                self.fail_info.append(url)
                self.next_page += 1
                break
            try:
                # 没有可用的IP代理池时从远程重新获取新的IP代理
                if len(self.proxy_list) <= self.limit_proxy_count:  # 当维护的代理池小于20个时， 则需要拉取新的代理
                    pass
                    # self.server.get_proxy_list(self.proxy_list)
                proxy = random.choice(self.proxy_list) if restart_times < self.max_restart_times/2 or not self.localhost_ban else {}  # 当重试达到最大次数一半的时候使用本地ip进行爬取
                # proxy = {}
                self.self_ip += 1 if proxy == {} else 0
                # nice代理 proxy = {'https': 'https://129.70.129.187:3128'}
                header = self.get_header()
                response = requests.get(url, proxies=proxy, headers=header, timeout=2)
                data = parse_func(response, url)
                self.success_times += 1
                self.log('成功 第%s次' % restart_times)
                time.sleep(0.3)
                break
            except (NotTarget, IPBanned, json.JSONDecodeError, ProxyError, StatusNot200) as e:
                self.log(e.__class__.__name__)
                self.handle_with_dity_ip(proxy)
            except (ChunkedEncodingError, TooManyRedirects, SystemBusy, ConnectTimeout,
                    ConnectionError, ReadTimeout, ) as e:
                self.handle_with_hang_ip(proxy)
                self.log(e.__class__.__name__)
            except Exception as s:
                self.other_wrong +=1
                self.log('*' * 100)
                self.log(s)
                self.log('*' * 100)
                break

    def get_header(self):
        return {
            'User-Agent': random.choice(self.user_agent_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }

    def get_crawled_eid_list(self):
        """
        从Mysql获取已经爬取的id, price
        """
        for eid, price in self.sql_tool.session.query(CrawlData.eid, CrawlData.price):
            self.set_dict[eid] = price

    @try_except
    def handle_with_dity_ip(self, proxy):
        """
        处理无效的IP(访问被拒绝， timeout)  # todo 可以做成异步的
        """
        self.handle_with_hang_ip(proxy)
        if proxy == {}:
            self.localhost_ban = True
        else:
            self.server.delet_proxy([proxy['id']])

    @try_except
    def handle_with_hang_ip(self, proxy):
        """
        处理被挂起的IP: 被封；IP代理连接数满了
        """
        self.log('删除了%s, 还剩%s个代理' % (proxy, len(self.proxy_list)))
        if proxy == {}:
            self.localhost_ban = True
        else:
            if proxy in self.proxy_list:
                self.proxy_list.remove(proxy)

    def parse(self, response, crawl_url):
        """
        解析数据
        """
        if response.status_code != 200:
            self.log(response.status_code, response.url, 'text>>>>>>>>>>>', response.text)
            raise StatusNot200
        # 根据域名判断是否来源服务器的返回
        if self.splithost(response.url) != self.crawl_host:
            raise NotTarget
        data = json.loads(response.text)
        if data.get('status') != self.vaild_status:
            raise IPBanned
        pager = data.get('pager')
        equip_list = data.get('equip_list')
        if not all([pager, equip_list]):
            # 可能原因 返回  {status: 0, msg: 系统繁忙}
            self.log(data)
            raise SystemBusy
        # 数据入库  目录格式:
        """
        {
            status: 0,
            pager: {
                num_end: 100,
                num_begin: 1,
                cur_page: 1,
            }
            equip_list : [
            {...},
            {....},
            ]
        }
        """
        self.log(len(equip_list), '数据量')
        self.analysis(equip_list)
        if not equip_list or pager['cur_page'] == pager['num_end'] or self.next_page == 100:
            self.next_page = 1
        else:
            self.next_page += 1
        # todo 消息提醒
        return data

    def analysis(self, equip_list):
        """分析数据"""
        # for k in self.set_dict: #for test
        #     self.set_dict[k] = '1'
        valid_update_list = []
        valid_insert_list = []
        for equip in equip_list:
            server_name = equip['server_name']
            serverid = equip['serverid']
            area_name = equip['area_name']
            time_left = equip['time_left']
            price = equip['price']
            nickname = equip['nickname']
            collect_num = equip['collect_num']
            eid = equip['eid']
            create_time = equip['create_time']
            data_dict = {
                            'server_name': server_name,
                            'serverid': serverid,
                            'area_name': area_name,
                            'time_left': time_left,
                            'price': price,
                            'nickname': nickname,
                            'collect_num': collect_num,
                            'eid': eid,
                            'create_time': create_time,
                            'dest_url': 'http://xyq.cbg.163.com/equip?s={0}&eid={1}'.format(serverid, eid),
                            'crawl_time': datetime.datetime.now(),
                            'order_id': self.order_id,
                        }
            # 更新价格
            if eid in self.set_dict and self.set_dict[eid] != price:
                valid_update_list.append(data_dict)
            # 插入数据
            if eid not in self.set_dict:
                valid_insert_list.append(data_dict)
                self.set_dict[eid] = price
        if valid_insert_list:
            self.sql_tool.batch_insert(CrawlData, valid_insert_list)
            self.redis_3.publish('new_crawl_data', json.dumps({
                'user_id': self.user_id,
                'data_list': self.datetime_serialize(valid_insert_list),
                'memo': self.memo,
            }))
            self.log('提交了%s条数据' % len(valid_insert_list))
        if valid_update_list:
            self.sql_tool.batch_update(CrawlData, valid_update_list, 'price')
            self.redis_3.publish('updata_crawl_data', json.dumps({
                'user_id': self.user_id,
                'data_list': self.datetime_serialize(valid_update_list),
                'memo': self.memo,
            }))
            self.log('更新了%s条数据' % len(valid_update_list))

    @staticmethod
    def splithost(url):
        res = _hostprog.match(url)
        return res.group(1) if res else None

    def datetime_serialize(self, l):
        for item in l:
            for k, v in item.items():
                if isinstance(v, datetime.datetime):
                    item[k] = str(v)
        return l





if __name__ == '__main__':
    import time

    c = Crawl(1, 2, 3, 4, 5)
    start = time.time()
    log('start>>>>>%s' % start)
    try:
        c.run()
    except KeyboardInterrupt:
        log('*' * 100)
        log('end>>>>消耗了%s' % (time.time()-start))
        log('总共失败了%s次' % c.fail_times)
        log('总共成功%s次' % c.success_times)
        log('使用了%s自己的ip' % c.self_ip)
        log('connect timeout' ,'>>>>>>', c.connect_timeout)
        log('connect error','>>>>>>', c.connect_error)
        log('read timeout','>>>>>>', c.read_timeout)
        log('chunkendocingerror','>>>>>>', c.chunk_error)
        log('to many redirect','>>>>>>', c.to_many)
        log('not 200','>>>>>>', c.not_200)
        log('not targe','>>>>>>', c.not_target)
        log('banned','>>>>>>', c.ip_banned)
        log('json wrong', '  ', c.json_wrong)
        log('proxy error', c.proxy_error)
        log('system busy', c.system_busy)
        log('other', c.other_wrong)
        log('fail info', c.fail_info)


"""
更新记录
1. 2018 4.15  将数据插入由爬取工具连接数据库 转为 数据传入服务器 服务器插入
"""


