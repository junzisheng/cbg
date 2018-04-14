#encoding=utf-8
import json
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
import logging
import logging.config
import datetime
import requests
from requests.exceptions import *
import redis
import random
from urllib import parse
import config
import re
from SqlHelper import SqlHelper
from models import *
import time
logger = logging.getLogger("root")
_hostprog = re.compile('https?://([^/?]*)(.*)', re.DOTALL)
LOG = 1


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
        requests.post(self.ip_api_delete, data={'id_list': id_list})


class Crawl(object):
    def __init__(self, url, order_id , user_id, user_push_message_type, crawl_interval):
        # 用户设置相关
        self.base_url = url + '&page={0}'
        self.server = Server()
        # self.base_url = 'http://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py?act=overall_search_role&fang_yu=90&level_min=69&level_max=69&school=1&shang_hai=150&page={0}'
        self.user_id = user_id  # 用户的id
        self.order_id = order_id
        self.user_push_message_type = user_push_message_type  # 爬取到数据后给用户推送的方式
        self.push_2_users = []  # 用户设置的推送给其他人
        self.crawl_host = self.splithost(self.base_url)  # 爬取url的域名
        self.vaild_status = 0  # 正确的状态码
        self.max_restart_times = config.MAX_RESTART_TIMES
        # 每几条推送一次    (app or phone)
        self.crawl_interval = crawl_interval  # 爬取一轮的间隔时间
        self.crawled_eid_list = []  # 已经爬取的信息  以后爬到则不在给用户推送信息
        self.crawl_data_set = set()
        # 代理池相关
        # self.ip_api_select = '127.0.0.1:8888/?types=0&count=1000'
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
        # self.conn = None  # MySql句柄
        # self.cursor = None  # Mysql游标
        self.redis = None  # redis句柄
        self.session = None
        self.sql_tool = None
        # 价格变动多少进行提醒 todo

        self.set_dict = dict()  # 去重

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
        self.redis = redis.StrictRedis(host='localhost', password='Xj3.14164', port=6379, db=2)
        # self.get_proxy_list()
        self.server.get_proxy_list(self.proxy_list)
        self.get_crawled_eid_list()  # 获取已经爬取过
        self.sql_tool = SqlHelper()
        self.sql_tool.init_db()
        log('爬取的url为%s' % self.base_url)
        time.sleep(5)

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
        # log('结束了》》》》》》》》》》》》》》》》》》》》》')
        # raise KeyboardInterrupt


    # def first_page_crawl(self):
    #     """
    #     爬取第一页的数据，从而获取总页数，然后才能使用gevent 的joinall
    #     """
    #     url = self.base_url + '&page=1'
    #     data = self.crawl(url)

    def crawl(self, url, parse_func, page):
        """
        爬取
        """
        restart_times = -1  # 重试次数
        while True:
            log('当前爬取第%s页' % page)
            restart_times += 1
            log('重试了第%s次%s' % (restart_times, url))
            
            if restart_times > self.max_restart_times:
                log('重试次数达到上限 已经停止【%s】的爬取>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                self.fail_times += 1
                logger.info('重试次数达到上限 已经停止【%s】的爬取>>>>>>%s' % (url, self))
                logger.warning('重试次数达到上限 已经停止【%s】的爬取>>>>>>%s' % (url, self))
                self.fail_info.append(url)
                self.next_page += 1
                break
            try:
                # 没有可用的IP代理池时从远程重新获取新的IP代理
                if len(self.proxy_list) <= self.limit_proxy_count:  # 当维护的代理池小于20个时， 则需要拉取新的代理
                    self.server.get_proxy_list(self.proxy_list)
                proxy = random.choice(self.proxy_list) if restart_times < self.max_restart_times/2 or not self.localhost_ban else {}  # 当重试达到最大次数一半的时候使用本地ip进行爬取
                self.self_ip += 1 if proxy == {} else 0
                #proxy = {}
                # nice代理 proxy = {'https': 'https://129.70.129.187:3128'}
                header = self.get_header()
                response = requests.get(url, proxies=proxy, headers=header, timeout=2)
                #response = requests.get(url, proxies={}, headers=header, timeout=2)
                # 返回json data
                data = parse_func(response, url)
                self.success_times += 1
                log('成功 第%s次》》》》》》》》》》》》》》》》》》》》》》》》》' % restart_times)
                time.sleep(0.3)
                break
            except (ConnectTimeout, ConnectionError, ReadTimeout, NotTarget, IPBanned,
                    json.JSONDecodeError, ProxyError, StatusNot200) as e:
                log(e.__class__.__name__)
                self.handle_with_dity_ip(proxy)
            except (ChunkedEncodingError, TooManyRedirects, SystemBusy) as e:
                self.handle_with_hang_ip(proxy)
                log(e.__class__.__name__)
            except Exception as s:
                self.other_wrong +=1
                log(traceback.format_exc(), 'wrong>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                logger.error(traceback.format_exc())
                logger.error(u'发生错误，%s订单%s url % 页已停止爬取')
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
        从Mysql获取已经爬取的id
        """
        pass

    def get_proxy_list(self):
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
                self.proxy_list.append({
                    'http': 'http://{0}:{1}'.format(proxy['ip'], proxy['port']),
                    'https': 'https://{0}:{1}'.format(proxy['ip'],proxy['port']),
                    'id': proxy['_id'],
                })
            # if not self.localhost_ban and {} not in self.proxy_list:
            #     self.proxy_list.append({})  # 允许使用本地ip去访问
            log('获取了%s个代理' % len(self.proxy_list))
            break

    @try_except
    def handle_with_dity_ip(self, proxy):
        """
        处理无效的IP(访问被拒绝， timeout)
        """
        self.handle_with_hang_ip(proxy)
        if proxy == {}:
            self.localhost_ban = True
        else:
            self.server.delet_proxy([proxy['id']])
            # requests.post(self.ip_api_delete, data={'id_list': proxy['id']})

    @try_except
    def handle_with_hang_ip(self, proxy):
        """
        处理被挂起的IP: 被封；IP代理连接数满了
        """
        log('删除了%s, 还剩%s个代理' % (proxy, len(self.proxy_list)))
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
            log(response.status_code, response.url, 'text>>>>>>>>>>>', response.text)
            raise StatusNot200
        # 根据域名判断是否来源服务器的返回
        if self.splithost(response.url) != self.crawl_host:
            raise NotTarget
        data = json.loads(response.text)
        log(data.get('status', '--status'))
        if data.get('status') != self.vaild_status:
            raise IPBanned
        pager = data.get('pager')
        equip_list = data.get('equip_list')
        if not all([pager, equip_list]):
            # 可能原因 返回  {status: 0, msg: 系统繁忙}
            log(data)
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
        log(len(equip_list), '数据量')
        self.analysis(equip_list)
        self.next_page = 1 if not equip_list or pager['cur_page'] == pager['num_end'] else self.next_page +1
        #log(equip_list, 'equip_list>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # self.sql_tool.session_commit()
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
        if valid_update_list:
            self.sql_tool.batch_update(CrawlData, valid_update_list, 'price')

    @staticmethod
    def splithost(url):
        res = _hostprog.match(url)
        return res.group(1) if res else None


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












