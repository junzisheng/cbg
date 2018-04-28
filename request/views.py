# encoding=utf-8
import json
from urllib import parse

from django.http import HttpResponse
from django.shortcuts import render
import config
from .models import CrawlOrders
from .tasks import crawl_task


def role_page(request):
    return render(request, 'crawl_url/role.html')

def bb_page(request):
    return render(request, 'crawl_url/bb.html')


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
    memo = request.POST.get('note')
    o = CrawlOrders.objects.create(memo=memo)
    # 发布新的爬取url
    crawl_task.delay(_role_crawl_url, o.id, memo)
    return HttpResponse('<a href="%s">%s</a>' % (_role_crawl_url, _role_crawl_url))

