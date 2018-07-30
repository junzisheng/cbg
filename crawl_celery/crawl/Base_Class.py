import sys
import json
import time
import logging
from gevent.lock import BoundedSemaphore
from multiprocessing import Queue
import gevent
import copy
from crawl_celery.models import Proxy
from share.setting_share import ALI_SMS
from cbg_backup import settings


def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            Logger.cls_error.exception('ip连接池错误')
            return False
    return wrapper


# 读写数据库操作对象
# write_sql_tool = SqlHelper(1)  # sql对象 这里根据读写分为俩个会话  原则是在 数据库操作同一个会话不能够并发， 因为库里面可能又未知的bug
# read_sql_tool = write_sql_tool  # 分俩个会话是没有用的，只要在线程中，异步就可能同时调用_rfile.read()这个不可重入函数
SqlLock = BoundedSemaphore(1)

class Set(list):
    """一个实现去重的列表"""
    def add(self, item):
        if item not in self:
            self.append(item)

    def extend(self, l):
        for item in l:
            self.add(item)

    def remove(self, item):
        """安全地remove"""
        if item in self:
            #Logger.cls_error.info('remove------------%s' % item)
            super(Set, self).remove(item)


class ProxyDict(dict):
    """自定义的继承dict的代理用的字典"""
    def __eq__(self, other):
        return self['ip'] == other['ip'] and other['port'] == self['port']


class Logger(object):
    """简单的日志类"""
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # console
    cls_console_handler = logging.StreamHandler(sys.stdout)
    # file
    cls_error_file_handler = logging.FileHandler('cbg_crawl.error.log')
    cls_error_file_handler.setFormatter(formatter)
    cls_error = logging.getLogger('crawl_gpub')

    cls_error.addHandler(cls_console_handler)
    cls_error.addHandler(cls_error_file_handler)
    cls_error.setLevel(logging.DEBUG)

    def __init__(self, log_file):
        self.console_handler = logging.StreamHandler(sys.stdout)
        # self.debug_file_handler = logging.FileHandler('/home/gwj/log/%s.debug.log' % log_file)
        # self.debug_file_handler.setFormatter(self.formatter)

        # self.error_file_handler = logging.FileHandler('/home/gwj/log/%s.error.log' % log_file)
        # self.error_file_handler.setFormatter(self.formatter)

        # debug模式
        self.debug = logging.getLogger('crawl_debug')
        # self.debug.addHandler(self.debug_file_handler)
        self.debug.addHandler(self.console_handler)
        self.debug.setLevel(logging.DEBUG)

        # error模式
        self.error = logging.getLogger('crawl_error')
        # self.error.addHandler(self.error_file_handler)
        self.error.addHandler(self.console_handler)
        self.error.setLevel(logging.DEBUG)


