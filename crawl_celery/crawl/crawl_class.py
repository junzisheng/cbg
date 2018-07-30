#encoding=utf-8
import datetime
import time
import json
import random
import re
import requests
from requests.exceptions import *


from  crawl_celery.crawl.exceptions import *
from crawl_celery.models import CbgCrawlData
from crawl_celery.crawl.Base_Class import Logger, TaskManager, ProxyManager, SqlLock
from crawl_celery.crawl import config


_hostprog = re.compile('https?://([^/?]*)(.*)', re.DOTALL)


# 应该只传一个orderid过来
class Base_Crawl(object):
    task_manager = TaskManager
    def __init__(self, url, order_info, crawl_interval=1, rounds=1):
        # 初始化日志类
        # 用户设置相关
        self.base_url = url + '&page={0}&timestamp={1}&'
        self.order_info = order_info
        # 将日期参数恢复
        self.order_info['end_time'] = datetime.datetime.strptime(order_info['end_time'], '%Y-%m-%d %H:%M:%S')
        # self.order_info['service_time'] = datetime.datetime.now() + datetime.timedelta(hours=9)
        self.order_info['time_range'] = datetime.timedelta(**order_info['time_range'])  # 获取多久内的数据
        # self.order_info['time_range'] = datetime.timedelta(minutes=10)
        #self.push_2_users = []  # 用户设置的推送给其他人
        self.push_type = order_info['push_type'].split(';') if order_info['push_type'] else None
        self.crawl_host = self.splithost(self.base_url)  # 获取爬取url的域名
        self.max_restart_times = 6  # 爬取重试的最大次数
        # 每几条推送一次    (app or phone)
        self.crawl_interval = crawl_interval  # 爬取一轮的间隔时间
        # 爬取相关
        self.start_date = datetime.datetime.now()  # 爬取开始的时间
        self.rounds = rounds  # 爬取的轮数  todo 考虑重新开启celery后任务重启的情况下
        self.next_page = 1
        self.user_agent_list = config.USER_AGENTS
        self.proxy_list = []  # ip代理池

        self.page_one_time = time.time()  # 爬取第一页的时间

        self.set_dict = dict()  # 去重  # 存贮已经爬取到的信息   {eid: {price: , ...}}
        self.use_count_url = True  # 是否使用支持count的url 和不支持count数据处理不同


    def init(self):
        """
        初始化
        """
        #self.logger = self.task_manager.Logger('order_id-%s' % self.order_info['order_id'] + self.order_info['memo'])
        ProxyManager.get_proxy_list()
        self.get_crawled_eid_list()

    def get_service_info(self):
        """从redis获取服务信息 如：
            推送方式
            服务期限
            参数修改
        """
        pass

    def __del__(self):
        pass

    def run(self):
        """ 启动 """
        self.init()
        while datetime.datetime.now() <= self.order_info['end_time']:
            if self.next_page == 1:
                self.page_one_time = time.time()
            self.crawl(self.base_url.format(self.next_page, time.time()))
            # gevent.sleep(self.crawl_interval)
        # 任务结束的逻辑在这里写或者on_sucess函数中写
        Logger.cls_error.info('爬取任务全部完成>>>>订单:%s, 耗时%s, 共爬取到了%s条数据, 历时%s轮'
            % (self.order_info['order_id'], datetime.datetime.now() - self.start_date, len(self.set_dict), self.rounds))
        if self in self.task_manager.crawl_obj_list:
            self.task_manager.crawl_obj_list.remove(self)
    # todo 进行一些算法控制  比如一轮爬取休息的时间取决于当前的繁忙程度 cpu, 网络


    def crawl(self, url):
        """ 爬取 """
        Logger.cls_error.info('第%s页' % (self.next_page))
        restart_times = -1  # 重试次数
        while True:
            restart_times += 1
            if restart_times > self.max_restart_times:
                Logger.cls_error.info('重试次数达到上限 已经停止第【%s】页的爬取>>>%s' % (self.next_page, url))
                self.next_page += 1
                break
            # 获取一个代理
            proxy = ProxyManager.select_proxy(restart_times == self.max_restart_times)
            header = self.get_header()
            try:
                response = requests.get(url, proxies=ProxyManager.create_vaild_proxy(proxy),
                                        headers=header, timeout=5)
                # 解析返回的数据
                self.public_check(response, url)
                data = json.loads(response.text)
                # 每个子类具体的校验函数
                self.different_check(data, proxy)
                equip_list = data.get('equips', []) if self.use_count_url else data.get('equip_list', [])
                if len(equip_list) == 0:
                    raise Empty
                out_time_range = self.analysis(equip_list, proxy)
                # if out_time_range or data.get('is_last_page', True) or self.next_page >= 100:
                # 判断是否一轮爬取结束了 1: 当前爬取的数据由超过三天时间 2：爬取已经是最后一页了 3. 爬取到了第一百页
                if out_time_range or self.end_round(data) or self.next_page >= 100:
                    Logger.cls_error.debug('%s第%s轮结束了 耗时:%s 第%s页 ' % (self.order_info['order_id'], self.rounds, time.time() - self.page_one_time, self.next_page))
                    self.rounds += 1
                    self.next_page = 1
                else:
                    self.next_page += 1

                if proxy != {}:
                    ProxyManager.return_proxy(proxy)
                break
            except (NotTarget, IPBanned, json.JSONDecodeError, OterStatus, ProxyError, StatusNot200) as e:
                if proxy != {}:
                    # self.task_manager.proxy_manager.delete_proxy(proxy)
                    ProxyManager.delete_proxy(proxy)
            except (ChunkedEncodingError, TooManyRedirects, SystemBusy, ConnectTimeout,
                    ConnectionError, ReadTimeout) as e:
                if proxy != {}:
                    ProxyManager.return_proxy(proxy, e.__class__.__name__)
            except Empty as e:
                Logger.cls_error.exception('空的**************>>>%s' % url)
                self.next_page = 1
                self.rounds += 1
                # gevent.sleep(60)
                if proxy != {}:
                    ProxyManager.return_proxy(proxy)
                break
            except ParamsError as e:
                if proxy != {}:
                    ProxyManager.return_proxy(proxy)
            except:
                Logger.cls_error.exception('发生未知错误**************>>>%s' % url)
                exit()

    def end_round(self, data):
        """判断一轮是否爬取结束了"""
        if not self.use_count_url:
            return data.get('is_last_page', True)
        else:
            pager = data.get('pager', {})
            return pager.get('cur_page') == pager.get('total_pages')


    def handle_with_exception(self, e):
        pass


    def get_header(self):
        return {
            'User-Agent': random.choice(self.user_agent_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }

    def public_check(self, response, crawl_url):
        """
        解析数据
        """
        if response.status_code != 200 or not response.ok:
            # self.task_manager.Logger.cls_error.info('%s-%s-%s' % (crawl_url, response.status_code, proxy))
            raise StatusNot200
        # 根据域名判断是否来源服务器的返回
        if self.splithost(response.url) != self.crawl_host:
            # self.task_manager.Logger.cls_error.info('%s-%s-%s' % (crawl_url, response.status_code, proxy))
            raise NotTarget

    def analysis(self, equip_list, proxy):
        """分析数据"""
        price_down_list = []  # 降价的数据
        insert_list = []  # 插入的数据
        update_list = []  # 更新的数据

        out_time_range = False
        # 描述爬取到数据后根据是否 降价提醒， 是否第一轮显示 来处理元数据
        for equip in equip_list:
            # 爬取的数据不是时间范围内的
            if self.crawl_data_deadline(equip['selling_time']):
                out_time_range = True
                continue
            eid = equip.get('eid', '')
            equip_dict = {}
            if self.use_count_url:
                other_info = json.loads(equip['other_info'])
            for key in self.template_field:
                # 有些数据是存放在元数据中的other_info中
                if key == 'icon':
                    if self.order_info['service_id'] in (1, 3): # 召唤兽
                        equip_dict[key] = equip.get('equip_type', "")
                    elif self.order_info['service_id'] == 2: # 角色
                        equip_dict[key] = equip.get('icon', "")
                    continue
                    # elif self.order_info['service_id'] == 3:
                    #     equip_dict[key] = equip.get('equip_type')
                if key == 'selling_time':
                    equip_dict[key] = datetime.datetime.strptime(equip.get(key) ,'%Y-%m-%d %H:%M:%S')
                    continue
                if key == 'highlight' and self.use_count_url:
                    equip_dict[key] = equip.get('highlights')
                    continue
                if key == 'price' and self.use_count_url:  # price_int
                    equip_dict[key] = equip.get('price_int')
                    continue
                if key in self.template_other_field and self.use_count_url:
                    if key == 'accept_bargain':  # 可能会没有这个值
                        equip_dict[key] = other_info.get(key, False)
                    elif key == 'subtitle':
                        equip_dict[key] = equip['equip_level_desc']
                    elif key == 'desc_sumup_short':
                        equip_dict[key] = other_info['summary']
                else:
                    val = equip.get(key, '')
                    if type(val) == bool:
                        equip_dict[key] = val
                    else:
                        equip_dict[key] = str(val)
            # equip_dict = dict((key, str(equip.get(key, '')) if equip.get(key, '') not in (True, False)
            #                   else equip.get(key, '') ) for key in self.template_field)
            # 判断上架情况
            if self.use_count_url:
                equip_dict['status_desc'] = '公示期' if equip.get('fair_show_end_time_left') != '5分钟' else '已上架'
            else:
                equip_dict['status_desc'] = equip.get('status_desc')
                if equip_dict['status_desc'] not in ('公示期', '上架中'):   # 还有未上架  会造成错误
                    continue
            # todo 1. 所有的通知需要的数据在爬取的脚本里面获取(复杂，且不稳定)  2. 只向redis推送order_id, 一切信息从数据库中获取(稳定，准确，消耗性能)
            equip_dict.update({
                'update_time': datetime.datetime.now(),
                'order_id': self.order_info['order_id'],
                'user_id': self.order_info['user_id'],
            })
            equip_dict['update_time'] = datetime.datetime.now()
            equip_dict['order_id'] = self.order_info['order_id']
            equip_dict['user_id'] = self.order_info['user_id']
            equip_dict['service_id'] = self.order_info['service_id']
            # 内存存储爬取过的数据，用来判断重复爬取数据是否更新
            unique_dict = dict((x, equip_dict[x]) for x in self.update_field)
            if eid not in self.set_dict:
                insert_list.append(equip_dict)
                self.set_dict[eid] = unique_dict
            elif unique_dict != self.set_dict[eid]:
                if int(unique_dict['price']) < int(self.set_dict[eid]['price']):
                    # todo 或者这里可以不用修改is_display  而是在展示的时候不过滤is_display
                    equip_dict['is_display'] = 1  # 如果这条数据是第一轮被隐藏的数据 降价需要显示出来
                    equip_dict['old_price'] = self.set_dict[eid]['price']  # 记录原先的价格
                    price_down_list.append(equip_dict)
                else:
                    update_list.append(equip_dict)
                self.set_dict[eid] = unique_dict
        if insert_list:
            for item in insert_list:
                # 第一轮的数据不展示
                # 这里就算不是第一轮也要不能想用默认的不显示赋值is_display 否则插入{..}和{...,is_display:0}是会报错的
                item['is_display'] = 0 if self.rounds == 1 and not self.order_info['first_round_push'] else 1
            need_push = (self.rounds != 1 or self.order_info['first_round_push']) and self.push_type is not None  # 是否需要推送
            self.task_manager.queue.put({'sql_type': 'insert',  'equip_list': insert_list, 'crawl_type': self.crawl_type,
                                         'order_id': self.order_info['order_id'], 'umobile': self.order_info['umobile'],
                                         'push_type': self.push_type, 'memo': self.order_info['memo'],
                                         'need_push': need_push})
        # 更新数据操作
        if update_list:
            self.task_manager.queue.put({'sql_type': 'update',  'equip_list': update_list, 'crawl_type': self.crawl_type})

        if price_down_list:
            # 插入价格更新表
            need_push = self.order_info['price_down_push'] == 1 and self.push_type is not None
            self.task_manager.queue.put({'sql_type': 'price_down', 'equip_list': price_down_list, 'crawl_type': self.crawl_type,
                                         'order_id': self.order_info['order_id'], 'push_type': self.push_type,
                                         'umobile': self.order_info['umobile'], 'memo': self.order_info['memo'],
                                         'need_push': need_push})

        return out_time_range

        # 0.011M  一个进程worker差不多增加25M  不指定-c 则占用600M  改用gevent则少得多
        # self.logger.debug.info('当前占用内存大小:set>>>%s, self>>>%s' % (sys.getsizeof(self.set_dict) / 1024 / 1024, sys.getsizeof(self) / 1024 / 1024))

    @staticmethod
    def splithost(url):
        """解析url的域名"""
        res = _hostprog.match(url)
        return res.group(1) if res else None

    def data_serialize(self, l):
        for item in l:
            for k, v in item.items():
                if isinstance(v, (datetime.datetime, list)):
                    item[k] = str(v)
        return l

    def different_check(self, data, proxy):
        raise ValueError(u'请在子类中重写prvite_parse方法')

    def get_crawled_eid_list(self):
        """
        从Mysql获取已经爬取的id, price
        """
        assert ValueError('请重写这个方法')

    def crawl_data_deadline(self, strtime):
        """判断爬取的记录是否在 时间范围内的 比如 3天内"""
        return datetime.datetime.now() - datetime.datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S') >= self.order_info['time_range']


class BBCrawl(Base_Crawl):
    data_model = CbgCrawlData
    # 定义插入数据库的模板
    template_field= ['subtitle', 'collect_num', 'serverid', 'selling_time', 'eid', 'equip_name', 'icon',
                     'price', 'accept_bargain', 'desc_sumup_short', 'area_name', 'server_name', 'highlight', 'game_ordersn']
    template_other_field = ['accept_bargain', 'subtitle', 'status_desc', 'desc_sumup_short']  # 支持count的url 这些字段需要在other_info中获取
    # 用来判断重复爬取的时候数据有没有更新
    update_field = ['collect_num', 'selling_time', 'price', 'accept_bargain']
    price_down_field = ['collect_num', 'selling_time', 'price', 'status_desc', 'accept_bargain', 'is_display', 'old_price']
    crawl_type = 'bb'

    def __init__(self, *args, **kwargs):
        super(BBCrawl, self).__init__(*args, **kwargs)
        self.vaild_status = 1  # 成功返回数据
        self.ban_status = 2  # 爬取频繁
        self.params_wrong_status = '0'  # 爬取的数据有误 # 被封  status = 3 输入验证码

    def get_crawled_eid_list(self):
        """从数据库取出已经爬取过的数据"""
        # self.task_manager.lock.acquire()  # 这里加锁防止2014错误 和runtime_error错误  # 现在使用的是myisam 不需要担心这个错误了
        try:
            with SqlLock:
                query_list = CbgCrawlData.objects.filter(order_id=self.order_info['order_id'])\
                                                .values('eid', 'collect_num', 'selling_time', 'price',
                                                        'status_desc', 'accept_bargain')
            for d in query_list:
                self.set_dict[d['eid']] = {
                    'collect_num': d['collect_num'],
                    'selling_time': d['selling_time'],
                    'price':  d['price'],
                    'status_desc': d['status_desc'],
                    'accept_bargain': d['accept_bargain'],
                }
        except Exception as e:
            Logger.cls_error.exception('查询发生错误')
            self.get_crawled_eid_list()

    def different_check(self, data, proxy):
        """不同种类的不同检测方法
            校验爬取的状态是否正确， 以及一页数据处理之后判断下一轮行为的方法
        """
        if data.get('status') == self.ban_status:
            # self.task_manager.Logger.cls_error.error('其它的状态码----%s----%s', (data, proxy))
            raise IPBanned
        elif data.get('status') == self.params_wrong_status:
            # self.task_manager.Logger.cls_error.error('其它的状态码----%s----%s', (data, proxy))
            raise ParamsError
        elif data.get('status') != self.vaild_status:
            # self.task_manager.Logger.cls_error.error('其它的状态码----%s----%s', (data, proxy))
            raise OterStatus

class RoleCrawl(BBCrawl):
    crawl_type = 'role'

class EquipCrawl(BBCrawl):
    crawl_type = 'equip'


if __name__ == '__main__':
    import time
    import multiprocessing
    Base_Crawl.task_manager = TaskManager
    TaskManager.init(1, BBCrawl)  # 1：召唤兽
    TaskManager.init(2, RoleCrawl) # 2 : 角色
    TaskManager.init(3, EquipCrawl)  # 3: 装备
    # 开启插入数据库的进程
    queue = multiprocessing.Queue(maxsize=500)
    TaskManager.queue = queue
    p = multiprocessing.Process(target=TaskManager.do_sql, args=(queue, TaskManager.crawl_cls_list))
    p.start()
    url = 'http://recommd.xyq-android2.cbg.163.com/cgi-bin/recommend.py?act=recommd_by_role&count=100&search_type=overall_equip_search&order_by=selling_time+DESC&limit_clothes_logic=or'
    # url = 'http://recommd.xyq-android2.cbg.163.com/cgi-bin/recommend.py?act=recommd_by_role&count=100&search_type=overall_role_search&order_by=selling_time+DESC&level_min=175&level_max=175&price_min=10000000'
    # url = 'http://recommd.xyq-android2.cbg.163.com/cgi-bin/recommend.py?act=recommd_by_role&count=100&search_type=overall_role_search&order_by=selling_time+DESC&expt_fangyu=15&bb_expt_kangfa=15&limit_clothes_logic=or&expt_kangfa=15&level_max=175&fang_yu=1300&bb_expt_gongji=15&shang_hai=2000&price_max=100000000&expt_gongji=15&limit_clothes=12512%2C12498%2C12513%2C12514%2C12647%2C12646%2C12648%2C12652%2C12654%2C12653%2C12765%2C12750%2C12850%2C12767%2C13790%2C40013%2C40025%2C40023%2C40108&bb_expt_fangyu=15&skill_dazao=100&bb_expt_fashu=15&level_min=160&pet_type_list=1&xiangrui_list=%E6%98%9F%E5%8D%8E%E9%A3%9E%E9%A9%AC%2C%E7%94%9C%E8%9C%9C%E7%8C%AA%E7%8C%AA%2C%E7%8E%89%E8%84%82%E7%A6%8F%E7%BE%8A%2C%E9%A3%9E%E5%A4%A9%E7%8C%AA%E7%8C%AA%2C%E7%A5%9E%E8%A1%8C%E5%B0%8F%E9%A9%B4&race=2'
    c = TaskManager.init_crawl_obj(3, url, {'push_type': '', 'order_id': 39, 'price_down_push': True, 'time_range': {'days': 1}, 'umobile': '18221410984',
     'user_id': 10, 'memo': '', 'end_time': '2018-07-31 15:43:02', 'first_round_push': True, 'service_id': 3})
    try:
        c.run()
    except KeyboardInterrupt:
        pass

# server_name = equip['server_name']
# serverid = equip['serverid']
# area_name = equip['area_name']
# time_left = equip['time_left']
# price = equip['price']
# nickname = equip['seller_nickname']
# collect_num = equip['collect_num']
# eid = equip['eid']
# create_time = equip['create_time']
# data_dict = {
#     'server_name': server_name,
#     'serverid': serverid,
#     'area_name': area_name,
#     'time_left': time_left,
#     'price': price,
#     'nickname': nickname,
#     'collect_num': collect_num,
#     'eid': eid,
#     'create_time': create_time,
#     'dest_url': 'http://xyq.cbg.163.com/equip?s={0}&eid={1}'.format(serverid, eid),
#     'crawl_time': datetime.datetime.now(),
#     'order_id': self.order_id,
# }

