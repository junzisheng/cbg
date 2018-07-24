from django.db import models
from core.models import BaseModel


# class CbgCrawlData(BaseModel):
#     # 爬取的数据
#     # 下面看情况进行扩展
#     user_id = models.IntegerField()
#     order_id = models.IntegerField()
#     subtitle = models.CharField(max_length=32)  # 等级
#     collect_num = models.SmallIntegerField()
#     selling_time = models.CharField(max_length=32)
#     eid = models.CharField(max_length=64)
#     equip_name = models.CharField(max_length=16)
#     icon = models.CharField(max_length=512)
#     old_price = models.IntegerField()
#     price = models.IntegerField()
#     status_desc = models.CharField(max_length=8)  # 上架 公示期
#     accept_bargain = models.BooleanField()   # 接收还价
#     desc_sumup_short = models.CharField(max_length=128)  #简介 比如成长 几技能
#     area_name = models.CharField(max_length=16)
#     serverid = models.CharField(max_length=16)
#     server_name = models.CharField(max_length=16)
#     highlight = models.CharField(max_length=128)  # 亮点
#     update_time = models.DateTimeField()
#     is_display = models.BooleanField(default=1)
#     is_delete = models.BooleanField(default=0)
#
#     out_params = ['id','user_id', 'order_id', 'subtitle', 'collect_num', 'selling_time', 'eid', 'equip_name',
#                   'icon', 'old_price', 'price', 'status_desc', 'accept_bargain', 'desc_sumup_short', 'area_name',
#                   'serverid', 'server_name', 'highlight', 'update_time']
#
#     class Meta:
#         db_table = 'bb_crawl_data'
"""
图片：
装备: https://cbg-xyq.res.netease.com/images/small/2062.gif  equip_face_img  equip_type(https://cbg-xyq.res.netease.com/images/small/2556.gif)
人物: https://cbg-xyq.res.netease.com/images/app/bigface/%s.png 角色类型的id icon  
召唤兽 https://cbg-xyq.res.netease.com/images/small/102231.gif:  equip_face_img  equip_type

"""



class CbgCrawlData(BaseModel):
    """爬取藏宝阁的信息"""
    user_id = models.IntegerField()
    order_id = models.IntegerField()
    subtitle = models.CharField(max_length=32)
    collect_num = models.SmallIntegerField()
    selling_time = models.DateTimeField()
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
        db_table = 'cbg_crawl_data'


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
    # s = session.query(CbgCrawlData).filter(CbgCrawlData.order_id == 100, CrawlData.eid == 2)
    # a = session.query(CbgCrawlData).filter(CbgCrawlData.order_id == 1, CrawlData.eid == 3)
    # s.update({'serverid': '123'})
    # a.update({'serverid': 'ssss'})
    # session.commit()



    # Base.metadata.drop_all(engine)  # 删除表



