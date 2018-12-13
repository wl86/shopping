from django.db import models
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from shop.shop_helper import Base, MysqlHelper

goods = [
    {"name": "貂皮大衣", "price": 3000},
    {"name": "Iphone手机", "price": 1200},
    {"name": "洋河蓝之梦", "price": 1800},
    {"name": "茅台", "price": 819},
    {"name": "游艇", "price": 20000},
    {"name": "空气净化器", "price": 1750},
    {"name": "新中式竹茶桌椅组合", "price": 1388},
    {"name": "华为手机", "price": 3190},
]


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer,primary_key=True,comment='商品Id')
    name = Column(String(50),comment='商品名称')
    price = Column(Integer,default=0,comment='商品价格')
    stock =Column(Integer,defafult=1,comment='商品库存')

