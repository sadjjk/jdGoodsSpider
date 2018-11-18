# -*- coding: utf-8 -*-


from .items import GoodsItem
import  pymongo
import  logging

class MongoPipeline(object):


    def open_spider(self, spider):

        self.client = pymongo.MongoClient('127.0.0.1')
        self.db = self.client["JD"]



    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):

        if isinstance(item,GoodsItem):
            try:
                collection_name = self.getCollection(item['goods_brand'])
                old_item = self.db[collection_name].find_one({"goods_id":item['goods_id']})
                if old_item is None:
                    logging.info("items: " + item['goods_id'] + " insert_in " + collection_name +" db.")
                    self.db[collection_name].insert(dict(item))

                elif self.needToUpdate(old_item,item):
                    self.db[collection_name].remove({'good_id':item['goods_id']})
                    self.db[collection_name].insert(dict(item))

                    logging.info("items: " + item['goods_id'] + " has  UPDATED in " + collection_name + " db.")

                else:
                    logging.info("item: " + item['goods_id'] + " has STORED in " + collection_name + " db.")

            except Exception as e :
                logging.error("PIPLINE EXCEPTION:" +str(e))

        return  item

    def getCollection(self,brand):
        if brand == u'乐事':
            return "Leshi"
        elif brand == u'旺旺':
            return "Wangwang"
        elif brand == u'三只松⿏':
            return "Sanzhisongshu"
        elif brand == u'卫⻰':
            return "Weilong"
        elif brand == u'口水娃':
            return "Koushuiwa"
        elif brand == u'奥利奥':
            return "Aoliao"
        elif brand == u'良品铺子':
            return "Liangpinpuzi"
        else:
            return "Other"


    def needToUpdate(self,old_item,new_item):
        if old_item['goods_price'] != new_item['goods_price']:
            old_time = old_item['goods_time']
            old_price = float(old_item['goods_prcie'])
            new_price = float(old_item['goods_price'])

            minus_price = abs(round((new_price - old_price) , 2 ))
            logging.info("needToUpdate")

            if minus_price >= 0:
                new_item['goods_describe']  = "比" + old_time + "涨了" + str(minus_price) + "元."
            else:
                new_item['goods_describe']  = "比" + old_time + "降了" + str(minus_price) + "元."

            return  True

        return  False




