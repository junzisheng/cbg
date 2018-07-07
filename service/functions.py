from urllib import parse

from cbg_backup import settings


def bb_params_handle(params, service_time):
    """召唤兽上传的数据处理"""
    args = {}
    for k, v in params.items():
        if not v:
            continue
        if k in ('is_baobao', 'skill_with_suit') and v in (True, 'true'):
            args[k] = 1
        elif type(v) == list:
            args[k] = ','.join(v)
        elif k in ('price_min', 'price_max'):
            args[k] = int(float(v) * 100)
        elif k == 'growth':  # 成长必须时俩位小数
            args[k] = int(float(v) * 1000)
        elif v:
            args[k] = v
    url_arg = parse.urlencode(args)  # 将参数转为url参数
    return  '召唤兽提醒服务' , settings.BB_BASE_URL_SEARCH + url_arg  # 组装爬取的url


def equip_params_handel(params, service_time):
    """装备上传数据处理"""
    pass
    return  '装备提醒服务' % service_time, settings.BB_BASE_URL_SEARCH + url_arg  # 组装爬取的url


def role_params_handel(params, service_time):
    """人物上传数据处理"""
    return  '角色提醒服务' % service_time, settings.BB_BASE_URL_SEARCH + url_arg  # 组装爬取的url
