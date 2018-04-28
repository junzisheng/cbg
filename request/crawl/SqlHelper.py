#encoding=utf-8
from models import engine, BaseModel, CrawlData
from sqlalchemy.orm import sessionmaker


class SqlHelper(object):
    def __init__(self):
        self.engine = engine
        DB_Session = sessionmaker(self.engine)
        self.session = DB_Session()

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

    def batch_insert(self, Model, data_list):
        """批量插入"""
        # assert isinstance(Model, BaseModel)
        self.session.execute(
            Model.__table__.insert(),
            data_list
        )
        self.session_commit()

    def insert_once(self, Model, data):
        # assert isinstance(Model, BaseModel)
        model = Model(**data)
        self.session.add(model)

    def merge(self, Model, data):
        model = Model(**data)
        self.session.merge(model)
        self.session.commit()

    def batch_update(self, Model, m_list, k):
        for m in m_list:
            self.session.query(Model).filter(Model.order_id == m['order_id'], Model.eid == m['eid'])\
                .update({k: m[k]})
        self.session_commit()

    def session_commit(self):
        self.session.commit()








if __name__ == '__main__':
    sql = SqlHelper()
    import datetime
    import random
    l = []
    for i in range(100):
         m = {
             'server_name': '123',
             'serverid': '123',
             'area_name': '123',
             'time_left': '222',
             'price': '123',
             'nickname': '123',
             'collect_num': 123,
             'eid': '%s' % random.randint(11, 200),
             'create_time': '123123123',
             'dest_url': '123123',
             'crawl_time': datetime.datetime.now()
         }
         l.append(m)
         # c = CrawlData(**m)
    s = sql.batch_insert(CrawlData, l)
    print(s)

    # m = sql.session.commit()
    # s = sql.session.query(CrawlData.server_name, CrawlData.eid).limit(10)
    # for k, v in s:
    #     print(k, v)
