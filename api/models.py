from django.db import models
# class Proxys(models.Model):
#     ip = models.CharField(max_length=11, blank=True)
#     port = models.SmallIntegerField()
#     types = models.SmallIntegerField()
#     protocol = models.SmallIntegerField()
#     country = models.CharField(max_length=32)
#     area = models.CharField(max_length=32)
#     updatetime = models.DateTimeField(auto_now_add=True)
#     speed = models.DecimalField(max_digits=5, decimal_places=2)
#     score = models.SmallIntegerField()
#
#     class Meta:
#         db_table = 'proxys'
#
# class CrawlData(BaseModel):
#     # ��ȡ������
#     __tablename__ = 'crawl_data'
#     # crawl_task_id = Column(Integer)  # ��ȡ�����id
#     # eid = Column(VARCHAR(128), nullable=False)  # ��ȡ��Ԫ���ݶ����Ψһ��ʶ
#     # ���濴���������չ
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     order_id = Column(Integer)
#     server_name = Column(VARCHAR(32))
#     serverid = Column(VARCHAR(32))
#     area_name = Column(VARCHAR(32))
#     time_left = Column(VARCHAR(32))
#     price = Column(VARCHAR(16))
#     nickname = Column(VARCHAR(32))
#     collect_num = Column(SmallInteger)
#     eid = Column(VARCHAR(64))
#     create_time = Column(VARCHAR(32))
#     dest_url = Column(VARCHAR(512))
#     crawl_time = Column(DateTime)
