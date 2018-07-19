import re
import json
import time
import string
import random
import datetime
from unit.utility import obj_2_json
from cbg_backup import settings
from .models import AliSmsQueue

phone_number_re = re.compile(r'1[3|4|5|8|7|6|9]\d{9}$')

sms_config_dict = {
    'register': {
        'template_code': settings.ALI_SMS['Verification']['template_code'],
        'sign_name': settings.ALI_SMS['Verification']['sign_name'],
    },
    'currency_pay': {
        'template_code': settings.ALI_SMS['Verification']['template_code'],
        'sign_name': settings.ALI_SMS['Verification']['sign_name'],
    },
    'modify_pwd': {
        'template_code': settings.ALI_SMS['Verification']['template_code'],
        'sign_name': settings.ALI_SMS['Verification']['sign_name'],
    }
}


def check_phone_number(phone_number):
    """校验手机号码格式"""
    return phone_number_re.match(phone_number)


def sms_ip_send(user_ip):
    """
     判断同一IP24小时内短信发送是否超过限制100次
    :param user_ip  : 用户IP
    :return:
    """
    key = "sms_ip_%s" % user_ip
    new_val = settings.redis3.incr(key)
    if new_val == 1:
        settings.redis3.expire(key, 60 * 60 * 24)
    return new_val > 100


def ip_visit_limit(user_ip, key_prefix, num, unit_time):
    """
    判断同一IP访问次数
    :param user_ip      :   用户ip
    :param key_prefix   :   访问类型前缀
    :param num          :   访问次数上限
    :param unit_time    :   多长时间，单位秒
    :return             :
    """
    key = "%s_%s" % (key_prefix, user_ip)
    new_val = settings.redis3.incr(key)
    if new_val == 1:
        settings.redis3.expire(key, unit_time)
    return new_val > num


def send_ali_sms(username, _type):
    """阿里验证码"""
    key = "%s_captcha_%s" % (_type, username)
    num_str = ''.join(random.sample(string.digits, 4))
    # 保存验证码和手机号 5分钟有效
    settings.redis3.set(key, num_str)
    settings.redis3.expire(key, "300")
    params = {'code': num_str}
    sms = dict(
            umobile=username,
            template_code=sms_config_dict[_type]['template_code'],
            sign_name=sms_config_dict[_type]['sign_name'],
            params=json.dumps(params),
            deadline=time.time() + 60*5,
            type=_type,
        )
    # 数据提交后通知redis订阅客户端处理
    settings.redis3.publish('sms_notify', json.dumps([sms,]))
    return num_str


def sms_can_repeat(username, prefix, deadline=60):
    """判断短信是否可以重新发送"""
    key = "%s_captcha_%s" % (prefix, username)
    return settings.redis3.ttl(key) > deadline
