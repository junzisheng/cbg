from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from cbg_backup import settings

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


class CbgSysInfo(BaseModel):
    """所有用户共享的系统通知"""
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # 0 表示系统消息
    content = models.CharField(max_length=256)  # 通知内容
    href = models.CharField(max_length=512)  # 链接
    thumb_img = models.CharField(max_length=512)  # 通知的缩略图
    create_time = models.DateTimeField(auto_now=True)
    display_time = models.DateTimeField()  # 消息可以展示的时间
    type = models.CharField(max_length=32)  # 通知的类型（常规通知， 优惠通知） notic, offer
    out_params = ['user_id', 'content', 'href', 'thumb_img', 'create_time']
    # is_private = models.BooleanField(default=True)  # 标识是否为公共通知

    def create(self, *args, **kwargs):
        super(CbgSysInfo, self).create(*args, **kwargs)


    class Meta:
        db_table = 'cbg_sysinfo'


class CbgUserSign(models.Model):
    """每日签到表"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    continue_days = models.SmallIntegerField(default=0)  # 持续签到的天数
    last_sign_time = models.DateField()  # 上次签到的时间
    sign_time = models.DateField(auto_now_add=True)  # 本次签到的时间

    class Meta:
        db_table = 'cbg_user_sign'







