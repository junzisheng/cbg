import time
import json
import re

from cbg_backup import settings
from .utility import response_json, Prpcrypt, to_list, queryset_to_list_of_dict
from user.functions import sms_ip_send, sms_can_repeat, check_phone_number
from service.models import Banner
from unit.cache import RedisKeyCache
from libraries.qiniu import Auth


def ajax_refresh(order_limit=('-id',), int_limit=15, filter_limit={}):
    """ajax增量刷新的接口装饰器
       filter:{} 规则  1.可以为空 2.value为正则表达式 3.key以_1为结尾表示传过来的filter参数必须要有这个数
       True, False >>> 'True' 'False'
    """
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            request = args[0]
            render = kwargs['render']
            method_obj = getattr(request, request.method)
            order_by = method_obj.get('order_by', '-id')
            try:
                filter_ = json.loads(method_obj.get('filter', '{}'))
                offset = int(method_obj.get('offset', 0))
            except:
                return response_json(retcode='FAIL', description='错误的请求！', msg="ErrorFilterParams")
            order_change = method_obj.get('order_change', False)
            # 禁止非法过滤
            vaild_filter = {}
            if set(filter_.keys()) - set([_x[:-2] if _x.endswith('_1') else _x for _x in filter_limit.keys()]):
                return response_json(retcode='FAIL', description='错误的请求！', msg="LegalFilter")
            for _k, _v in filter_limit.items():
                if _k.endswith('_1') and _k[:-2] not in filter_: # 校验必须要有的过滤字段
                    return response_json(retcode='FAIL', description='错误的请求！', msg="WithoutFilterParams")
                vaild_k = _k[:-2] if _k.endswith('_1') else _k
                if vaild_k in filter_:  # 检验过滤参数的格式
                    if not re.match(_v, str(filter_[vaild_k])):
                        return response_json(retcode='FAIL', description='错误的请求！', msg="WithoutFilterParams")
                    vaild_filter[vaild_k] = filter_[vaild_k] if filter_[vaild_k] not in ('True', 'False') else eval(filter_[vaild_k])

            if order_by not in order_limit:  # 校验合法order参数
                return response_json(retcode='FAIL', description='错误的请求！', msg="LegalOrder")

            # 当修改排序规则的时候，offset置为0
            if order_change:
                offset = 0
            render['query_params'] = (offset, (order_by,), int_limit, vaild_filter)
            result = func(*args, **kwargs)
            result['is_last'] = len(result['query_list']) < int_limit  # 是否已经是最后的数据了， 当然如果正巧是最后15个话，可能会浪费一次请求， 但问题不大
            result['offset'] = offset + len(result['query_list'])
            return response_json(retcode='SUCC', **result)
        return _wrapper
    return _decorate


def sms_send(func):
    """发短信的前置装饰器"""
    def _wrapper(*args, **kwargs):
        render = kwargs['render']
        render['token'] = Prpcrypt.encrypt('%s_BS(@**' % time.time())
        return func(*args, **kwargs)
    return _wrapper


def sms_check(username_str, sms_repeat_deadline):
    """校验发送短信的参数是否正确"""
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            request = args[0]
            render = kwargs['render']
            method_obj = getattr(request, request.method)

            ip = request.META.get('REMOTE_ADDR', '')
            # 校验token
            token = method_obj.get('token', '_')
            type = method_obj.get('type')
            if type not in ('register', 'currency_pay'):
                return response_json('FAIL', description='非法访问', msg='UnlegalVisit')
            try:
                token = Prpcrypt.decrypt(token) or '_'
                t, salt = token.split('_')
                if salt != 'BS(@**':
                    return response_json('FAIL', description='非法访问', msg='UnlegalVisit')
                if time.time() - int(float(t)) >= 180:
                    return response_json('FAIL', description='token过期', msg='TokenExpired')
            except:
                return response_json('FAIL', description='非法访问', msg='UnlegalVisit')
            # 校验ip频率
            if sms_ip_send(ip):
                return response_json('FAIL', description='ip短信发送受限', msg='IpSmsMaxed')
            # 检验时限内是否重复发送
            username = method_obj.get(username_str, '')
            if type in ('register',) and not check_phone_number(username):
                return response_json('FAIL', description='错误的请求', msg='PhoneReFail')
            if type not in ('register',):
                if not render['user_login']:
                    return response_json('FAIL', description='错误的请求', msg='HasSend')
                username = request.user.username
            if sms_can_repeat(username or request.user.username, type, sms_repeat_deadline):
                return response_json('FAIL', description='已经发送过短信', msg='HasSend')
            result = func(*args, **kwargs, username=username)
            return result
        return _wrapper
    return _decorate


def banner(key):
    """获取banner的信息"""
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            tag_list = to_list(key)
            render = kwargs['render']
            redis_cache = RedisKeyCache(key_prefix='banner')
            banner_list = redis_cache.get('banner_list')
            if banner_list is None:
                banner_list = []
                for banner in Banner.objects.filter(tag__in=tag_list, is_delete=0):
                    # 处理需要删除的
                    if render['timenow'] >= banner.deadline_time:
                        banner.delete()
                    else:
                        banner_list.append(banner)
                # 计算缓存时间
                # timeout = min([_x.deadline_time.timestamp() -  render['timenow'].timestamp() for _x in banner_list]) \
                #     if banner_list else 60 * 60 * 24  # 没有相应的banner 缓存 24h
                redis_cache.set('banner_list', banner_list, timeout=60 * 60 * 24, version=redis_cache.incr_version())
            banner_list = [_x for _x in banner_list if _x.start_time < render['timenow'] and _x.deadline_time > render['timenow']]
            render['banner_list'] = json.dumps(queryset_to_list_of_dict(banner_list, support_json=True))
            return func(*args, **kwargs)
        return _wrapper
    return _decorate


def accept_token(type):
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            request = args[0]
            render = kwargs['render']
            type_list = to_list(type)
            if 'qiniu' in type_list:
                q = Auth(settings.qiniu['AK'], settings.qiniu['SK'])
                # 上传策略
                file_name = 'image/%s/' % request.user.id
                policy = {
                    'scope': '%s:%s' % (settings.qiniu['ImageBucket'], file_name),  # 仅能已/user/user_id/为前缀的文件名
                    'isPrefixalScope': 1,
                    'insertOnly': 1, # 只能新增，不能修改,
                    'fsizeLimit': 2 * 1024 * 1024,  # 最大2m,
                    'mimeLimit': 'image/*',  # 限制上传的格式,
                }
                token = q.upload_token(settings.qiniu['ImageBucket'], None, expires=3600, policy=policy)
                render['qiniu_token'] = token
                render['qiniu_domain'] = settings.qiniu['Domain']
                render['qiniu_buccket'] = settings.qiniu['ImageBucket']
            return func(*args, **kwargs)
        return _wrapper
    return _decorate






