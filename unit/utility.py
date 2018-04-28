#encoding=utf-8
import re
import types
import datetime
import json
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from unit import gpub
import configparser
try:
    from cbg_backup import settings
except:
    from cbg_backup.cbg_backup import settings
import os

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


def render_to_response(request, response, render, template_name):
    template = get_template(template_name)
    response.write(template.render(render, request=request))
    return response


def ip_visit_limit(user_ip , key_prefix , num , unit_time):
    """
    判断同一IP访问次数
    :param user_ip      :   用户ip
    :param key_prefix   :   访问类型前缀
    :param num          :   访问次数上限
    :param unit_time    :   多长时间，单位秒
    :return             :
    """
    key = "%s_%s" % (key_prefix ,user_ip)
    new_val = gpub.redis3.incr(key)
    if new_val == 1:
        settings.redis3.expire(key, unit_time)
    return new_val > num


def validate_nick_name(nick_name):
    for func in [_validate_nick_name_len, _validate_nick_name_limit_word]:
        flag, msg = func(nick_name)
        if not flag:
            return msg
    return None


def strip_html(nick_name):
    # 去除html标签
    html_regx = u"\<[\\]?[a-zA-Z]+\>|\\n|\\t|\\f|\\r|\\v"

    return re.sub(html_regx, "", nick_name).strip()


def _validate_nick_name_limit_word(nick_name, config_limit_word=None):
    config_limit_word = MyConfigParser(os.path.join(settings.BASE_DIR, 'cbg_backup', 'limitword.ini'))
    if not config_limit_word:
        return True, ""
    for section in [u'MINGANCI', u'ZANGHUA', u'YUNYING']:
        regx_str = u"|".join(config_limit_word[section])
        limit_word = ",".join(re.findall(regx_str, nick_name, re.IGNORECASE))
        if limit_word:
            return False, u"包含不合法词:%s" % limit_word
    return True, u""


def _validate_nick_name_len(nick_name):
    # 只保留中英文数字
    t_nick_name = "".join(re.findall(u"[\u4e00-\u9fa5a-zA-Z0-9]", nick_name))
    if not t_nick_name:
        return False, u"昵称应该包含中英文和数字"
    min = 4
    if re.search(u"[\u4e00-\u9fa5]", t_nick_name):
        min = 2
    if len(t_nick_name) < min:
        return False, u"中文至少要2位或英文至少4位"
    # 分成中文字符 和其他字符串
    chinese_str = "".join(re.findall(u"[\u4e00-\u9fa5]", nick_name))
    other_str = "".join(re.findall(u"[^\u4e00-\u9fa5]", nick_name))
    nick_name_len = len(chinese_str) * 2 + len(other_str)
    if nick_name_len > 16:
        return False, u"长度超过限制,中文最多8个字，字母和数字最多16位"
    return True, ""



class MyConfigParser(configparser.ConfigParser):
    """继承configparser来重写optionxform使其区分大小写"""
    _instance = None
    _init = None
    def __init__(self, path ,defaults=None):
        if self._init:
            return
        configparser.ConfigParser.__init__(self,defaults)
        self.read(path, encoding='utf-8')

    def optionxform(self, optionstr):
        return optionstr

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MyConfigParser, cls).__new__(cls)
        return cls._instance

    def __getitem__(self, item):
        assert item in self.sections()
        return self.options(item)

# def get_current_url(request , full_domain = False , quote_path = False , quote_query = False):
#     """取得当前Request请求的URL，full_domain控制是否获取完整的全路径
#     . 在一些需要登录跳转的地方经常会被用到
#     """
#     url_cur = request.path if full_domain else request.get_full_path()
#     # url_cur  = urllib2.quote(request.META['PATH_INFO'].encode('utf8')) if quote_path else request.META['PATH_INFO']
#
#     query    = ('?' + request.META['QUERY_STRING']) if request.META.get('QUERY_STRING' , None) else ''
#     url_cur += urllib2.quote(query) if quote_query else query
#
#     return (request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST']) + url_cur





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
    # from sys import getsizeof
    # i = IProxyManager()
    # i.bulk_insert([[0, 1, 2, 3, 2]])
    # i.bulk_insert([[0, 1, 2, 3, 1]])
    # i.bulk_insert([[1, 1, 2, 3, 5]])
    # i.bulk_insert([[0, 1, 2, 3, 8]])
    # i.bulk_insert([[0]])
    # i.single_insert([3,1,2,3, 10])
    # i.single_insert([5])
    # s = i.select()
    # print(s)
    # print(getsizeof(i))
    # print(len(i))
    # i.single_remove([3,1,4,3])
    # i.bulk_remove([[0, 1, 2, 3], [1,2,3,45]])
    a = MyConfigParser(os.path.join(settings.BASE_DIR, 'cbg_backup', 'limitword.ini'))
    print(validate_nick_name('你妈B'))










