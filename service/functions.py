from urllib import parse

from cbg_backup import settings


def bb_params_handle(params):
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
    return settings.BB_BASE_URL_SEARCH + url_arg  # 组装爬取的url


def role_params_handel(params):
    """角色上传数据处理"""
    args = {}
    for k, v in params.items():
        if not v:
            continue
        elif type(v) == list:
            args[k] = ','.join(v)
        elif k in ('price_min', 'price_max'):
            args[k] = int(float(v) * 100)
        elif v:
            args[k] = v
    url_arg = parse.urlencode(args)  # 将参数转为url参数
    return settings.ROLE_BASE_URL_SEARCH + url_arg  # 组装爬取的url

def equip_params_handel(params):
    """装备上传数据处理"""
    args = {}
    if params.get('level_min') == 60 and params.get('level_max') == 160:
        params.pop('level_min')
        params.pop('level_max')
    for k, v in params.items():
        if not v:
            continue
        elif type(v) == list:
            args[k] = ','.join(v)
        elif k in ('price_min', 'price_max'):
            args[k] = int(float(v) * 100)
        elif v:
            args[k] = v
    url_arg = parse.urlencode(args)  # 将参数转为url参数
    return settings.EQUIP_BASE_URL_SEARCH + url_arg  # 组装爬取的url
