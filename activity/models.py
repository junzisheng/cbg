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

