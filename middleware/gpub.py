import sys
import time
import datetime

from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response

from cbg_backup import settings
from unit.utility import response_json, render_to_error_response
from unit.cache import RedisKeyCache
from service.models import CbgService


class PublicMiddleWare(MiddlewareMixin):
    """视图处理之前的预处理"""
    def process_view(self, request, view_func, args, kwargs):
        if settings.DEBUG is False and request.path.startswith(settings.STATIC_URL):
            return None
        # xadmin也不需要处理
        if request.path.startswith('/xadmin'):
            return None
        args = list(args)
        check_active = kwargs.pop('check_active') if 'check_active' in kwargs else True
        allow_method = kwargs.pop('allow_method') if 'allow_method' in kwargs else None
        need_login = kwargs.pop('need_login') if 'need_login' in kwargs else False
        need_ajax = kwargs.pop('ajax') if 'ajax' in kwargs else False
        if settings.DEBUG is False:
            # 对ajax请求进行校验
            if request.is_ajax() is False and need_ajax is True:
                return HttpResponseForbidden()
            # 对视图允许的请求方法进行校验
            if allow_method and request.method not in allow_method:
                return HttpResponseForbidden()

        response = HttpResponse()
        wsgi_url_scheme = request.META['wsgi.url_scheme']
        render = {
            'request': request,
            'settings': settings,
            'urlnow': wsgi_url_scheme + '://' + request.META['HTTP_HOST'] + request.get_full_path(),  # 请求的完整路径
            'timenow': datetime.datetime.now(),
            'DOMAIN': settings.DOMAIN,
            'user_login': request.user.is_authenticated,
            'is_staff': False,
            'super_user': False,
            'time': time,
        }
        self.build_render(render)
        # 校验是否需要登陆
        if need_login is True and not render['user_login']:
            if request.is_ajax():
                return response_json('FAIL', msg='LOGIN', description='请先登陆')
            else:
                return HttpResponseRedirect('/user/login?redirect=%s' % render['urlnow'])

        # 校验用户的账号是否被封
        if render['user_login']:
            if check_active is True and request.user.is_active == 0:
                if request.is_ajax():
                    return response_json('FAIL', msg='Ban', description='账号已被封禁，如有疑问，请联系管理员')
                else:
                    return render_to_error_response(request, response, render, '账号已被封禁，如有疑问，请联系管理员')
            render['is_staff'] = request.user.is_staff == 1
            render['super_user'] = request.user.is_superuser == 1
        self.build_render_enviorment_byrequest(request, render)
        request.__render__ = render
        kwargs['response'] = response
        kwargs['render'] = render
        return None

    def process_response(self, request, response):
        if not hasattr(request, '__render__'):
            return response
        render = request.__render__
        view_cost = time.time() - request.__track__['handle_before']
        info_log  = u'%6d %s (%s-%s-%s) %s %s' % (view_cost ,
                                                  request.user.username if request.user.is_authenticated else '未登录',
                                                  request.META['REMOTE_ADDR'] ,
                                                  render['browser'] or 'browser' ,
                                                  render['platform'],
                                                  render['urlnow'] ,
                                                  request.META.get('HTTP_REFERER' , '')
                                                  )
        settings.log_django.info(info_log)
        return response

    def process_exception(self, request, exception):
        # 有异常django会处理， 所以不需要写日记了
        if request.user.is_superuser and settings.DEBUG is False:
            return technical_500_response(request, *sys.exc_info())

    def build_render(self, render):
        """对render加一些补丁"""
        # 获取服务
        redis_cache = RedisKeyCache(key_prefix='service')
        service_list = redis_cache.get('service_list')
        if service_list is None:
            service_list = list(CbgService.objects.filter(is_display=1))
            redis_cache.set('service_list', service_list, timeout=60 * 60 * 24, version=redis_cache.incr_version())
        render['service_list'] = service_list

    def build_render_enviorment_byrequest(self, request , render):
        """根据请求初始化RENDER中的全局环境变量"""
        user_agent  = request.META['HTTP_USER_AGENT'].lower() if 'HTTP_USER_AGENT' in request.META else ''
        render['browser'] = 'PC'
        if 'micromessenger' in user_agent or request.GET.get('weixin'):
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

            elif 'mqqbrowser' in user_agent or request.GET.get('qq' , ''):
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


