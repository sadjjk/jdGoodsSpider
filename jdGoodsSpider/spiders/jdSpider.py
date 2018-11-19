# -*- coding: utf-8 -*-


from ..settings import MAX_PAGE_NUM,START_URL
from ..items import GoodsItem
from scrapy import Request
import datetime
import scrapy
import re

class JdspiderSpider(scrapy.Spider):
    name = 'jdSpider'
    allowed_domains = ['search.jd.com']
    start_urls = START_URL

    max_page  = MAX_PAGE_NUM



    def parse(self, response):

        brand_list = [re.sub(u"[A-Za-z0-9\!\%\[\]\,\。\(\)\（\）\
\"\.\'\ ]","",brand_title) for brand_title in response.xpath('//li[contains(@id,"brand-")]/a/@title').extract()]


        goods_temp_list = response.xpath('//li[@class = "gl-item"]')


        for item  in goods_temp_list:
            goods_id = item.xpath('@data-sku').extract_first()
            goods_title = ''.join(item.xpath('.//div[contains(@class,"p-name")]/a/em/text()').extract())
            goods_url = item.xpath('.//div[@class = "p-img"]/a/@href').extract_first()
            goods_url = goods_url if "https://" in goods_url else  "http:" + goods_url
            goods_img = 'http:' + item.xpath('.//div[@class = "p-img"]/a/img/@source-data-lazy-img').extract_first()
            goods_price = item.xpath('.//div[@class = "p-price"]//i/text() ').extract_first()
            goods_shop = item.xpath('.//div[@class ="p-shop"]//a/text()').extract_first()
            goods_shop = goods_shop if goods_shop else  " "
            goods_icon = " ".join(item.xpath('.//div[@class ="p-icons"]/i/text()').extract())
            goods_brand = self.getGoodsBrand(goods_title, brand_list)

            cur_time = datetime.datetime.now()
            cur_year = str(cur_time.year)
            cur_month = str(cur_time.month) if len(str(cur_time.month)) == 2 else "0"+str(cur_time.month)
            cur_day = str(cur_time.day) if len(str(cur_time.day)) == 2 else "0" + str(cur_time.day)

            goods_time = "-".join([cur_year,cur_month,cur_day])

            goods_describe = ""
            goods = GoodsItem()

            for field in goods.fields:
                try:
                    goods[field] = eval(field)
                except NameError:
                    self.logger.debug("Field is Not Defined " + field)
            yield goods

        cur_page_num = int(response.url.split('&page=')[1])
        next_page_num = cur_page_num + 1
        if cur_page_num < self.max_page:
            next_url = response.url[:-len(str(cur_page_num))] + str(next_page_num)
            yield  Request(url=next_url,callback=self.parse)


    def getGoodsBrand(self,goods_title,brand_list):
        for brand in brand_list:
            if brand in goods_title:
                return  brand
        return  "No-brand"
