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
    service_id = models.IntegerField()
    subtitle = models.CharField(max_length=32)  # 等级
    collect_num = models.SmallIntegerField()  # 收藏数
    selling_time = models.DateTimeField()  # 出售的时间
    eid = models.CharField(max_length=64)
    equip_name = models.CharField(max_length=16)  # 名称(人物是id 召唤兽和装备就是名称)
    icon = models.CharField(max_length=512)  # 创建图片链接的参数
    game_ordersn = models.CharField(max_length=128)  # 组成详情页的url  http://xyq-m.cbg.163.com/cgi/mweb/product/detail/{serverid}/{game_ordersn}??view_loc=link_weixin&equip_refer=326
    old_price = models.IntegerField()
    price = models.IntegerField()
    status_desc = models.CharField(max_length=8)  # 上架 公示期
    accept_bargain = models.BooleanField()  # 是否接收还价
    desc_sumup_short = models.CharField(max_length=128)  # 简单的介绍
    area_name = models.CharField(max_length=16)
    serverid = models.CharField(max_length=16)
    server_name = models.CharField(max_length=16)
    highlight = models.CharField(max_length=128)  # 亮点
    update_time = models.DateTimeField()
    is_display = models.BooleanField(default=1)  # 是否显示
    is_delete = models.BooleanField(default=0)  # 是否被删除

    out_params = ['id','user_id', 'order_id', 'subtitle', 'collect_num', 'selling_time', 'eid', 'equip_name',
                  'icon', 'old_price', 'price', 'status_desc', 'accept_bargain', 'desc_sumup_short', 'area_name',
                  'serverid', 'server_name', 'highlight', 'update_time', 'game_ordersn', 'service_id']

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
        app_label = 'proxy'


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



