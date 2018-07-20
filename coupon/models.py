from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from service.models import CbgService



# Create your models here.
class CbgCoupon(models.Model):
    id              = models.AutoField(primary_key=True)
    style_choice    = ((1, '满减'), (2, '满折扣'))
    style           = models.SmallIntegerField(choices=style_choice, verbose_name='类型')
    coupon_name     = models.CharField(max_length=256, verbose_name='优惠券名')              # 优惠券名
    service_range   = models.CharField(max_length=128, verbose_name='使用范围', null=True, blank=True)
    # service         = models.ManyToManyField(CbgService, through=CbgCouponServiceRelation, through_fields=['coupon_id', 'service_id'],
    #                                          related_name='cbg_service')
    service         = models.ManyToManyField(CbgService)
    fill            = models.SmallIntegerField(verbose_name='条件')  # 满多少才享受优惠
    discount        = models.SmallIntegerField(verbose_name='折扣', null=True, blank=True)  # 折扣力度 100以内
    reduction       = models.SmallIntegerField(verbose_name='满减', null=True, blank=True)  # 满减
    total_limit     = models.IntegerField(verbose_name='发放数量', default=0)                         # 发放数量上限
    assign_limit    = models.SmallIntegerField(default=1, verbose_name='单用户领取上限')         # 每个用户可以领取的上限 -1表示可以无限领取
    acquire_count   = models.IntegerField(default=0, verbose_name='已领取')                # 领取数 （每次领取后数值 +1）
    usage_count     = models.IntegerField(default=0, verbose_name='已使用')                # 使用数 （每次使用后数值 +1）
    acquire_start_time = models.DateField(verbose_name='发放时间')                     # 可领取开始时间
    acquire_end_time = models.DateField(verbose_name='截至时间')                       # 可领取结束时间
    create_time     = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')       # 创建时间
    received        = models.BooleanField(default=True, verbose_name='可领取')             # 是否可以通过接口获取

    def __str__(self):
        return self.coupon_name

    def get_reduction(self, price):
        """获取订单的优惠"""
        if price < self.fill:
            raise ValueError
        return self.reduction if self.style == 1 else price * (1- (self.discount/100) )

    class Meta:
        db_table = 'cbg_coupon'
        verbose_name = '优惠券管理'
        verbose_name_plural = verbose_name


class CbgCouponUserRelation(BaseModel):
    id              = models.AutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    status          = models.SmallIntegerField()                            # 状态 0 未使用， 1正在使用 2.已使用
    coupon          = models.ForeignKey(CbgCoupon, on_delete=models.CASCADE)# 对应 CbgCoupon 中的 id
    service_ids     = models.CharField(max_length=32, null=True, blank=True)
    acquire_time    = models.DateField()                                # 领取时间
    expire_time     = models.DateField()                                # 优惠券的过期时间
    usage_time      = models.DateTimeField()                                # 使用时间 (未使用时为 null)
    order_id        = models.IntegerField()                                 # 使用 coupon 时对应的 order_id, 即为 cbg_orders 中的 id
    out_params = ['id', 'user_id', 'coupon_id', 'expire_time', 'usage_time', 'order_id', 'status']

    class Meta:
        db_table = 'cbg_coupon_user_relation'


# class CbgCouponService(models.Model):
#     cbgcoupon = models.ForeignKey(CbgCoupon, on_delete=models.DO_NOTHING)
#     cbgservice = models.ForeignKey(CbgService, on_delete=models.DO_NOTHING)
#
#     class Meta:
#         db_table = 'cbg_coupon_service'


# class CbgCouponServiceRelation(models.Model):
#     """优惠券与产品的关系表"""
#     id = models.AutoField(primary_key=True)
#     coupon = models.ForeignKey('CbgCoupon', on_delete=models.CASCADE)
#     service = models.ForeignKey(CbgService, on_delete=models.CASCADE)
#     coupon_name = models.CharField(max_length=32)  # 优惠券的名字
#     service_range = models.CharField(max_length=128)  # 适用范围， 即适用服务的统称: 召唤兽服务-装备服务
#
#     class Meta:
#         db_table = 'cbg_coupon_service'


