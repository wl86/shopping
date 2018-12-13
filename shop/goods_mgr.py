'''
1. 设计表结构，将上述商品列表信息，同步到db数据库中，查询价格大于2000的商品

2. 购买功能。 假设用户初始总金额为15000，购买了新的产品后，金额做减法，要求用户输入购买金额，如果低于商品列表中的最低价，则要求用户重新输入

3. 购物车功能。

   假设用户初始总金额为15000

       （1） 显示商品列表，让用户根据序号选择商品，加入购物车

       （2）查看购物车，购物车内如果有相同的产品不要重复显示  [(商品id, 2), ]

       （3）可以让用户删除购物车内的产品，或清空购物车

       （4）结算时如果余额不足，则提示账户余额不足

建议将上述功能点都封装到类中。
'''
import random

import time
from shop.shop_models import *

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


class GoodMgr:
    def __init__(self):

        self.__money = 15000

    def synchronous(self):
        '''
        同步到Db
        :return:
        '''
        (self.__minst, self.__session) = db_synchronous()

    def add_goods(self, goods):
        '''
        录入商品
        __mist: 调用类方法,将对象添加到db
        :param goods:
        :return:
        '''
        self.__minst.add_records(self.__session, goods)

    def show_goods(self):
        '''
        显示商品
        :return:
        '''
        goods_list = self.__minst.query_records(self.__session, Goods)
        for goods in goods_list:
            print(goods)

    def add_shopcat(self, goodsid):
        '''
        将商品添加到购物车
        :param goodsid:可能是单个或多个商品,所以要判断
        :return:
        '''
        cat_list = []
        strtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        orders = strtime + str(random.randint(100, 999))

        if isinstance(goodsid, list):
            for i in goodsid:
                good = self.__session.query(Goods).filter_by(id=i).first()
                shopcat = self.__session.query(ShopCat).filter_by(csid=i).first()
                try:
                    if shopcat.csid:
                        if i != shopcat.csid:
                            goods = ShopCat(csid=i, num=1, total_price=good.price, order=orders)
                            cat_list.append(goods)
                            self.__minst.add_records(self.__session, cat_list)
                        else:
                            shopcat.num +=1
                            shopcat.total_price = shopcat.num * good.price
                            self.__session.commit()
                except:
                    goods = ShopCat(csid=i, num=1, total_price=good.price, order=orders)
                    cat_list.append(goods)
                    self.__minst.add_records(self.__session, cat_list)
        else:
            good = self.__session.query(Goods).filter_by(id=goodsid).first()
            shopcat = self.__session.query(ShopCat).filter_by(csid=goodsid).first()
            try:
                if shopcat.csid:
                    if goodsid != shopcat.csid:
                        goods = ShopCat(csid=goodsid, num=1, total_price=good.price, order=orders)
                        cat_list.append(goods)
                        self.__minst.add_records(self.__session, cat_list)
                    else:
                        goods = ShopCat(csid=goodsid, num=shopcat.num + 1, total_price=good.price, order=orders)
                        cat_list.append(goods)
                        self.__minst.add_records(self.__session, cat_list)
            except:
                goods = ShopCat(csid=goodsid, num=1, total_price=good.price, order=orders)
                cat_list.append(goods)
                self.__minst.add_records(self.__session, cat_list)

    def show_shopcat(self):
        shopcat_list = self.__minst.query_records(self.__session, ShopCat)
        for shopcat in shopcat_list:
            print(shopcat)


def __logging_data():
    '''
    录入数据
    :return:
    '''
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

    good_list = []
    for good in goods:
        gmodel = Goods(name=good['name'], price=good['price'],
                       stock=random.randint(1, 100))
        good_list.append(gmodel)

    return good_list


def __add_cat(csid, num, total_price, order):
    cat_list = []
    goods = ShopCat(csid=csid, num=num, total_price=total_price, order=order)
    cat_list.append(goods)
    return cat_list


def init_db(good_mgr):
    '''
    初始化数据
    :return:
    '''
    good_list = __logging_data()
    good_mgr.add_good_record(good_list)


good_mgr = GoodMgr()
good_mgr.synchronous()
good_list = __logging_data()
good_mgr.add_goods(good_list)
good_mgr.show_goods()
good_mgr.add_shopcat([1,2])
