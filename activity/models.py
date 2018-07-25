import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CbgLottery1(models.Model):
    """抽奖活动1"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    lottery_times = models.SmallIntegerField(default=3)
    last_lottery_time = models.DateField()  # 最近一次的抽奖时间

    class Meta:
        db_table = 'cbg_lottery_1'


class CbgConvertCode(models.Model):
    """藏宝阁兑换码"""
    # user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    obj_type = models.SmallIntegerField(choices=((1, '优惠券'), ((2, '货币'))), verbose_name='兑换类型')   # 兑换的类型
    obj_id = models.IntegerField(verbose_name='优惠券id', blank=True)  # 兑换的对象id  这里用作优惠券的id
    obj_quantity = models.SmallIntegerField(verbose_name='货币数量', blank=True)  # 盒币的数量
    convert_code = models.CharField(max_length=126, blank=True, verbose_name='兑换码')  # 兑换码
    quantity_limit = models.SmallIntegerField(default=1, verbose_name='用户兑换上限')  # 每个用户兑换的上限
    total_limit = models.SmallIntegerField(verbose_name='开放兑换次数')  # 该兑换码总共可以被领取的次数
    receive_total = models.SmallIntegerField(default=0, verbose_name='已被兑换(次)')  # 已经被领取的次数
    start_time = models.DateTimeField(verbose_name='可兑换开始时间')
    end_time = models.DateTimeField(verbose_name='可兑换截至时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')

    class Meta:
        db_table = 'cbg_conver_code'
        verbose_name = '兑换码管理'
        verbose_name_plural = verbose_name

    @classmethod
    def create_code(cls, obj_type, quantity_limit=1, total_limit=1, create_total=1, obj_id=None, obj_quantity=None,
                    start_time=None, end_time=None):
        """生成兑换码"""
        if not (start_time or end_time):
            return False, '缺少时间！'
        if obj_type not in (1, 2):
            return False, '错误的兑换码类型！'
        if total_limit != 1 and create_total != 1:
            return False, '多人兑换码不能批量创建！'
        bulk_list = []
        for i in range(create_total):
            bulk_list.append(CbgConvertCode(
                obj_type=obj_type,
                obj_id=obj_id,
                obj_quantity=obj_quantity,
                convert_code=str(uuid.uuid1()),
                total_limit=total_limit,
                receive_total=0,
                start_time=start_time,
                end_time=end_time,
            ))
        cls.objects.bulk_create(bulk_list)
        return bulk_list


class CbgConvertCodeLog(models.Model):
    """兑换码使用记录"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    convert = models.ForeignKey(CbgConvertCode, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cbg_convert_code_log'

