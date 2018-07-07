from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    nickname = models.CharField(max_length=32, blank=True)
    sex         = models.CharField(max_length=10, blank=True)
    age         = models.CharField(max_length=20, blank=True)
    head_image  = models.CharField(max_length=100, blank=True)
    v           = models.CharField(max_length=16, blank=True)
    introduce   = models.CharField(max_length=600, blank=True)
    alias       = models.CharField(max_length=60, blank=True)
    attr        = models.CharField(max_length=128, blank=True)
    comment_limit = models.DateTimeField(null=True, blank=True)
    points      = models.IntegerField(null=True, blank=True,default=0)
    auto_country = models.CharField(max_length=32, blank=True)
    auto_province = models.CharField(max_length=32, blank=True)
    auto_city   = models.CharField(max_length=32, blank=True)
    auto_district = models.CharField(max_length=32, blank=True)
    be_used_points   = models.IntegerField(null=True, blank=True,default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency      = models.IntegerField(null=True, blank=True,default=0)  # 货币
    give_currency = models.IntegerField(null=True, blank=True,default=0)

    class Meta:
        db_table = 'user_profile'


class AliSmsQueue(models.Model):
    """阿里短信"""
    mobilephone = models.CharField(max_length=20)
    type = models.CharField(max_length=16, null=True, blank=True)  # 短信的类别 1.注册码 2.上架通知 3.降价通知
    template_code = models.CharField(max_length=32, blank=True,)  # 短信模板
    sign_name = models.CharField(max_length=32)  # 短信签名
    params = models.CharField(max_length=256)  # 短信的内容   "{'code': '123'}"
    create_time = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    error_log = models.CharField(max_length=526, blank=True, null=True)  # 出错的日志
    class Meta:
        db_table = 'ali_sms_queue'


class EmailQueue(models.Model):
    """邮件队列"""
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)  # 发送对象
    type = models.CharField(max_length=16, null=True, blank=True)  # 邮件的发送类型 1.降价 2.上架
    message = models.CharField(max_length=1024)  # 内容
    create_time = models.DateTimeField(auto_created=True)  # 发送时间



