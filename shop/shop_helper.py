
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

mysql_str = 'mysql+pymysql://root:123456@127.0.0.1:3306/shopping'
engine = create_engine(mysql_str)

Base = declarative_base()


class MysqlHelper:

    def db_table(self):
        Base.metadata.create_all(engine)

    def create_session(self):
        self.db_table()
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def add_records(self, session, objs):
        if isinstance(objs, list):
            session.add_all(objs)
        else:
            session.add(objs)
        session.commit()

    def query_records(self, session, Cls):
        '''
        查询数据
        :param session:
        :param Cls: 查询的类(表)
        :return:
        '''
        return session.query(Cls).all()

    def query_conditions(self, session, Cls, field, value):
        '''
        查询满足条件的数据
        :param session:
        :param Cls: 查询的表
        :param field: Cls.field 查询的键 举个栗子: 查询姓名 Cls.name
        :param value: 查询的值  举个栗子: 姓名 : 'hh'
        :return:
        '''
        return session.query(Cls).filter(field == value)



    def update_record(self, session, Cls, field, value, dic):
        '''
        更新数据
        :param session:
        :param Cls: 更新的表
        :param field: 需要更新的字段
        :param value: 字段的值
        :param dic: 更新后的字段和值组成的字典  {key:value}
        :return:
        '''
        return session.query(Cls).filter(field == value).update(dic)

    def delete_records(self, Cls, session, field, *args):
        '''
        删除多条或单条数据
        :param Cls:
        :param session:
        :param field:
        :param args: 单条或多条数据
        :return:
        '''
        try:
            for i in args:
                obj = session.query(Cls).filter(field == i).delete()
                if len(args) == 1:
                    if obj:
                        session.commit()
                        return True
                    else:
                        return False
                # 保存同步到数据库
                session.commit()
            return True
        except Exception as e:
            print(e)

