#encoding=utf-8
import time
import random
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from unit.utility import *
# from .models import *
import json
import threading
ip_manager = IProxyManager()

def insert(requests, IProxyManager):
    """添加"""
    # ip = requests.GET.get('ip')
    # port = requests.GET.get('port')
    if requests.method != 'POST':
        return HttpResponseBadRequest()
    proxy_list = requests.POST.get('proxy_list')
    try:
        proxy_list = json.loads(proxy_list)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()
    IProxyManager.bulk_insert(proxy_list)
    r = IProxyManager.proxy_.id
    time.sleep(random.randint(0,3))
    return HttpResponse(r)


def delete(requests, IProxyManager):
    if requests.method != 'POST':
        return HttpResponseBadRequest()
    try:
        _id_list = requests.POST.getlist('id_list')
        _id_list = [{'id': int(_x)} for _x in _id_list]
        IProxyManager.bulk_remove(_id_list)
        return HttpResponse(len(IProxyManager))
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def select(requests, IProxyManager):
    """"""
    if requests.method != 'GET':
        return HttpResponseBadRequest()
    operate = requests.GET.get('operate')  # use: 是否增加proxy的使用次数 reverse: use的
    use = False if operate == 'check' else True
    try:
        count = int(requests.GET.get('count', 20))
    except:
        return HttpResponseBadRequest()
    return JsonResponse(IProxyManager.select(count=count,  # 选取的数量
                                             serialize=True, # use正反序
                                             use=use,  # use是否增加次数
                                             ),
                        safe=False)
#
#
# def data_insert(requests):
#     """批量插入数据"""
#     if requests.method != 'POST':
#         return HttpResponseBadRequest()
#     data_list = requests.POST.getlist('data_list')
#     bulk_list = []
#     for data_dict in data_list:
#         bulk_list.append(data_dict)
#         bulk_list.append(CrawlData(**data_dict))
#     CrawlData.objects.bulk_create(bulk_list)
#     response_json(retcode='SUCC', description=u'数据插入成功')
#
#
# def data_update(requests):
#     """批量更新数据"""








