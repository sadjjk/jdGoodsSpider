# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()  # 零食的ID
    goods_title = scrapy.Field()  # 零食的名字
    goods_url = scrapy.Field()  # 零食的详情⻚页URL
    goods_img = scrapy.Field()  # 零食的图⽚片
    goods_price = scrapy.Field()  # 零食的价格
    goods_shop = scrapy.Field()  # 零食的店铺
    goods_icon = scrapy.Field()  # 零食的优惠活动
    goods_time = scrapy.Field()  # 零食的扫描时间
    goods_brand = scrapy.Field()  # 零食的品牌
    goods_describe = scrapy.Field()  # 零食的描述
