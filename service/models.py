# encoding:utf8
from django.db import models
from core.models import BaseModel




class Banner(models.Model):
    tag = models.CharField(max_length=16)  # 标识banner
    href = models.CharField(max_length=512)  # banner链接
    img_url = models.CharField(max_length=512)  # banner图片链接
    brief = models.CharField(max_length=128, null=True, blank=True)  # banner的文字简介
    create_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()  # 启用时间
    deadline_time = models.DateTimeField()  # 截至时间
    weight = models.SmallIntegerField()  # 显示的权重
    is_delete = models.BooleanField(default=0)  # 是否被删除

    class Meta:
        db_table = 'banner'




# class Jct5AssessWebrequest(models.Model):
#     id = models.AutoField(primary_key=True, db_column='ID') # Field name m
#     host = models.CharField(max_length=32L, blank=True)
#     path_info = models.CharField(max_length=128L, blank=True)
#     query_string = models.CharField(max_length=128L, blank=True)
#     timestamp = models.DateTimeField()
#     duration = models.FloatField(null=True, blank=True)
#     cpu_all = models.FloatField(null=True, blank=True)
#     localredis_cpu_all = models.FloatField(null=True, blank=True)
#     db_count = models.IntegerField(null=True, blank=True)
#     db_duration_total = models.FloatField(null=True, blank=True)
#     db_rows = models.IntegerField(null=True, blank=True)
#     db_duration_max = models.FloatField(null=True, blank=True)
#     redis_count = models.IntegerField(null=True, blank=True)
#     redis_duration_total = models.FloatField(null=True, blank=True)
#     redis_duration_max = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = 'jct5_assess_webrequest'




