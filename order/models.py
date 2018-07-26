from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from service.models import CbgService
from coupon.models import CbgCoupon, CbgCouponUserRelation
from service.models import CbgBanner, CbgServiceActivity
from cbg_backup import settings


class CbgOrders(BaseModel):
    service_name    =   models.CharField(max_length=126, blank=True, null=True)  # 服务名称
    service         =   models.ForeignKey(CbgService, on_delete=models.DO_NOTHING)
    user            =   models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price           =   models.IntegerField(null=True, blank=True)  # 价格
    real_price      =   models.IntegerField(null=True, blank=True)  # 实付价格
    points          =   models.IntegerField(null=True, blank=True)  # 使用积分
    pay_status      =   models.CharField(max_length=32, blank=True)  # 支付状态
    pay_channel     =   models.CharField(max_length=32, blank=True)  # 支付渠道
    pay_time        =   models.DateTimeField(null=True, blank=True)  # 支付时间
    pay_tradeno     =   models.CharField(max_length=64, blank=True)  # 第三方流水号
    status          =   models.CharField(max_length=16, blank=True) # 待付款， 进行中，已完成
    service_info    =   models.CharField(max_length=126)   # 服务的信息  推送方式|服务时长|是否第一轮推送|是否降价推送|memo  #
    modify_times = models.SmallIntegerField(default=3)  # 可以更改爬取参数的次数
    last_modify_time = models.DateTimeField(null=True)  # 最近一次修改的时间
    is_delete       =   models.BooleanField(default=False)
    create_time     =   models.DateTimeField(auto_created=True, null=True)
    closing_time    =   models.DateTimeField(null=True, blank=True)  # 订单完成时间
    out_params = ['id', 'service_id', 'create_time', 'price', 'status', 'closing_time', 'service_info', 'real_price', 'pay_time', 'modify_times']
    class Meta:
        db_table = 'cbg_orders'
        ordering = ['-id']

    def resolve_service_info(self):
        _info = self.service_info.split('|', 4)  # 推送方式|服务时长|是否第一轮推送|是否降价推送|memo
        _info[2] = _info[2] == 'True'
        _info[3] = _info[3] == 'True'
        return _info

    def save(self, *args, pre_status=None,  **kwargs):
        """这里主要是根据订单状态的转变修改redis中的数据"""
        super(CbgOrders, self).save(*args, **kwargs)
        pip3 = settings.redis3.pipeline()
        if pre_status == '初始状态' and self.status == '待付款':
            pip3.hincrby('user_order_count', 'wait:%s' % self.user_id)
            pip3.execute()
        elif pre_status == '待付款' and self.status == '进行中':
            pip3.hincrby('user_order_count', 'wait:%s' % self.user_id, -1)
            pip3.hincrby('user_order_count', 'doing:%s' % self.user_id, 1)
            pip3.execute()
        elif pre_status == '进行中' and self.status == '已完成':
            pip3.hincrby('user_order_count', 'doing:%s' % self.user_id, -1)
            pip3.execute()
        elif pre_status == '待付款' and self.status == '已删除':
            pip3.hincrby('user_order_count', 'wait:%s' % self.user_id, -1)
            pip3.execute()


class CbgOrderDetail(models.Model):
    user            =   models.ForeignKey(User, on_delete=models.CASCADE)
    order           =  models.OneToOneField(CbgOrders, on_delete=models.CASCADE)
    memo            =   models.CharField(max_length=25, blank=True, default='')  # 备注
    user_ip         =   models.CharField(max_length=64, blank=True)
    user_agent      =   models.CharField(max_length=256, blank=True)
    free_push_times = models.SmallIntegerField(default=50)  # 免费短信推送次数
    crawl_url       =   models.CharField(max_length=2096, null=False)  # 爬取的url
    upload_params   =   models.TextField(max_length=10192, null=False)  # 爬取的参数
    first_round_push = models.BooleanField(default=False)
    price_down_push = models.BooleanField(default=False)
    push_type       =   models.CharField(max_length=32)  # 推送的方式  短信 邮件
    service_time    =   models.SmallIntegerField()  # 服务时间 1-30 天
    start_time      =   models.DateTimeField(null=True, blank=True)  # 开始时间
    closing_time    =   models.DateTimeField(null=True, blank=True)  # 结束时间

    class Meta:
        db_table = 'cbg_order_detail'
        ordering = ['-id']


class CbgOrderReductionLog(models.Model):
    """订单优惠的记录"""
    order = models.ForeignKey(CbgOrders, on_delete=models.DO_NOTHING, null=True, blank=True)
    style = models.SmallIntegerField(choices=((1, '优惠券'), (2, '活动优惠'),))
    alias = models.CharField(max_length=32)  # 优惠的名称
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    coupon_rel = models.ForeignKey(CbgCouponUserRelation, on_delete=models.DO_NOTHING)
    reduction = models.SmallIntegerField()  # 优惠的力度
    activity = models.ForeignKey(CbgServiceActivity, on_delete=models.DO_NOTHING, null=True, blank=True)
    deadline = models.DateTimeField()  # 订单未支付的时候有效， 用来判断该优惠是否还有效
    create_time = models.DateTimeField(auto_now_add=True)
    pay_success = models.BooleanField(default=False)

    class Meta:
        db_table = 'cbg_order_reduction_log'




class CbgRechargeRecord(BaseModel):
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
    alias       = models.CharField(max_length=32, null=True, blank=True, default="")  # 说明

    out_params = ['id', 'quantity', 'give', 'pay_time', 'left_quantity', 'alias']

    class Meta:
        db_table = 'cbg_recharge_record'
        ordering = ['-id']


class CbgCurrencyConsumeRecord(BaseModel):
    """货币消费记录"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    quantity = models.IntegerField()  # 充值数量 1￥/个
    create_time = models.DateTimeField(auto_now=True)  # 创建的时间
    left_quantity = models.IntegerField()  # 操作之后剩余的货币数量
    order = models.ForeignKey(CbgOrders, on_delete=models.PROTECT)
    brief = models.CharField(max_length=128)  # 简介
    out_params = ['id', 'quantity', 'create_time', 'order_id', 'brief']

    class Meta:
        db_table = 'cbg_currency_consume_record'
        ordering = ['-id']


