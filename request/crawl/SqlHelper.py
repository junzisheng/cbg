#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config
from models import engine, BaseModel, CrawlData


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

    def insert_once(self, Model, data):
        # assert isinstance(Model, BaseModel)
        model = Model(**data)
        self.session.add(model)

    def merge(self, Model, data):
        model = Model(**data)
        self.session.merge(model)
        self.session.commit()

    def session_commit(self):
        self.session.commit()







if __name__ == '__main__':
    sql = SqlHelper()
    sql.drop_db()
