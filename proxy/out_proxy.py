#encoding=utf-8
import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest


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
