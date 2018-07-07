from django.db import models


class Webrequest(models.Model):
    """记录一次请求的cpu, redis, mysql, http报文时间进行统计"""
    host = models.CharField(max_length=32, blank=True)
    http_cost = models.FloatField()  # http请求耗时
    path_info = models.CharField(max_length=128, blank=True)
    query_string = models.CharField(max_length=128, blank=True)
    timestamp = models.DateTimeField()
    duration = models.FloatField(null=True, blank=True)
    cpu_all = models.FloatField(null=True, blank=True)
    localredis_cpu_all = models.FloatField(null=True, blank=True)
    db_count = models.IntegerField(null=True, blank=True)
    db_duration_total = models.FloatField(null=True, blank=True)
    db_rows = models.IntegerField(null=True, blank=True)
    db_duration_max = models.FloatField(null=True, blank=True)
    redis_count = models.IntegerField(null=True, blank=True)
    redis_duration_total = models.FloatField(null=True, blank=True)
    redis_duration_max = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'webrequest'


class WebrequestMysql(models.Model):
    """请求的mysql使用统计"""
    awr = models.ForeignKey(Webrequest)
    timestamp = models.DateTimeField()
    duration = models.FloatField(null=True, blank=True)
    db_alias = models.CharField(max_length=16, blank=True)
    db_server = models.CharField(max_length=32, blank=True)
    db_name = models.CharField(max_length=16, blank=True)
    table_name = models.CharField(max_length=32, blank=True)
    sql = models.CharField(max_length=2048, blank=True)
    exp_select_type = models.CharField(max_length=32, blank=True)
    exp_type = models.CharField(max_length=32, blank=True)
    exp_row = models.IntegerField(null=True, blank=True)
    exp_extra = models.CharField(max_length=32, db_column='exp_Extra', blank=True)
    exp_posibblekey = models.CharField(max_length=64, blank=True)
    exp_key = models.CharField(max_length=32, blank=True)
    exp_key_detail = models.CharField(max_length=64, blank=True)
    exp_key_table = models.CharField(max_length=32, blank=True)
    class Meta:
        db_table = 'webrequest_mysql'


class WebrequestRedis(models.Model):
    awr = models.ForeignKey(Webrequest)
    timestamp = models.DateTimeField()
    duration = models.FloatField(null=True, blank=True)
    host = models.CharField(max_length=32, blank=True)
    db = models.IntegerField(null=True, blank=True)
    classname = models.CharField(max_length=32, blank=True)
    method = models.CharField(max_length=32, blank=True)
    args = models.CharField(max_length=128, blank=True)
    kwargs = models.CharField(max_length=128, blank=True)
    retval = models.CharField(max_length=128, blank=True)
    class Meta:
        db_table = 'webrequest_redis'
