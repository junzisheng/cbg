import redis
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed
import traceback
try:
    from cbg_backup import settings
except:
    from cbg_backup.cbg_backup import settings
import datetime
from unit.utility import response_json
# import logging
# log_info = logging.getLogger('django')
# log_info.log('123', msg="", level=1)
# exit()
import time

redis3 = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=3)
redis2 = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=2)

class ExceptionHTTPResponse(Exception):
    pass


def wglobal(need_login=False, allow_tuple=None, ajax=False):
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            _request = args[0]
            if ajax and not _request.is_ajax():
                raise Http404
            if allow_tuple and _request.method not in allow_tuple:
                raise Http404
            request_start = time.time()
            _args = list(args)
            response = HttpResponse()
            _args.append(response)
            wsgi_url_scheme = _request.META['wsgi.url_scheme']
            render = {
                'request': _request,
                'settings': settings,
                'urlnow': wsgi_url_scheme + '://' + _request.META['HTTP_HOST'] + _request.get_full_path(),  # 请求的完整路径
                'timenow': datetime.datetime.now(),
                'DOMAIN': settings.DOMAIN,
                'user_login': _request.user.is_authenticated(),
                'is_staff': False,
                'super_user': False,
            }
            # render.update(settings.RENDER_BASE)  # 可以使用django.settings中的公共CONTEXT
            build_render_enviorment_by_request(_request, render)

            if need_login and not render['user_login']:
                if _request.is_ajax():
                    return response_json('FAIL', command='LOGIN')
                else:
                    return HttpResponseRedirect('/user/login?redirect=%s' % render['urlnow'])

            if render['user_login'] and _request.user.is_staff:
                render['is_staff'] = True
            if render['user_login'] and _request.user.is_superuser:
                render['super_user'] = True
            _args.append(render)
            try:
                ret_val = func(*_args, **kwargs)
                ret_code = ret_val.status_code
            except ExceptionHTTPResponse as e:
                ret_val = e.args[0]
                ret_code = ret_val.status_code
            except Exception as r:
                print(r)
                _request._cache_exception = traceback.format_exc()
                ret_code = 500
                raise
            finally:
                time_tick = time.time() - request_start
                info_log  = u'%6d %s (%s-%s-%s) %s %s %s' % (int(time_tick * 1000000) ,
                                                             _request.user.username if _request.user.is_authenticated() else '*' ,
                                                             _request.META['REMOTE_ADDR'] ,
                                                             render['browser'] or 'browser' ,
                                                             render['platform'],
                                                             ret_code , render['urlnow'] ,
                                                             _request.META.get('HTTP_REFERER' , ''))
                # log_info.log(log_info)
                print(info_log)

            return ret_val

        return _wrapper
    return _decorate















def build_render_enviorment_by_request(request , render):
    """根据请求初始化RENDER中的全局环境变量"""
    user_agent  = request.META['HTTP_USER_AGENT'].lower() if 'HTTP_USER_AGENT' in request.META else ''

    render['browser'] = 'PC'
    if 'micromessenger' in user_agent or request.REQUEST.get('weixin'):
        render['browser'] = 'weixin'
    # 判断出浏览器的平台：iPad、iPhone、iPod, Android、Windows Phone, MQQBrowser（QQ手机浏览器）
    # 将上述都设置为移动类型，其他都是非移动类型
    render['ismobile'] , render['platform'] = None , None
    for key in ('ipad' , 'iphone' , 'ipod' , 'android'):
        if key in user_agent:
            render['ismobile'] , render['platform'] = True , key
            break

    if render['ismobile'] is None:
        if 'windows phone' in user_agent:
            render['ismobile'] , render['platform'] = True , 'winphone'

        elif 'mqqbrowser' in user_agent or request.REQUEST.get('qq' , ''):
            render['ismobile'] , render['platform'] = True , 'qq'

        else:
            render['ismobile'] , render['platform'] = False , 'pc'

    # 为显示挑选显示模板，目前是直接取browser值
    # render['screen']   = render['browser'] if render['browser'] else ('mobile' if render['ismobile'] else 'pc')
    render['browser']  = 'mobile' if render['ismobile'] else render['browser']
    #render['basehtml'] = 'platform/%s/base.html' % render['screen']

    # 对于代理访问，用户源地址在HTTP_X_FORWARDED_FOR或者HTTP_REMOTEIP中
    cdn_remote_host = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_REMOTEIP')

    if cdn_remote_host and cdn_remote_host != request.META['REMOTE_ADDR']:
        slb_forward = cdn_remote_host.split(',')
        request.META['REMOTE_ADDR'] = slb_forward[0].strip()

        if len(slb_forward) > 1:
            request.META['HTTP_X_FORWARDED_BY'] = slb_forward[1].strip()

