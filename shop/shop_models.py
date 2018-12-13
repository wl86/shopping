from sqlalchemy import Column, Integer, String, ForeignKey

from shop.shop_helper import Base,MysqlHelper

import json


class Goods(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True, comment='商品id')  # create id column, set it auto_increment.
    name = Column(String(50), comment='商品名称')
    price = Column(Integer, default=0, comment='商品价格')
    stock = Column(Integer, default=1, comment='商品库存')

    def __str__(self):
        mdict = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
        }
        return json.dumps(mdict)


class ShopCat(Base):
    __tablename__ = 'shop_cat'
    cid = Column(Integer, primary_key=True, comment='商品订单Id')
    csid = Column(Integer,comment='商品Id')
    num = Column(Integer, comment="商品数量")
    total_price = Column(Integer, comment='商品总价')
    order = Column(String(64), comment='商品订单号')
    gsid = Column(ForeignKey('goods.id'))

    def __str__(self):
        mdict = {
            'cid': self.cid,
            'csid':self.csid,
            'num': self.num,
            'total_price': self.total_price,
            'order': self.order,
        }
        return json.dumps(mdict)


def db_synchronous():
    minst = MysqlHelper()
    session = minst.create_session()
    return (minst, session)
