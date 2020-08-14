# -*- coding: utf-8 -*-
import base64
import os
import re

import scrapy
from fontTools.ttLib import TTFont
from lxml import etree


class SxsSearchJobsSpider(scrapy.Spider):
    name = 'sxs_search_jobs'
    allowed_domains = ['shixiseng.com']
    start_urls = ['inn_oaa5eydglz7z', 'inn_bulgyhycojpc', 'inn_pfenyj08bcmw', 'inn_zatlrnw9hmpx', 'inn_4l9om3okqp6b',
                  'inn_ezfp1kviqbw0', 'inn_4lndsaqt4mhi', 'inn_cxmaalq5ggjm', 'inn_dcwk1hhkamat', 'inn_e69yvlosufbx',
                  'inn_fcnkynrtddmb', 'inn_g5euq2s321uc', 'inn_jwinkxwrbjrx', 'inn_jwinkxwrbjrx', 'inn_kxws5hnei0re',
                  'inn_m1xazpyammzf', 'inn_n97yutog5wdq', 'inn_ojqebb13cope', 'inn_p1dker7toat5', 'inn_phol4rfufz8i',
                  'inn_qistj5t6leav']

    def start_requests(self):
        for u in self.start_urls:
            url = f'https://www.shixiseng.com/intern/{u}?pcm=pc_Company'
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
                meta={'handle_httpstatus_list': [302]}
            )

    def parse(self, response):
        if response.status in (302,):
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                dont_filter=True
            )
        else:
            jobid = str(response.url).split('intern/')[1].split('?pcm')[0]
            path1 = os.path.abspath(__file__)
            path2 = os.path.dirname(path1)
            try:
                font_face = str(re.findall(re.compile(r'base64,(.*?)}', re.S), response.text)[0]).strip('")')
            except Exception:
                font_face = ''
            if font_face == '':
                self.logger.warning(f'页面找不到了：{response.url}')
            else:
                b = base64.b64decode(font_face)
                with open(f'{path2}\\{jobid}.woff', 'wb') as f:
                    f.write(b)
                    f.close()
                font = TTFont(f'{path2}\\{jobid}.woff')
                os.remove(f'{path2}\\{jobid}.woff')
                ccmap = font['cmap'].getBestCmap()
                newmap = {}
                for key, value in ccmap.items():
                    # 转换成十六进制
                    key = hex(key)
                    value = value.replace('uni', '')
                    a = 'u' + '0' * (4 - len(value)) + value
                    newmap[key] = a
                # 删除第一个没用的元素
                newmap.pop('0x78')
                # 加上前缀u变成unicode....
                for i, j in newmap.items():
                    newmap[i] = eval("u" + "\'\\" + j + "\'")

                new_dict = {}
                # 根据网页上显示的字符样式改变键值对的显示
                for key, value in newmap.items():
                    key_ = key.replace('0x', '&#x')
                    new_dict[key_] = value
                yield scrapy.Request(
                    url=response.url,
                    callback=self.parse_detail,
                    dont_filter=True,
                    meta={'new_dict': new_dict, 'jobid': jobid, 'handle_httpstatus_list': [302]}
                )

    def parse_detail(self, response):
        if response.status in (302,):
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                dont_filter=True
            )
        else:
            new_dict = response.meta.get('new_dict')
            jobid = response.meta.get('jobid')
            html = response.text
            for key, value in new_dict.items():
                html = html.replace(key, value)
            res = etree.HTML(html)
            item = {}
            # 职位名称
            item['poname'] = res.xpath('//div[@class="new_job_name"]/@title')[0]
            # 城市
            item['city'] = res.xpath('//span[@class="job_position"]/@title')[0]
            # 薪资
            item['salary'] = res.xpath('//span[@class="job_money cutom_font"]/text()')[0]
            # 学历
            item['edu'] = res.xpath('//span[@class="job_academic"]/text()')[0]
            # 工作地点
            try:
                item['address'] = res.xpath('//span[@class="com_position"]/text()')[0]
            except Exception:
                item['address'] = ''
            # 每周工作天数
            item['job_week'] = res.xpath('//span[@class="job_week cutom_font"]/text()')[0]
            # 实习时间
            try:
                item['job_time'] = res.xpath('//span[@class="job_time cutom_font"]/text()')[0]
            except Exception:
                item['job_time'] = ''
            # 职位详情地址
            item['job_url'] = response.url
            item['jobid'] = jobid
            # 职位介绍
            item['jd'] = '\n'.join(res.xpath('//div[@class="job_part"]//text()'))
            # 职位福利
            item['welfare'] = '|'.join(res.xpath('//div[@class="job_good_list"]/span//text()'))
            # 职位更新时间
            item['update_time'] = res.xpath('//div[@class="job_date "]/span[1]/text()')[0]
            # 截止时间
            item['end_time'] = re.findall(re.compile(r'截止日期：(.*?)</div>', re.S), html)[0]
            # 简历要求
            item['resume_requirement'] = re.findall(re.compile(r'简历要求：(.*?)</div>', re.S), html)[0]
            # 公司名称
            try:
                item['coname'] = str(res.xpath('//a[@class="com-name "]/text()')[0]).strip()
            except Exception:
                item['coname'] = str(
                    res.xpath('//a[@class="com-name com-name--with-label"]/text()')[0]).strip()
            try:
                href = res.xpath('//a[@class="com-name "]/@href')[0]
            except Exception:
                href = res.xpath('//a[@class="com-name com-name--with-label"]/@href')[0]
            # https://www.shixiseng.com/com/com_apjk2grlcpdj?pcm=pc_SearchList
            # 公司唯一id
            item['coid'] = str(href).split('/com/')[1].split('?')[0]
            # 企业性质
            try:
                item['conature'] = str(
                    re.findall(re.compile(r'iconqiyexingzhi.*?</i>(.*?)</div>', re.S), html)[0]).strip()
            except Exception:
                item['conature'] = ''
            item['flag'] = 'sxs_search_jobs'
            print(item)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'sxs_search_jobs'])