class ProxyManager(object):
    """和远程服务器通信的类"""
    last_local_ip_use_time = 0  # 记录最近一次使用本地ip的时间戳
    local_ip_uses = 0  # 记录使用本地ip的总次数
    local_ip_lock = BoundedSemaphore(1)  # 使用本地ip需要加锁， 防止被封
    local_ip_interval = 2  # 使用本地ip的间隔

    proxy_set = Set()  # 当前还剩的代理队列
    using_proxy_set = Set() # 在用代理队列
    mem_proxy_set = Set()  # 缓存代理
    delete_proxy_list = list()  # 等待删除的代理

    @classmethod
    def get_proxy_list(cls, recursive=False):
        """
        从数据库中获取足够的代理
        当代理不够的时候，从缓存代理列表中补充代理， 然后再从数据库中补充到缓存代理
        这么做的原因是避免直接从数据库中获取代理， 因为这样会导致所有的协成都需要等待这个io， 导致协成不停的切换并且都满足
        （代理不够的条件从而走到这个函数中，导致多次请求数据库）
        """
        if len(cls.proxy_set) >= 5:
            return
        Logger.cls_error.info('当前ip使用情况 未使用:%s 使用中:%s' % (len(cls.proxy_set), len(cls.using_proxy_set)))
        # 如果是递归进来的 先休眠1s中
        if recursive:
            gevent.sleep(1)

        cls.proxy_set.extend([proxy for proxy in cls.mem_proxy_set if proxy not in cls.using_proxy_set])  # 将缓存的ip放入池中
        Logger.cls_error.info('获取缓存ip之后情况 未使用:%s 使用中:%s' % (len(cls.proxy_set), len(cls.using_proxy_set)))

        try:
            # 先将废弃的proxy删除
            if len(cls.delete_proxy_list):
                cls.delete_proxy(None, 0)
            with SqlLock:
                query = Proxy.objects.all().values('ip', 'port')[:len(TaskManager.crawl_obj_list)*20]
                cls.mem_proxy_set = Set([ProxyDict([('ip', q['ip']), ('port', q['port']), ('uses', 0), ('last_time', 0), ('successes', 0)])
                                         for q in query])
            Logger.cls_error.info('获取了%s个缓存代理' % len(cls.mem_proxy_set))
        except:
            Logger.cls_error.exception('获取代理发生错误-------------')
        finally:
            cls.get_proxy_list(recursive=True)

    @classmethod
    def select_proxy(cls, use_local_ip):
        """根据失败次数来考虑是否使用本地ip 并且同一时间只有一个协程序能够使用本地ip
           优先级是： 1.使用次数越多，越优先使用，2.俩次使用的间隔时间必须要大于2s 保证统一个代理爬取频率不是很高
        """
        cls.get_proxy_list()
        if use_local_ip:
            with cls.local_ip_lock:
                Logger.cls_error.info('获取本地ip中-----------')
                while True:
                    time_left = time.time() - cls.last_local_ip_use_time
                    # 本地ip俩秒一次的频率不会被封
                    if time_left > cls.local_ip_interval:
                        cls.last_local_ip_use_time = time.time()
                        cls.local_ip_uses += 1
                        Logger.cls_error.info('使用了本地ip, 已使用了%s次' % cls.local_ip_uses)
                        return {}
                    else:
                        gevent.sleep(time_left + 0.00001)
        # 从代理池中获取代理
        cls.proxy_set.sort(key=lambda x: x['successes'], reverse=True)
        now = time.time()
        vaild_proxy_list = [proxy for proxy in cls.proxy_set if now - proxy['last_time'] >= cls.local_ip_interval]  # 为了保护每一个ip 每个ip使用的间隔时间需要超过一定的时间
        _proxy = cls.proxy_set.pop(cls.proxy_set.index(vaild_proxy_list[0])) if vaild_proxy_list else cls.proxy_set.pop()
        # _proxy = cls.proxy_set.pop(0)
        _proxy['uses'] += 1
        # 放到使用队列中
        cls.using_proxy_set.add(_proxy)
        return _proxy

    @classmethod
    def create_vaild_proxy(cls, proxy):
        """将代理构建成为requests可用的形式"""
        return proxy and {
            'https': 'https://%s:%s' % (proxy['ip'], proxy['port']),
            'http': 'http://%s:%s' % (proxy['ip'], proxy['port']),
        }

    @classmethod
    def delete_proxy(cls, proxy, count=10):
        """删除"""
        if proxy:
            cls.using_proxy_set.remove(proxy)
            cls.proxy_set.remove(proxy)
            cls.delete_proxy_list.append(proxy['ip'])
        if len(cls.delete_proxy_list) == 0 or proxy and len(cls.delete_proxy_list) <= count:
            return
        Logger.cls_error.info('删除代理:%s个' % len(cls.delete_proxy_list))
        delete_ip_list = list()
        try:
            # 这里需要先清空整个列表 否则所有的协成会堵塞在这儿
            delete_ip_list = copy.deepcopy(cls.delete_proxy_list)
            cls.delete_proxy_list.clear()
            with SqlLock:
                delete_count = Proxy.objects.filter(ip__in=delete_ip_list).delete()
                Logger.cls_error.debug('删除了%s个代理' % delete_count)
        except:
            cls.delete_proxy_list = list(set(cls.delete_proxy_list + delete_ip_list))
            Logger.cls_error.exception('删除代理发生错误')

    @classmethod
    def return_proxy(cls, proxy, wrong=None):
        """归还使用过的代理, 并统计这个代理引发异常的次数
            当发生的异常与使用次数达到一定比列的次数，物理删除这个代理
        """
        if not proxy:
            return
        cls.using_proxy_set.remove(proxy)
        proxy['last_time'] = time.time()
        if wrong:
            proxy[wrong] = proxy.get(wrong, 0) + 1
            # 根据一定的规则判断是否删除这个代理
            if proxy['uses'] >= 5 and proxy[wrong] / proxy['uses'] >= 0.5:
                Logger.cls_error.info('代理出错达到上限 已经删除 %s' % proxy)
                cls.delete_proxy(proxy)
            else:
                cls.proxy_set.add(proxy)
        else:
            proxy['successes'] += 1
            cls.proxy_set.add(proxy)


