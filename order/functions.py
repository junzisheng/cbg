import hashlib
from django.conf import settings


def ppz_signature(price, type, order_id, order_info, redirect):
    """生成paypay猪第三方支付的签名
    @param: type 1微信 2支付宝
    """
    param = {
        'api_user': settings.PPZ['api_user'],
        'price': price,
        'type': type,
        'redirect': redirect,
        'order_id': order_id,
        'order_info': order_info,
    }
    param_keys = list(param.keys())
    param_keys.sort()
    param_str = settings.PPZ['api_key']
    for key in param_keys:
        param_str += str(param[key])
    return hashlib.md5(param_str.encode()).hexdigest()


def paysapi_signature(price, istype, orderid, orderuid, goodsname, notify_url, return_url):
    """生成条状payapi第三方支付网页所需的post参数"""
    param = {
        'goodsname': goodsname,
        'istype': istype,
        'notify_url': notify_url + '?istype=%s' % istype,
        'orderid': orderid,
        'orderuid': orderuid,
        'price': price,
        'return_url': return_url,
        'token': settings.PAYS_API['token'],
        'uid': settings.PAYS_API['uid'],
    }
    param_keys = list(param.keys())
    param_keys.sort()
    to_signature_str = ''
    for key in param_keys:
        to_signature_str += str(param[key]).lower()
    param['key'] = hashlib.md5(to_signature_str.encode()).hexdigest()
    return param


# def check_paysapi_notify_signature(payapi_id, orderid, price, realprice, orderuid, signature):
def check_paysapi_notify_signature(params):
    """payapi回调生成签名"""
    key = params.pop('key')
    params['token'] = settings.PAYS_API['token']
    param_keys = list(params.keys())
    param_keys.sort()
    to_signature_str = ''
    for k in param_keys:
        to_signature_str += str(params[k]).lower()
    signature = hashlib.md5(to_signature_str.encode()).hexdigest()
    return signature == key
