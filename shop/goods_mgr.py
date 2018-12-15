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
        self.synchronous()
        self.__money = 15000

    def get_money(self):
        return self.__money

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
        在数据库中不显示重复的商品信息,只在数量上增加
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
                            shopcat.num += 1
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
        '''
        显示购物车内容
        :return:
        '''
        shopcat_list = self.__minst.query_records(self.__session, ShopCat)
        for shopcat in shopcat_list:
            print(shopcat)

    def delete_cat(self, nums):
        '''
        删除或清空购物车
        :return:
        '''

        try:
            if len(nums) != 1:

                for i in nums:
                        self.__session.query(ShopCat).filter_by(cid=i).delete()
                        self.__session.commit()
                print('购物车以清空')

            else:
                self.__session.query(ShopCat).filter_by(cid=nums).delete()
                self.__session.commit()
                print('购物车以清空')

        except Exception as e:
            print(e)

    def good_by(self):
        '''
        购买商品
        :return:
        '''
        shops = self.__session.query(ShopCat).all()
        money = 0
        for shop in shops:
            money += shop.total_price
        if money > self.__money:
            print('您的余额不足,请充值,结算失败')
        else:
            self.__money -= money
            print('结算成功,余额为:', self.get_money())


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


def init_db(good_mgr):
    '''
    初始化数据
    :return:
    '''
    good_list = __logging_data()
    good_mgr.add_good_record(good_list)


# good_mgr = GoodMgr()


# good_list = __logging_data()
# good_mgr.add_goods(good_list)
# good_mgr.show_goods()
# good_mgr.add_shopcat([1,2])
# good_mgr.show_shopcat()
# good_mgr.good_by()


def add_good(good_mgr):
    print("1--> 添加商品数据\n")
    name = input("请输入商品名称:")
    price = int(input("请输入商品价格:"))
    stock = int(input("请输入库存"))
    goods = Goods(name=name, price=price, stock=stock)
    good_mgr.add_goods(goods)
    print("\n添加数据成功!\n")
    good_mgr.show_goods()


def show_goods(good_mgr):
    print("2--> 显示商品列表\n")
    good_mgr.show_goods()


def add_shop_car(good_mgr):
    print("3---> 添加购物车\n")
    good_ids = input("请输入一个或者多个商品id (以逗号,分割):")
    good_ids_list = good_ids.split(",")
    good_ids = [good_id.strip() for good_id in good_ids_list]
    good_mgr.add_shopcat(good_ids)
    good_mgr.show_shopcat()


def clear_shop_car(good_mgr):
    print("4--> 清空购物车\n")
    good_mgr.show_shopcat()
    num = input("请输入ID")
    num_list = num.split(',')
    nums = [num1 for num1 in num_list]
    good_mgr.delete_cat(nums)



def show_shop_car(good_mgr):
    print("5--> 查看购物车内容\n")
    good_mgr.show_shopcat()


def buy_goods(good_mgr):
    print("6--> 购买商品\n")
    good_mgr.good_buy()


DISPATCH_MAP = {
    '1': add_good,
    '2': show_goods,
    '3': add_shop_car,
    '4': clear_shop_car,
    '5': show_shop_car,
    '6': buy_goods,

}


def process():
    good_mgr = GoodMgr()
    print("0--->退出\n1--> 添加商品数据\n2--> 显示商品列表\n"
          "3---> 添加购物车\n4--> 清空购物车\n"
          "5--> 查看购物车内容\n6--> 购买商品\n7--> 订单详情列表\n8--> 获取当前余额\n")
    while True:
        input_str = input("请输入数字：").strip()
        if input_str == '0':
            print("0-->退出")
            break
        function = DISPATCH_MAP.get(input_str, None)
        if function == None:
            print("0--->退出\n1--> 添加商品数据\n2--> 显示商品列表\n"
                  "3---> 添加购物车\n4--> 清空购物车\n"
                  "5--> 查看购物车内容\n6--> 购买商品\n7--> 订单详情列表\n8--> 获取当前余额\n")
            continue
        function(good_mgr)


if __name__ == "__main__":
    process()
    li = 's,sa,a'
    print(len(li))
    print(li.split(','))
