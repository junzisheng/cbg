from order.models import CbgOrders
from crawl_celery.models import CbgCrawlData
from unit.decoration import ajax_refresh
from unit.utility import *
from unit.dtlib import FDT2


def crawl_data_page(request, response, render, order_id):
    if not CbgOrders.objects.filter(user_id=request.user.id, id=order_id, is_delete=0).exists():
        return HttpResponse('您没有该订单')
    render['order_id'] = order_id
    return render_to_response(request, response, render, 'order/crawl_data_page.html')


@ajax_refresh(order_limit=('-id',), filter_limit={'old_price__isnull': 'False|True', 'order_id_1': '\d+'})
def crawl_data_api(request, response, render):
    """获取爬取的数据"""
    # todo 记录用户最近一次查看的时间， 超过这个时间的都是最新的
    offset, order_by, int_limit, filter_ = render['query_params']
    filter_['is_display'] = 1
    filter_['user_id'] = request.user.id
    queryset = CbgCrawlData.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_)
    # 几天前 todo
    for data in queryset:
        data['price'] = '%.2f' % (int(data['price']) / 100)
        if data['old_price']:
            data['old_price'] = '%.2f' % (int(data['old_price']) / 100)
        try:
            data['highlight'] = eval(data['highlight'])
        except:
            data['highlight'] = ''
        data['selling_time'] = date_gap_personal(dtlib.DT2(data['selling_time']), render['timenow'])
    return {'query_list': queryset}


def delete_crawl_data_api(request, response, render):
    try:
        del_id_list = request.GET.get('del_id_list', '[]')
        order_id = request.GET.get('order_id')
        del_id_list = json.loads(del_id_list)
        CbgCrawlData.objects.filter(order_id=order_id, id__in=del_id_list, user_id=request.user.id) \
            .update(is_display=0)
        return response_json(retcode='SUCC', msg='删除成功')
    except Exception as e:
        return response_json(retcode='FAIL', msg='ERROR_ID_LIST', description='删除失败')

