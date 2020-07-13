# -*- coding: utf-8 -*-

import json
import time

import scrapy


class ZhaopinSearchJobsSpider(scrapy.Spider):
    name = 'zhaopin_search_jobs'
    allowed_domains = ['zhaopin.com']
    start_urls = [
        'https://fe-api.zhaopin.com/c/i/jobs/searched-jobs?pageNo=1&pageSize=90&cityId=653&workExperience=0305&jobType=16000500160000&education=4&companyType=-1']

    cotype_list = ['国企: 1', '外商独资: 2', '代表处: 3', '合资: 4', '民营: 5', '股份制企业: 8', '上市公司: 9', '国家机关: 6', '事业单位: 10',
                   '银行: 11',
                   '医院: 12', '学校/下级学院: 13', '律师事务所: 14', '社会团体: 15', '港澳台公司: 16', '其它: 7']
    cosize_list = ['20人以下: 1', '20-99人: 2', '100-299人: 3', '300-499人: 8', '500-999人: 4', '1000-9999人: 5', '10000人以上: 6']
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS': 64
    }

    def parse(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            # 没有数据
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for cotype in self.cotype_list:
                yield scrapy.Request(
                    url=str(response.url).replace('companyType=-1', f'companyType={cotype.split(": ")[1]}'),
                    dont_filter=True,
                    callback=self.parse_cotype
                )

    def parse_cotype(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for cosize in self.cosize_list:
                yield scrapy.Request(
                    url=str(response.url).replace('companySize=-1', f'companySize={cosize.split(": ")[1]}'),
                    dont_filter=True,
                    callback=self.parse_cosize
                )

    def parse_cosize(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for page in range(1, 4):
                yield scrapy.Request(
                    url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                    dont_filter=True,
                    callback=self.parse_result
                )

    def parse_result(self, response):
        datas = json.loads(response.text)
        try:
            data_list = datas['data']['list']
        except Exception:
            data_list = []

        if len(data_list) > 0:
            for data in data_list:
                item = {}
                # 职位名称
                item['poname'] = data['name']
                # 公司名称
                item['coname'] = data['company']
                # 职位详情地址
                item['job_url'] = data['positionUrl']
                # 公司规模
                item['cosize'] = data['companySize']
                # 公司详情地址
                item['company_url'] = data['companyUrl']
                # 工作城市
                item['city'] = data['workCity']
                # 薪资范围
                item['providesalary'] = data['salary']
                # 工作经验
                item['worktime'] = data['workingExp']
                # 学历要求
                item['degree'] = data['education']
                # 公司性质
                item['coattr'] = data['property']
                # 职位类别
                item['rank'] = data['jobType']
                # 批次
                item['batch'] = time.strftime("%Y-%m", time.localtime())
                # 插入时间
                item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                # 来源网址
                item['origin_url'] = response.url
                # 发布日期
                item['update_time'] = ''
                # 公司行业
                item['indtype'] = ''
                # 来源网站
                item['origin'] = '智联招聘'
                item['status'] = 2
                print(item)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'zhaopin_search_jobs'])
