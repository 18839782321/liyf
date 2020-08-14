# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Request, HtmlResponse


class SxsCompanyListSpider(scrapy.Spider):
    name = 'sxs_company_list'
    allowed_domains = ['shixiseng.com']
    start_urls = [
        'https://www.shixiseng.com/interns?page=1&keyword=&type=company&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend=']
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'RETRY_HTTP_CODES': [302],
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
    }

    def parse(self, response: HtmlResponse):
        company_href_l = response.xpath("//*[@class='intern-wrap cursor intern-item']/@href").extract()
        for company_url in company_href_l:
            yield Request(company_url, callback=self.parse_company_detail)

    def parse_company_detail(self, response: HtmlResponse):
        item = {}
        item['short_name'] = response.xpath("//*[@class='com_name']/text()").extract_first()
        item['city'] = response.xpath("//*[@class='com_position']/text()").extract_first()
        item['cosize'] = response.xpath("//*[@class='com_num']/text()").extract_first()
        item['industry'] = response.xpath("//*[@class='com_class']/text()").extract_first()
        jd_l = response.xpath("//*[@class='content_left']//*[@class='com_detail']//text()").extract()
        if not jd_l:
            jd_l = response.xpath("//*[@class='content_left']//*[@class='com_detail']/div//text()").extract()
        item['cojd'] = '\n'.join(['企业介绍：'] + jd_l)
        item['coname'] = response.xpath(
            "//*[@class='content_right']/*[@class='com_item'][1]/*[@class='com_detail']/text()").extract_first()
        # 公司官网
        item['website'] = response.xpath("//*[@class='content_right']/*[@class='com_item'][1]/a/@href").extract_first()
        item['cotype'] = response.xpath(
            "//*[@class='content_right']/*[@class='com_item'][2]/*[@class='com_detail'][1]/text()").extract_first()
        item['cocode'] = response.xpath(
            "//*[@class='content_right']/*[@class='com_item'][2]/*[@class='com_detail'][2]/text()").extract_first()
        item['cofound'] = response.xpath(
            "//*[@class='content_right']/*[@class='com_item'][2]/*[@class='com_detail'][3]/text()").extract_first()
        item['cocapital'] = response.xpath(
            "//*[@class='content_right']/*[@class='com_item'][2]/*[@class='com_detail'][4]/text()").extract_first()
        colabel_l = response.xpath(
            "//*[@class='content_right']/*[@class='com_item'][3]/*[@class='com_detail']//text()").extract()
        item['colabel'] = '|'.join(colabel_l)
        company_url = response.url
        item['coid'] = company_url.split("/")[-1]
        # 这段代码用来抓取该公司下的所有招聘信息，并塞到redis中
        # a_list = response.xpath('//div[@class="all_job"]/a')
        # red = self.get_redis()
        # for a in a_list:
        #     href = a.xpath('@href').get()
        #     info = {
        #         'jobid': href
        #     }
        #     info = json.dumps(info)
        #     red.sadd('sxs_search_jobs:start_urls', info)
        # self.logger.info(f"公司：{item['coname']}，岗位数：{len(a_list)}")
        item['company_url'] = company_url
        item['flag'] = 'sxs_company_list'
        print(item)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'sxs_company_list'])
