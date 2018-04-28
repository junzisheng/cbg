#-*- coding: utf8 -*-

import os
import sys
import re
import traceback
import datetime


FMT_DT2 = '%Y-%m-%d %H:%M:%S'
RE_DT2  = re.compile('^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}) (?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})$')
RE_DT2X = re.compile('^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}) (?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2}) (?P<msecond>\d{1,3})$')
RE_DT2S = re.compile('^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2}):(?P<msecond>\d{1,3})$')

FMT_DT  = '%Y%m%d%H%M%S'
RE_DT   = re.compile('^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})$')
RE_DTX  = re.compile('^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(?P<msecond>\d{3})$')

FMT_DD2 = '%Y-%m-%d'
RE_DD2  = re.compile('^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$')

FMT_DD  = '%Y-%m'
RE_DD   = re.compile('^(?P<year>\d{4})-(?P<month>\d{1,2})$')

FDT2 = lambda dt: dt.strftime(FMT_DT2)
FDT  = lambda dt: dt.strftime(FMT_DT)
FDD2 = lambda dt: dt.strftime(FMT_DD2)
FDD  = lambda dt: dt.strftime(FMT_DD)

def __DT(dt_str , re_dt):
    # 公共的时间转换函数，使用指定的正则表达式
    # 如失败，返回None

    re_dt = re_dt.match(dt_str)
    if not re_dt:
        return None

    int_time = [int(i) for i in re_dt.groups()]
    if len(int_time) == 7:
        int_time[6] = int_time[6] * 1000
    return datetime.datetime(*int_time)

def DT2X(dt_str):
    # 转换函数，将YYYY-MM-DD HH:MM:SS mmm形式文本转换为时间对象，如失败，返回None
    return __DT(dt_str , RE_DT2X)

def DT2S(dt_str):
    # 转换函数，将YYYY/MM/DD/HH:MM:SS:mmm形式文本转换为时间对象，如失败，返回None，SMAP专用
    return __DT(dt_str , RE_DT2S)

def DT2(dt_str):
    # 转换函数，将YYYY-MM-DD HH:MM:SS形式文本转换为时间对象，如失败，返回None
    return __DT(dt_str , RE_DT2)

def DTX(dt_str):
    # 转换函数，将YYYYMMDDHHMMSSmmm形式文本转换为时间对象，如失败，返回None
    return __DT(dt_str , RE_DTX)

def DT(dt_str):
    # 转换函数，将YYYYMMDDHHMMSS形式文本转换为时间对象，如失败，返回None
    return __DT(dt_str , RE_DT)

def DD2(dd_str):
    # 转换函数，将YYYY-MM-DD形式文本转换为日期，如失败，返回None
    ret = __DT(dd_str , RE_DD2)
    if ret is None:
        return None
    else:
        return ret.date()

def DD(dd_str):
    # 转换函数，将YYYY-MM形式文本转换为日期，如失败，返回None
    ret = __DT(dd_str + '-01' , RE_DD2)
    if ret is None:
        return None
    else:
        return ret.date()

def DT2S2(dt):
    if isinstance(dt, datetime.datetime):
        return u'%d年%d月%d日' % (dt.year,dt.month,dt.day)
    return None

def DT2S3(dt):
    if isinstance(dt, datetime.datetime):
        return u'%d年%d月%d日 %02d:%02d' % (dt.year,dt.month,dt.day, dt.hour, dt.minute)
    return None

if __name__ == '__main__':
    print(DT2S2(datetime.datetime.now()))
    print(DT2S3(datetime.datetime.now()))

    str_run =   [   "DT2X('2012-03-04 12:23:34 324')" ,
                    "DT2('2012-03-04 12:23:34')" ,
                    "DT('20120304122334')" ,
                    "DD2('2012-03-04')" ,
                    "DD('2012-03')" ,
                ]

    for str in str_run:
        val = eval(str)
        print(str , '=' , val)
        print('FDT2(val) = ' , eval('FDT2(val)'))
        print('FDT(val)  = ' , eval('FDT(val)'))
        print('FDD2(val) = ' , eval('FDD2(val)'))
        print('FDD(val)  = ' , eval('FDD(val)'))
        print('-' * 30)

    print("DT2X('2012-03-04 12:23:34 324') - DT2X('2012-03-04 12:23:34 224')" , DT2X('2012-03-04 12:23:34 324') - DT2X('2012-03-04 12:23:34 224'))