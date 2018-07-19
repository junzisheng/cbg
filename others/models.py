from django.db import models
from django.contrib.auth.models import User


class Problems(models.Model):
    """收集用户上传的问题"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, null=True, blank=True)  # 问题的种类
    subtype = models.CharField(max_length=64, null=True, blank=True)  # 子问题
    title = models.CharField(max_length=128, null=True, blank=True)  # 问题的标题
    detail = models.CharField(max_length=512, null=True, blank=True)  # 问题的详情
    img_list = models.CharField(max_length=2560, null=True, blank=True)  # 图片的路径 用;分割
    create_time = models.DateTimeField(auto_now=True)
    accept = models.BooleanField()  # 是否被采纳
    read_time = models.DateTimeField()  # 查阅的事件
    is_read = models.BooleanField(default=0)  # 是否已经查阅过了

    class Meta:
        db_table = "cbg_problems"
        ordering = ['-id']