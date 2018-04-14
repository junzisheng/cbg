#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # 描述表结构
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, SmallInteger, DateTime, VARCHAR
from sqlalchemy.orm import relationship

engine = create_engine('mysql+pymysql://wordpress:Xj3.14164@127.0.0.1:3306/sql_test?charset=utf8',
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=5,  # 连接池大小
                       pool_timeout=30,  # 池中没有线程最多等待时间， 否则报错
                       pool_recycle=-1,  # 多久对线程池中的线程进行一次连接回收
                       echo=False,  # 显示所有执行的sql语句
                       )
BaseModel = declarative_base()


# class Users(BaseModel):
#     # Django的内置User表 这里
#     __tablename__ = 'auth_user'
#     id = Column(Integer, primary_key=True)
#     password = Column(VARCHAR(128), nullable=False)
#     last_login = Column(DateTime)
#     is_superuser = Column(SmallInteger)
#     username = Column(VARCHAR(150), nullable=False)
#     first_name = Column(VARCHAR(30), nullable=False)
#     last_name = Column(VARCHAR(150), nullable=False)
#     email = Column(VARCHAR(254))
#     is_staff = Column(SmallInteger)
#     is_active = Column(SmallInteger)
#     date_joined = Column(DateTime)
#
#
# class UserProfile(BaseModel):
#     # 用户扩展表
#     __tablename__ = 'user_profile'
#     id = Column(Integer, primary_key=True)
#
#
#
#
# class Order(BaseModel):
#     # 订单表
#     # 用户相关
#     __tablename__ = 'order'
#     id = Column(Integer, primary_key=True)
#     umobile = Column(VARCHAR(32))
#     user_id = Column(Integer)
#     uname = Column(VARCHAR(16))
#     uemail = Column(VARCHAR(128))
#     memo = Column(VARCHAR(256))  # 备注
#     user_ip = Column(VARCHAR(64))  # 用户的ip
#     user_agent = Column(VARCHAR(256))  # 用户的UA
#     # 支付相关
#     pay_status = Column(VARCHAR(32))  # 订单状态 免费体验，记录订单是否发生；如果是订购，则记录是否支付，是否发货
#     pay_time = Column(DateTime)  # 支付时间
#     quantity = Column(Integer)  # 商品数量
#     price = Column(Integer)  # 价格 ps：这里保存的是100倍 展示的时候需要 /100
#     real_price = Column(Integer)  # 实际付款
#     points = Column(Integer)  # 产品购买积分
#     real_points = Column(Integer)  # 实际支付积分
#     discount = Column(SmallInteger)  # 这里  同样需要 /100
#     # 第三方
#     pay_channel = Column(VARCHAR(32))  # 支付渠道
#     pay_mode = Column(VARCHAR(32))  # 支付的账号 支付宝账号、微信openid或网银等
#     pay_tradeno = Column(VARCHAR(64))  # 第三方支付的流水号
#     # 父订单相关
#     # 订单时间相关
#     create_time = Column(DateTime)  # 订单创建时间
#     # 订单开启时间
#     start_time = Column(DateTime)  # 订单生效时间
#     end_time = Column(DateTime)  # 订单完成时间
#     order_status = Column(VARCHAR(16))  # 未开始  一开始 已完成
#
#     def get_order_num(self):
#         """构建流水号"""
#         pass
#
#     def recover_order_num(self):
#         """将流水号恢复为id"""
#         pass
#
#
# class CrawlTask(BaseModel):
#     __tablename__ = 'crawl_task'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))


class CrawlData(BaseModel):
    # 爬取的数据
    __tablename__ = 'crawl_data'
    # crawl_task_id = Column(Integer)  # 爬取任务的id
    # eid = Column(VARCHAR(128), nullable=False)  # 爬取的元数据对象的唯一标识
    # 下面看情况进行扩展
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer)
    server_name = Column(VARCHAR(32))
    serverid = Column(VARCHAR(32))
    area_name = Column(VARCHAR(32))
    time_left = Column(VARCHAR(32))
    price = Column(VARCHAR(16))
    nickname = Column(VARCHAR(32))
    collect_num = Column(SmallInteger)
    eid = Column(VARCHAR(64))
    create_time = Column(VARCHAR(32))
    dest_url = Column(VARCHAR(512))
    crawl_time = Column(DateTime)






if __name__ == '__main__':
    # BaseModel.metadata.create_all(engine)  # 创建表
    DB_Session = sessionmaker(engine)
    session = DB_Session()
    s = session.query(CrawlData).filter(CrawlData.order_id == 100, CrawlData.eid == 2)
    a = session.query(CrawlData).filter(CrawlData.order_id == 1, CrawlData.eid == 3)
    s.update({'serverid': '123'})
    a.update({'serverid': 'ssss'})
    session.commit()



    # Base.metadata.drop_all(engine)  # 删除表



