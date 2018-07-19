# encoding:utf8
from django.db import models
from django.utils.safestring import mark_safe


class CbgBanner(models.Model):
    tag = models.CharField(max_length=16, verbose_name='标签')  # 标识banner
    href = models.CharField(max_length=512, verbose_name='链接')  # banner链接
    img_url = models.CharField(max_length=512, verbose_name='banner图片')  # banner图片链接
    brief = models.CharField(max_length=128, null=True, blank=True, verbose_name='简介')  # banner的文字简介
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    start_time = models.DateTimeField(verbose_name='展示时间')  # 启用时间
    deadline_time = models.DateTimeField(verbose_name='隐藏时间')  # 截至时间
    weight = models.SmallIntegerField(verbose_name='权重')  # 显示的权重
    is_delete = models.BooleanField(default=0, verbose_name='是否展示')  # 是否被删除

    def __str__(self):
        return self.tag + '-' + self.brief

    def render_img(self):
        return mark_safe('<img src="%s" \>' % self.img_url)
    render_img.short_description = '图片'

    class Meta:
        db_table = 'cbg_banner'
        verbose_name = 'banner管理'
        verbose_name_plural = verbose_name


class CbgService(models.Model):
    """服务"""
    name = models.CharField(max_length=64, blank=True, verbose_name='服务名')
    subtitle = models.CharField(max_length=128, blank=True, null=True, verbose_name='子标题')
    show_img = models.CharField(max_length=256, blank=True, null=True, verbose_name='图片')
    count_buy = models.IntegerField(default=0, verbose_name='销售量')  # 销量
    count_price = models.IntegerField(default=0, verbose_name='总收入')  # 总收入  分为单位
    price = models.IntegerField(null=True, blank=True, verbose_name='价格/天')  # 价格
    points = models.IntegerField(default=0, verbose_name='赠送积分')   # 赠送积分
    activity = models.ForeignKey('CbgServiceActivity', on_delete=models.DO_NOTHING, blank=True, null=True,
                                 verbose_name='开展活动')  # 产品进行的活动
    is_display = models.BooleanField(default=1)  # 隐藏或者显示服务
    def render_img(self):
        """xadmin渲染图片用"""
        return mark_safe('<img src="%s" width="80px"\>' % self.show_img)
    render_img.short_description = '图片'

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cbg_service'
        verbose_name = '服务管理'
        verbose_name_plural = verbose_name


class CbgServiceActivity(models.Model):
    """产品的活动，三种折扣力度: 1.直接减金额 2.打折 3.送优惠券 4.送积分"""
    style_choice = ((1, '满减'), (2, '满折扣'), (3, '送优惠券'), (4, '送积分'))
    style = models.SmallIntegerField(choices=style_choice, verbose_name='活动类型')
    title = models.CharField(max_length=16, verbose_name='活动标题')  # 活动标题
    subtitle = models.CharField(max_length=128, blank=True, verbose_name='活动子标题')  # 活动副标题
    fill = models.SmallIntegerField(verbose_name='条件')  # 满多少才享受优惠
    discount = models.SmallIntegerField(verbose_name='折扣', blank=True, null=True)  # 折扣力度 100以内
    reduction = models.SmallIntegerField(verbose_name='优惠', blank=True, null=True)  # 满减的金额  单位是分
    # coupon =  models.ForeignKey(CbgCoupon, on_delete=models.DO_NOTHING)  # 对应的优惠券
    points = models.SmallIntegerField(verbose_name='赠送积分', blank=True, null=True)
    banner = models.ForeignKey(CbgBanner, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='banner图片')  # 活动的banner,
    start_time = models.DateTimeField()  # 活动开始时间
    end_time = models.DateTimeField()  # 活动结束时间

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cbg_service_activity'
        verbose_name = '活动管理'
        verbose_name_plural = verbose_name


# class CbgCouponServiceRelation(models.Model):
#     """优惠券与产品的关系表"""
#     id = models.AutoField(primary_key=True)
#     coupon = models.ForeignKey(CbgCoupon, on_delete=models.CASCADE)
#     service = models.ForeignKey(CbgService, on_delete=models.CASCADE)
#     coupon_name = models.CharField(max_length=32)  # 优惠券的名字
#     service_range = models.CharField(max_length=128)  # 适用范围， 即适用服务的统称: 召唤兽服务-装备服务
#
#     class Meta:
#         db_table = 'cbg_coupon_service_rel'


