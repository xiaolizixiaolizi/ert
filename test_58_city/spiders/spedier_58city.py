# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request  # 导入Request包
from ..utils.parse import parse, xiaoqu_parse, get_ershou_price_list, chuzu_list_pag_get_detail_url,get_chuzu_house_info
from traceback import format_exc
from ..items import City58XiaoQu,City58ItemZhuCu

class Spedier58citySpider(scrapy.Spider):
    name = 'spedier_58city'
    allowed_domains = ['58.com']
    host = 'cd.58.com'
    xiaoqu_url_format = 'http://{}/xiaoqu{}/'
    xiaoqu_code = list()
    xiaoqu_code.append(115)

    def start_requests(self):  # 重写start_requests函数
        start_urls = [self.xiaoqu_url_format.format(self.host, code) for code in self.xiaoqu_code]
        self.logger.debug(start_urls)
        for url in start_urls:
            yield Request(
                url,
                callback=self.parse
            )  # 遍历所有区域比如http://cd.58.com/xiaoqu/115/并且作为request发送到 def parse(self, response):

    def parse(self, response):
        url_list = parse(response)  # 调用parse函数
        for url in url_list:
            yield Request(
                url,
                callback=self.xiaoqu_detail_page,
                errback=self.error_back
            )

    def xiaoqu_detail_page(self, response):
        data = xiaoqu_parse(response)
        item = City58XiaoQu()
        item.update(data)
        item['id'] = response.url.spilt('/')[4]
        yield item

        # 二手房
        url = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.ershoufang_list_pag,
                      errback=self.error_back,
                      meta={'id': item['id']}
                      )
        # 出租房
        url_ = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host, item['id'])

        yield Request(url_,
                      callback=self.chuzu_list_pag,  # 回调chuzu_list_pag方法
                      errback=self.error_back,
                      meta={'id': item['id']}
                      )

    def ershoufang_list_pag(self, response):
        _=self #没有实际意思
        price_list = get_ershou_price_list(response)
        yield {
            'id': response.meta['id'],
            'price_list': price_list
        }
        # 翻页

    def chuzu_list_pag(self, response):
        url_list = chuzu_list_pag_get_detail_url(response)
        for url in url_list:
            yield response.Request.repalce(url=url, callback=self.chu_zu_detail)
        #翻页

    def chu_zu_detail(self,response):
        data=get_chuzu_house_info(response)
        item=City58ItemZhuCu()
        item.update(data)
        item['id']=response.meta['id']
        item['url']=response.url
        yield  item

    def error_back(self, e):
        _ = e,
        self.logger.error(format_exc())
