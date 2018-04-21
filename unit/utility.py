#encoding=utf-8
import types
import datetime
import json
from django.http import HttpResponse

try:
    from cbg_backup.unit import dtlib
except:
    from unit import dtlib

to_list = lambda x : list(x) if isinstance(x , (tuple, dict, set, list)) else [x] if x else []


def queryset_to_list_of_dict(queryset , support_json = False):
    """将QuerySet转换为字典结构的数组，方便进行JSON转换
    . 如果指定支持JSON转化，则会将日期等类型转换
    """

    list_ret = []
    for qs in queryset:
        dict_qs = {}

        for field in qs._meta.fields:
            field_name = field[0].attname if isinstance(field , (list, tuple)) else field.attname
            field_val  = getattr(qs , field_name)

            if support_json:
                if type(field_val) == datetime.date:
                    field_val = dtlib.FDD2(field_val)

                elif type(field_val) == datetime.datetime:
                    field_val = dtlib.FDT2(field_val)


            dict_qs[field_name] = field_val

        list_ret.append(dict_qs)

    return list_ret


def response_json(retcode , description = '', **kwargs):
    """快捷函数，返回JSON格式的HttpResponse，至少提供retcode和description两个参数，和附加命名参数"""
    dict_ret = {'retcode': retcode}
    if description:
        dict_ret['description'] = description
    dict_ret.update(kwargs)
    return HttpResponse(json.dumps(dict_ret))





from threading import Lock
lock = Lock()


class Proxy(object):
    out_attr = ('ip', 'port', 'protocol', 'types', 'uses', '_id')
    id = 0

    def __init__(self, ip=None, port=None, protocol=None, types=None, u=0, speed=None, id=None):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.types = types
        self.score = 20
        self.uses = u
        self._id = id

    def __eq__(self, other):
        return self.ip == other.ip or self._id == other._id

    def __ne__(self, other):
        return True

    def __hash__(self):
        return True


def lock_manager(func):
    """对实例对象的操作进行锁控制"""
    def wrapper(*args, **kwargs):
        lock.acquire()
        r = func(*args, **kwargs)
        lock.release()
        return r
    return wrapper


class IProxyManager(object):
    container = list()
    proxy_ = Proxy
    # def __init__(self):
    #     self.container = list()

    @lock_manager
    def select(self, count=20, use=True, serialize=True, reverse=False):
        """查询
            use: 表示记录proxy的使用
        """
        self.container.sort(key=lambda x:x._id, reverse=reverse)
        proxy_list = self.container[:count]
        if use:
            for p in proxy_list:
                p.uses += 1
        return proxy_list if not serialize else self.serialize(proxy_list)

    @lock_manager
    def bulk_insert(self, proxy_list):
        """批量插入"""
        l = set(map(self.init_proxy, proxy_list))
        self.container = self.list_set(l | set(self.container))

    @lock_manager
    def single_insert(self, proxy):
        proxy = self.init_proxy(proxy, True)
        self.container.append(proxy)
        self.container = self.list_set(self.container)

    def init_proxy(self, proxy, incr_id=True):
        """实例代理对象"""
        p = Proxy(**proxy)
        if incr_id:
            p._id = self.proxy_.id = self.proxy_.id + 1
            print(p._id)
        return p

    @lock_manager
    def single_remove(self, proxy):
        proxy = self.init_proxy(proxy, incr_id=False)
        print(proxy._id)
        if proxy in self.container:
            self.container.remove(proxy)

    @lock_manager
    def bulk_remove(self, proxy_list):
        proxy_list = [self.init_proxy(p, False) for p in proxy_list]
        for p in proxy_list:
            if p in self.container:
                self.container.remove(p)

    def serialize(self, proxy_list):
        _l = []
        for p in proxy_list:
            _d = dict((k, p.__dict__[k]) for k in Proxy.out_attr)
            _l.append(_d)
        return _l

    def __iter__(self):
        return self.container

    @staticmethod
    def list_set(l):
        return list(set(l))

    def __len__(self):
        return len(self.container)




if __name__ == '__main__':
    from sys import getsizeof
    i = IProxyManager()
    i.bulk_insert([[0, 1, 2, 3, 2]])
    i.bulk_insert([[0, 1, 2, 3, 1]])
    i.bulk_insert([[1, 1, 2, 3, 5]])
    i.bulk_insert([[0, 1, 2, 3, 8]])
    i.bulk_insert([[0]])
    i.single_insert([3,1,2,3, 10])
    i.single_insert([5])
    s = i.select()
    print(s)
    # print(getsizeof(i))
    # print(len(i))
    # i.single_remove([3,1,4,3])
    # i.bulk_remove([[0, 1, 2, 3], [1,2,3,45]])










