import os
import datetime
import traceback
import sys
import time
from urllib import parse
from django.db import connections
from django.http import HttpResponse
from .models import Webrequest, WebrequestMysql
from unit.functions import normal_request, mysql_execute
from cbg_backup import settings

through_path_list = ['/user/qrcode', '/favicon.ico']  # 不处理的path


class CpuUsage(object):
    """计算cpu占用的时间 jiffies"""
    def __init__(self, pid=None):
        self.pid = pid or os.getpid()
        self.last_stat = [0, 0, 0, 0]  # 用户态， 核心态， waited-for用户态， waited-for核心态
        self.is_linux = sys.platform == 'linux2'
        self.start()

    def start(self):
        """查询当前cpu资源使用状态"""
        if self.is_linux:
            data_proc_stat = open('/proc/%s/stat' % self.pid, 'rb').read().split()
            self.last_stat = [int(x) for x in data_proc_stat[13:17]]

    def usage(self, b_update_newest=False):
        """与最近一次查询"""
        if self.is_linux:
            data_proc_stat = open('/proc/%s/stat' % self.pid, 'rb').read().split()
            current_stat = [int(x) for x in data_proc_stat[13:17]]
            delta_stat = [y - x for y, x in zip(current_stat, self.last_stat)]
            if b_update_newest:
                self.last_stat = delta_stat
            return delta_stat
        return [0, 0, 0, 0]


class WebRequestMonitor(object):
    """监测一个http请求的消耗时间"""
    def __init__(self):
        pass

    def process_request(self, request):
        # 获取前端报文发送的时间
        http_cost = -1
        if request.path not in through_path_list:
            b, http_cost = normal_request(request)
        request.__track__ = {
            'http_cost': http_cost,
            'handle_before': time.time(),  # 记录处理请求前的时间
            'cpusage': CpuUsage()
        }
        return None

    def process_response(self, request, response):
        if request.path in through_path_list:
            return response
        cpu_usage = request.__track__['cpusage'].usage()
        awr = Webrequest()
        awr.host = request.META.get('HTTP_HOST', "")
        awr.http_cost = request.__track__['http_cost']
        awr.path_info = request.META.get('PATH_INFO', "")[:128]
        awr.query_string = parse.unquote(request.META.get('QUERY_STRING' , ''))[:128]
        awr.timestamp = datetime.datetime.now()
        awr.duration = time.time() - request.__track__['handle_before']
        awr.cpu_all = sum(cpu_usage)
        db_log_list = self.mysql_log(awr)
        awr.save()
        for db_log in db_log_list:
            db_log.awr_id = awr.id
        WebrequestMysql.objects.bulk_create(db_log_list)
        return response


    def mysql_log(self, awr):
        """计算mysql使用的消耗"""
        awr.db_count = 0
        awr.db_duration_total = 0
        awr.db_duration_max = 0
        awr.db_rows = 0
        db_log_list = []
        for django_conn in connections.all():  # connections.all(): {'defalut': {}}
            cursor = connections[django_conn.alias].cursor()  # django_conn.alias: 'defult'
            count_query = len(django_conn.queries)  # 获取所有的数据库操作
            for x in django_conn.queries[:count_query]:
                if 'mysql' not in django_conn.settings_dict['ENGINE']:
                    continue
                try:
                    # 处理查询语句
                    if x['sql'].startswith('SET'):  # django会自动执行 set sql_auto_isnull = true  这个在1.11会修复
                        continue
                    if x['sql'].startswith('SELECT'):
                        ret_exps = mysql_execute(None, 'EXPLAIN ' + x['sql'], cursor)
                        for ret_exp in ret_exps:  # for是为了子查询或者join
                            if ret_exp.table in ('django_session', 'auth_user'):
                                continue
                            awrsql = WebrequestMysql()
                            awrsql.timestamp = None
                            awrsql.duration = float(x['time'])
                            awrsql.db_alias = django_conn.alias
                            awrsql.db_server = django_conn.settings_dict['HOST']
                            awrsql.db_server = django_conn.settings_dict['NAME']
                            awrsql.table_name = ret_exp.table
                            awrsql.sql = x['sql'][:2048]
                            awrsql.exp_select_type = ret_exp.select_type
                            awrsql.exp_type = ret_exp.type
                            awrsql.exp_row = ret_exp.rows or 0
                            awrsql.exp_extra = ret_exp.extra
                            awrsql.exp_posibblekey = (ret_exp.possible_keys or '')[:128]
                            awrsql.exp_key = ret_exp.key
                            awrsql.exp_key_table = ret_exp.table
                            awr.db_rows += awrsql.exp_row
                            if ret_exp.key:
                                # 获取表中使用该索引的字段
                                ret_idx = mysql_execute(None ,
                                                        """SELECT INDEX_SCHEMA , SEQ_IN_INDEX , COLUMN_NAME
                                                             FROM information_schema.STATISTICS
                                                            WHERE INDEX_NAME = '%s' AND TABLE_NAME = '%s'
                                                         ORDER BY SEQ_IN_INDEX""" % (ret_exp.key , ret_exp.table), cursor)
                                awrsql.exp_key_detail = ','.join(idx.column_name for idx in ret_idx)
                            else:
                                awrsql.exp_key_detail = ''
                            db_log_list.append(awrsql)
                    else:
                        awrsql = WebrequestMysql()
                        awrsql.timestamp = None
                        awrsql.duration = float(x['time'])
                        awrsql.db_alias = django_conn.alias
                        awrsql.db_server = django_conn.settings_dict['HOST']
                        awrsql.db_name = django_conn.settings_dict['NAME']
                        awrsql.sql = x['sql'][:2048]
                        db_log_list.append(awrsql)
                except Exception as e:
                    raise e
                    settings.log_error.exception('mysql数据收集发生错误>>>>%s' % x['sql'])
                awr.db_count += 1
                awr.db_duration_total += float(x['time'])
                awr.db_duration_max = max(awr.db_duration_max, float(x['time']))
        return db_log_list



