#encoding=utf-8
import time
import random
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from unit.utility import IProxyManager
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



