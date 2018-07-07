import json
from unit.utility import obj_2_json
import time


def time_now(_):
    return time.time()

def start_with(o, s):
    return o.startswith(s)


def round_2(param, format='%.2f'):
    return format % (int(param) / 100)


def hide_phone_number(phone_number):
    return phone_number[:3] + '*'*4 + phone_number[-4:]


def obj_2_json_str(obj, support_fields):
    return json.dumps(obj_2_json(obj, support_fields, support_json=True))


