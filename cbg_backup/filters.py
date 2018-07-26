import json
from django.db import transaction
import datetime
from unit.utility import obj_2_json, Prpcrypt, queryset_to_list_of_dict
from cbg_backup import settings
import time


def time_now(_):
    return time.time()

def start_with(o, s):
    return o.startswith(s)


def round_2(param, format='%.2f'):
    return format % (int(param) / 100)


def hide_phone_number(phone_number):
    return phone_number[:3] + '*'*4 + phone_number[-4:]


def obj_2_json_str(obj, support_fields=None):
    """把orm对象转为json"""
    return json.dumps(obj_2_json(obj, support_fields, support_json=True))


def sms_token(_):
    """返回短信的token"""
    return Prpcrypt.encrypt('%s_BS(@**' % time.time())


def get_wait_message(user_id, type_):
    """获取未读取的redis信息"""
    if not user_id:
        return
    if type_ == 'all':
        return int(settings.redis3.hget('user_message', 'notic:%s' % user_id) or 0) + \
               int(settings.redis3.hget('user_message', 'offer:%s' % user_id) or 0)
    else:
        return int(settings.redis3.hget('user_message', '%s:%s' % (type_, user_id)) or 0)


@transaction.atomic
def get_lottery_times(user):
    """获取每日抽奖的剩余次数"""
    from activity.models import CbgLottery1
    today = datetime.date.today()
    try:
        lottery = CbgLottery1.objects.select_for_update().get(user=user)
        if lottery.last_lottery_time != today:
            lottery.last_lottery_time = today
            lottery.lottery_times = 3
            lottery.save()
    except CbgLottery1.DoesNotExist:
        lottery = CbgLottery1.objects.create(lottery_times=3, last_lottery_time=today, user=user)
    return lottery.lottery_times


def json_dumps(obj):
    return json.dumps(obj)


def queryset_to_js(queryset):
    return queryset_to_list_of_dict(queryset, support_json=True)


def get_mine_redis_data(request):
    """获取mine页面所有redis中的数据"""
    user_id = request.user.id
    pip = settings.redis3.pipeline()
    # 消息
    pip.hget('user_message', 'notic:%s' % user_id)
    pip.hget('user_message', 'offer:%s' % user_id)
    # 订单
    pip.hget('user_order_count', 'wait:%s' % user_id)
    pip.hget('user_order_count', 'doing:%s' % user_id)
    result = pip.execute()
    notic = int(result.pop(0) or 0)
    offer = int(result.pop(0) or 0)
    wait = int(result.pop(0) or 0)
    doing = int(result.pop(0) or 0)
    return [notic + offer, wait, doing]