class TaskManager(object):
    """爬取的入口"""
    crawl_cls_list = list()  # 存放的所有的爬取类
    crawl_obj_list = list()  # 存放所有的爬取对象

    type_crawl_cls_dict = dict()  # 爬取对象与爬取类的映射: {'bb': BbCrawl}
    queue = Queue()  # 存放了所有的爬取数据，在一个进程中统一处理

    @classmethod
    def init(cls, type_, crawl_cls):
        """初始化任务管理对象"""
        cls.crawl_cls_list.append(crawl_cls)
        cls.type_crawl_cls_dict[type_] = crawl_cls

    @classmethod
    def init_crawl_obj(cls, type_, *args, **kwargs):
        """初始化一个爬取对象, 并进行管理"""
        _obj = cls.type_crawl_cls_dict[type_](*args, **kwargs)
        cls.crawl_obj_list.append(_obj)
        return _obj


    @classmethod
    def sms_notic(cls, order_id, umobile, _type):
        """通知给用户"""
        pass

    @classmethod
    def do_sql(cls, queue, cls_crawl_list):
        """一个进程函数， 用来将所有爬取到的数据插入到数据库中"""
        # 存放每种爬取类型的数据
        _type_task_dict = {}
        for _cls in cls_crawl_list:
            _type_task_dict[_cls.crawl_type] = {
                'insert': list(),
                'update': list(),
                'price_down': list(),
                'model': _cls.data_model,
                'price_down_field': _cls.price_down_field,
                'update_field': _cls.update_field,
            }
        # task_list = []
        n = 0
        try:
            while True:
                task_list = []
                type_task_dict = copy.deepcopy(_type_task_dict)
                while 1:  # 这里用empty判断是不准确， 因为在不断的Put 可能
                    # task: {'sql_type': 'insert', 'equip_list': [{}, {}], 'crawl_type': 'bb'}
                    # Logger.cls_error.info('sql is alive')
                    try:
                        task_list.append(queue.get_nowait())
                    except:
                        break
                    # 控制任务数量， 防止一次性插入的数据过多， 或者消费速度小于生产速度导致无线循环而不会插入到数据库中
                    if len(task_list) >= 20:
                        break
                if not task_list:
                    time.sleep(1)
                    continue
                # 清理数据
                sms_push_dict = {}  # {order_id: {}}
                weixin_dict = {'insert': [], 'down': []}
                timestamp = time.time()
                for task in task_list:
                    sql_type = task['sql_type']
                    type_task_dict[task['crawl_type']][sql_type].extend(task['equip_list'])
                    if sql_type == 'update' or task['need_push'] is False:
                        continue
                    if '短信' in task['push_type']:
                        memo = task['memo'][:15] if len(task['memo']) <= 15 else task['memo'][:15] + '...'
                        push_type = '上架' if sql_type == 'insert' else '降价'
                        params = {'memo': memo, 'push': push_type, 'oid': task['order_id']}
                        if task['order_id'] not in sms_push_dict:
                            sms_push_dict[task['order_id']] = dict(
                                umobile=task['umobile'],
                                template_code=ALI_SMS['Push']['template_code'],
                                sign_name=ALI_SMS['Push']['sign_name'],
                                params=json.dumps(params),
                                deadline= timestamp + 60*5,
                                type='【%s】' % push_type,
                            )
                        elif push_type not in sms_push_dict[task['order_id']]['type']:
                            sms_push_dict[task['order_id']]['type'] = sms_push_dict[task['order_id']]['type'][:-1] + '-' + push_type + '】'
                # sql操作， 插入到数据库中
                for crawl_type, _task in type_task_dict.items():
                    _Model = _task['model']
                    insert_list = _task['insert']
                    update_list = _task['update']
                    price_down_list = _task['price_down']
                    # 批量插入
                    if insert_list:
                        bulk_list = []
                        for data in insert_list:
                            bulk_list.append(_Model(**data))
                            weixin_dict['insert'].append( (data['game_ordersn'], data['serverid']) )
                        # bulk_list = [_Model(**data) for data in insert_list]
                        _Model.objects.bulk_create(bulk_list)
                        Logger.cls_error.info('插入了%s条数据' % len(insert_list))
                    # 更新
                    for data in update_list:
                        update_field = dict((_k, data[_k]) for _k in _task['update_field'])
                        _Model.objects.filter(user_id=data['user_id'], order_id=data['order_id'], eid=data['eid'])\
                                      .update(**update_field)
                    # 价格刷新
                    for data in price_down_list:
                        weixin_dict['down'].append( (data['game_ordersn'], data['serverid']) )
                        price_down_field = dict((_k, data[_k]) for _k in _task['price_down_field'])
                        _Model.objects.filter(user_id=data['user_id'], order_id=data['order_id'], eid=data['eid']) \
                            .update(**price_down_field)
                        Logger.cls_error.info('降价了%s条数据' % len(insert_list))
                # if sms_push_dict:
                #     sms_push_list = [_x for _x in sms_push_dict.values()]
                #     settings.redis2.publish('sms_notify', json.dumps(sms_push_list))
                    # 微信通知

                if weixin_dict['insert'] or weixin_dict['down']:
                    settings.redis2.publish('weixin_notic', json.dumps(weixin_dict))  #{'insert': [(),()], price: [(),()]}

        except:
            Logger.cls_error.exception('数据库操作发生了错误')
            exit()
