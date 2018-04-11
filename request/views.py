# encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from config import config
from urllib import parse
import json
from .tasks import crawl_task



def role_page(request):
    return render(request, 'crawl_url/role.html')


def role_crawl_rul(request):
    """
    获取【人物】爬取的url
    """
    # todo  由于未知原因 前端js部分有编码问题 暂时不支持祥瑞等中文查询数据
    # 拼接爬取的字符串
    _role_crawl_url = config.ROLE_BASE_URL_SEARCH
    # cbg的接口是写死的 不是从前端获取的
    # act = request.POST.get('act')
    args = json.loads(request.POST.get('args'))
    url_arg = parse.urlencode(args)
    _role_crawl_url += 'act=%s&' % config.ROLE_ACT
    _role_crawl_url += url_arg
    # 发布新的爬取url
    config.REDIS_1.publish('role_url', _role_crawl_url)
    crawl_task.delay(_role_crawl_url)
    return HttpResponse('<a href="%s">%s</a>' % (_role_crawl_url, _role_crawl_url))
