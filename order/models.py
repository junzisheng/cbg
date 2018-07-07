from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class CrawlOrders(BaseModel):
    oid             =   models.CharField(max_length=32, blank=True)  # 订单的流水id
    service_name    =   models.CharField(max_length=126, blank=True, null=True)  # 服务名称
    uname           =   models.CharField(max_length=32, blank=True)  # 用户名
    umobile         =   models.CharField(max_length=64, blank=True)  # 用户手机号码
    uemail          =   models.CharField(max_length=12, blank=True, default='')
    memo            =   models.CharField(max_length=25, blank=True, default='')  # 备注
    price           =   models.IntegerField(null=True, blank=True)  # 价格
    real_price      =   models.IntegerField(null=True, blank=True)  # 实付价格
    points          =   models.IntegerField(null=True, blank=True)  # 使用积分
    real_points     =   models.IntegerField(null=True, blank=True)  # 真实积分
    pay_status      =   models.CharField(max_length=32, blank=True)  # 支付状态
    pay_channel     =   models.CharField(max_length=32, blank=True)  # 支付渠道
    pay_time        =   models.DateTimeField(null=True, blank=True)  # 支付时间
    pay_tradeno     =   models.CharField(max_length=64, blank=True)  # 第三方流水号
    user_id         =   models.CharField(max_length=16, null=False)
    user_ip         =   models.CharField(max_length=64, blank=True)  #
    user_agent      =   models.CharField(max_length=256, blank=True)
    create_time      =   models.DateTimeField(auto_created=True, null=True)
    status          =   models.CharField(max_length=16, blank=True) # 待付款， 进行中，已完成
    start_time      =   models.DateTimeField(null=True, blank=True)  # 开始时间
    closing_time    =   models.DateTimeField(null=True, blank=True)  # 结束时间
    crawl_url       =   models.CharField(max_length=2096, null=False)  # 爬取的url
    upload_params   =   models.TextField(max_length=10192, null=False)  # 爬取的参数
    first_round_push = models.BooleanField(default=False)
    price_down_push = models.BooleanField(default=False)
    push_type = models.CharField(max_length=108)  # 推送的方式  短信 邮件
    service_time = models.SmallIntegerField()  # 服务时间 1-30 天
    is_delete = models.BooleanField(default=False)
    free_push_times = models.SmallIntegerField(default=50)  # 免费短信推送次数
    change_params_times = models.SmallIntegerField(default=3)  # 可以更改爬取参数的次数

    out_params = ['id', 'create_time', 'status', 'closing_time', 'memo', 'real_price', 'upload_params', 'pay_time']

    class Meta:
        db_table = 'orders'
        ordering = ['-id']


class RechargeRecord(BaseModel):
    """货币充值记录"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    quantity = models.IntegerField()  # 充值数量 1￥/个
    give = models.IntegerField()  # 赠送的数量
    status = models.CharField(max_length=16)  # 未支付，已支付
    create_time = models.DateTimeField()  # 创建的时间
    pay_time = models.DateTimeField()  # 支付的时间
    left_quantity = models.IntegerField()  # 操作之后剩余的货币数量
    pay_tradeno = models.CharField(max_length=128)  # 第三方流水号
    pay_channel = models.CharField(max_length=16)  # 支付的渠道 1.支付宝 2.微信

    out_params = ['id', 'quantity', 'give', 'pay_time', 'left_quantity']

    class Meta:
        db_table = 'recharge_record'
        ordering = ['-id']


class CurrencyConsumeRecord(BaseModel):
    """货币消费记录"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    quantity = models.IntegerField()  # 充值数量 1￥/个
    create_time = models.DateTimeField(auto_now=True)  # 创建的时间
    left_quantity = models.IntegerField()  # 操作之后剩余的货币数量
    order = models.ForeignKey(CrawlOrders, on_delete=models.PROTECT)
    brief = models.CharField(max_length=128)  # 简介
    out_params = ['id', 'quantity', 'create_time', 'order_id', 'brief']

    class Meta:
        db_table = 'currency_consume_record'
        ordering = ['-id']



