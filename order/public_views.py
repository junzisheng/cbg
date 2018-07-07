from unit.utility import *
from unit import gpub
from crawl_celery.tasks import crawl_task



url = """http://xyq-android2.cbg.163.com/app2-cgi-bin/app_search.py?act=super_query&search_type=overall_pet_search&order_by=selling_time+DESC&is_baobao=1"""

@gpub.wglobal(need_login=True, allow_tuple=('GET'), ajax=True)
def test(request, response, render):
    crawl_task.delay('bb', url, {
        'order_id': 430,
        'memo': '哈哈',
        'umobile': '18221410984',
        'user_id': 1,
        'push_type': '短信;',
        'end_time': datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), '%Y-%m-%d %H:%M:%S'),
        'time_range': {'days': 3},
        'first_round_push': 1,
        'price_down_push': 1,
    })
    return render_to_error_response(request, response, render, '123123')








    








