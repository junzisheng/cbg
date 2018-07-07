from django.db import models
from core.models import BaseModel


class BbCrawlData(BaseModel):
    # 爬取的数据
    # 下面看情况进行扩展
    user_id = models.IntegerField()
    order_id = models.IntegerField()
    subtitle = models.CharField(max_length=32)
    collect_num = models.SmallIntegerField()
    selling_time = models.CharField(max_length=32)
    eid = models.CharField(max_length=64)
    equip_name = models.CharField(max_length=16)
    icon = models.CharField(max_length=512)
    old_price = models.IntegerField()
    price = models.IntegerField()
    status_desc = models.CharField(max_length=8)
    accept_bargain = models.BooleanField()
    desc_sumup_short = models.CharField(max_length=128)
    area_name = models.CharField(max_length=16)
    serverid = models.CharField(max_length=16)
    server_name = models.CharField(max_length=16)
    highlight = models.CharField(max_length=128)
    update_time = models.DateTimeField()
    is_display = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)

    out_params = ['id','user_id', 'order_id', 'subtitle', 'collect_num', 'selling_time', 'eid', 'equip_name',
                  'icon', 'old_price', 'price', 'status_desc', 'accept_bargain', 'desc_sumup_short', 'area_name',
                  'serverid', 'server_name', 'highlight', 'update_time']

    class Meta:
        db_table = 'bb_crawl_data'


class Proxy(models.Model):
    ip = models.CharField(max_length=16, primary_key=True)
    port = models.SmallIntegerField()
    types = models.SmallIntegerField()
    protocol = models.SmallIntegerField()
    country = models.CharField(max_length=126)
    area = models.CharField(max_length=126)
    speed = models.FloatField()
    score = models.SmallIntegerField()

    class Meta:
        db_table = 'proxys'









if __name__ == '__main__':
    BaseModel.metadata.create_all(engine)  # 创建表
    # DB_Session = sessionmaker(engine)
    # session = DB_Session()
    # s = session.query(BbCrawlData).filter(BbCrawlData.order_id == 100, CrawlData.eid == 2)
    # a = session.query(BbCrawlData).filter(BbCrawlData.order_id == 1, CrawlData.eid == 3)
    # s.update({'serverid': '123'})
    # a.update({'serverid': 'ssss'})
    # session.commit()



    # Base.metadata.drop_all(engine)  # 删除表



