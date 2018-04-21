# encoding:utf8
from django.db import models
class CrawlOrders(models.Model):
    # id              =   models.AutoField(primary_key=True)
    oid             =   models.CharField(max_length=32, blank=True)  # 订单的流水id
    uname           =   models.CharField(max_length=32, blank=True)  # 用户名
    umobile         =   models.CharField(max_length=64, blank=True)  # 用户手机号码
    uemail          =   models.CharField(max_length=12, blank=True)
    uaddress        =   models.CharField(max_length=12, blank=True)
    memo            =   models.CharField(max_length=25, blank=True)  # 备注
    price           =   models.IntegerField(null=True, blank=True)
    real_price      =   models.IntegerField(null=True, blank=True)
    points          =   models.IntegerField(null=True, blank=True)
    real_points     =   models.IntegerField(null=True, blank=True)
    pay_status      =   models.CharField(max_length=32, blank=True)
    pay_channel     =   models.CharField(max_length=32, blank=True)
    pay_time        =   models.DateTimeField(null=True, blank=True)
    pay_tradeno     =   models.CharField(max_length=64, blank=True)  # 第三方流水号
    user_ip         =   models.CharField(max_length=64, blank=True)
    user_agent      =   models.CharField(max_length=256, blank=True)
    createtime      =   models.DateTimeField(auto_created=True)
    status          =   models.CharField(max_length=16, blank=True)
    # quantity        =   models.IntegerField(null=True, blank=True)
    # supplier_id     =   models.BigIntegerField(null=True, blank=True)
    # home_page       =   models.CharField(max_length=256L, blank=True)
    # supplier_name   =   models.CharField(max_length=64L, blank=True)
    # parent_id       =   models.BigIntegerField(null=True, blank=True)
    # is_parent       =   models.IntegerField(null=True, blank=True)
    closing_time    =   models.DateTimeField(null=True, blank=True)
    # delivery_time   =   models.DateTimeField(null=True, blank=True)
    delete_falg     =   models.DateTimeField(null=True, blank=True)
    # edelivery_time  =   models.DateTimeField(null=True, blank=True)
    # callback_id     =   models.CharField(max_length=32L, blank=True)
    # user = models.ForeignKey(User)
    # is_sync         =   models.IntegerField(null=True, blank=True)
    # discount        =   models.FloatField(null=True, blank=True)
    # product         =   models.ForeignKey(Jct4Products)
    # retreat_time    =   models.DateTimeField(null=True, blank=True)
    # order_channel   =   models.CharField(max_length=20L, default='namibox', blank=True)
    # is_goods        =   models.IntegerField(null=True, blank=True, default=0)


class CrawlData(models.Model):
    order_id = models.IntegerField()
    server_name = models.CharField(max_length=32)
    server_id = models.CharField(max_length=32)
    area_name = models.CharField(max_length=32)
    time_left = models.CharField(max_length=32)
    price = models.CharField(max_length=16)
    nickname = models.CharField(max_length=32)
    collect_num = models.SmallIntegerField()
    eid = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    dest_url = models.CharField(max_length=512)
    crawl_time = models.DateTimeField(max_length=512)

    class Meta:
        db_table    = 'crawl_data'
