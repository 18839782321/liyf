# -*- coding: utf-8 -*-
import json
import time

import scrapy


class ZoroSpider(scrapy.Spider):
    name = 'zoro'
    allowed_domains = ['zoro.com']
    start_urls = ['https://www.zoro.com/measuring-layout-tools/c/4415/']
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        json_data = response.xpath('//div[@id="search-raw-response"]/@data-search-response').get()
        datas = json.loads(json_data)
        for record in datas['records']:
            zoro_sku = record['allMeta']['id']
            brand = record['allMeta']['brand']
            image = record['allMeta']['variants'][0]['image']
            mfr = record['allMeta']['variants'][0]['mfr_no']
            detail_url = f'https://www.zoro.com/product/?products={zoro_sku}'
            try:
                slug = record['allMeta']['variants'][0]['slug']
                des_url = f'https://www.zoro.com/{slug}/i/{zoro_sku}/'
                in_stock = record['allMeta']['variants'][0]['salesStatus']
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail,
                    dont_filter=True,
                    meta={
                        "zoro_sku": zoro_sku,
                        "brand": brand,
                        "mfr": mfr,
                        "des_url": des_url,
                        "in_stock": in_stock,
                        "image": image,
                        'status': '1',
                        'a_url': response.url
                    },
                )
            except:
                des_url = f'https://www.zoro.com/i/{zoro_sku}/'
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail,
                    dont_filter=True,
                    meta={
                        "zoro_sku": zoro_sku,
                        "brand": brand,
                        "mfr": mfr,
                        "des_url": des_url,
                        "image": image,
                        "status": '0',
                        'a_url': response.url
                    },
                )

        # 下一页逻辑
        next_page_href = response.xpath('//div[@class="category-pagination"]/ul[last()]/li[last()]/a/@href').get()
        if next_page_href == '#':
            print(f'没有下一页了，最后一页网址为：{response.url}')
            pass
        else:
            print(f'有下一页，网址为：{next_page_href}')
            yield scrapy.Request(
                dont_filter=True,
                url=next_page_href,
                callback=self.parse,
                # meta={'handle_httpstatus_list': [301, 302]}
            )

    def parse_detail(self, response):
        minOrderQuantity = json.loads(response.text)['products'][0]['validation']['minOrderQuantity']
        if minOrderQuantity:
            price = json.loads(response.text)['products'][0]['price']
            try:
                img_url = f'https://www.zoro.com/static/cms/product/full/{response.meta.get("image")}'
            except:
                img_url = ''

            if response.meta.get('status') == '1':
                des_url = response.meta.get('des_url')
                in_stock = response.meta.get('in_stock')
            else:
                des_url = response.meta.get('des_url')
                in_stock = json.loads(response.text)['products'][0]['salesStatus']

            yield scrapy.Request(
                url=des_url,
                callback=self.parse_description,
                dont_filter=True,
                meta={
                    "in_stock": in_stock,
                    "brand": response.meta.get('brand'),
                    "minOrderQuantity": minOrderQuantity,
                    "zoro_sku": response.meta.get('zoro_sku'),
                    "mfr": response.meta.get('mfr'),
                    "price": price,
                    "img_url": img_url,
                    # 'handle_httpstatus_list': [301, 302]
                }
            )

    def parse_description(self, response):
        description = str(response.xpath('//div[@class="product-description__text"]/text()').get()).strip()
        if description == 'None':
            description = str(response.xpath('//div[@class="product-description__text"]/ul/li//text()').get()).strip()
        title = str(response.xpath(
            '//div[@class="zcl-heading product-title__name bu-title zcl-heading--2 bu-is-2 bu-is-size-3-mobile"]/text()').get()).strip()

        li_list = response.xpath('//ul[@class="product-overview__attributes"]/li')
        featue = {}
        for li in li_list:
            key = str(li.xpath('strong/text()').get()).replace(':', '')
            val = str(li.xpath('text()').get()).strip()
            featue[key] = val
        featues = str(featue).replace("'", '').replace('{', '').replace('}', '')
        zoro_sku = response.meta.get('zoro_sku')
        payload = {f"{zoro_sku}": f"{zoro_sku}"}
        yield scrapy.Request(
            url='https://www.zoro.com/avl/',
            method='POST',
            body=json.dumps(payload),
            callback=self.parse_dcs,
            dont_filter=True,
            meta={
                "in_stock": response.meta.get('in_stock'),
                "brand": response.meta.get('brand'),
                "minOrderQuantity": response.meta.get('minOrderQuantity'),
                "title": title,
                "zoro_sku": zoro_sku,
                "price": response.meta.get('price'),
                "img_url": response.meta.get('img_url'),
                "description": description,
                "mfr": response.meta.get('mfr'),
                "featues": featues,
            }
        )

    def parse_dcs(self, response):
        zoro_sku = response.meta.get('zoro_sku')
        dcs = json.loads(response.text)[zoro_sku][-1]
        if '.' in str(dcs):
            dcs = dcs.split('.')[0]
        else:
            dcs = dcs

        web_id = 1

        if int(dcs) < 1:
            pass
        else:
            item = {}
            item['batch'] = time.strftime("%Y-%m-%d", time.localtime())
            item['in_stock'] = response.meta.get('in_stock')
            item['dcs'] = dcs
            item['web_id'] = web_id
            item['brand'] = response.meta.get('brand')
            item['minOrderQuantity'] = response.meta.get('minOrderQuantity')
            item['title'] = response.meta.get('title')
            item['zoro_sku'] = response.meta.get('zoro_sku')
            item['price'] = response.meta.get('price')
            item['img_url'] = response.meta.get('img_url')
            item['description'] = response.meta.get('description')
            item['mfr'] = response.meta.get('mfr')
            item['featues'] = response.meta.get('featues')
            print(item)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'zoro'])
