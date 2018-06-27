# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import logging
import json


class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def __init__(self, proxy_url, decrease_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.decrease_url = decrease_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_url=crawler.settings.get('PROXY_URL'),
            decrease_url=crawler.settings.get('DECREASE_URL')
        )

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def decrease_proxy(self, proxy):
        try:
            response = requests.get(self.decrease_url + proxy)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.info('使用代理 ' + proxy)
            request.meta['proxy'] = uri

    def process_exception(self, request, exception, spider):
        self.logger.info('代理 ' + request.meta['proxy'] + '不可用,扣1分')
        if self.decrease_proxy(request.meta['proxy'].split('//')[-1]):
            self.logger.info('扣分成功')
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.info('更换代理 ' + proxy)
            request.meta['proxy'] = uri
            return request


class CookieMiddleware(object):
    def process_request(self, request, spider):
        cookie = '_ga=GA1.2.1788820479.1530017396; _gid=GA1.2.548878708.1530017396; user_trace_token=20180626204956-6d90d0ca-793f-11e8-9759-5254005c3644; LGUID=20180626204956-6d90d401-793f-11e8-9759-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEGBB8802493B7E1F0A482368B224D77BD2; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530017396,1530103186; LGSID=20180627214030-a8b2843e-7a0f-11e8-9759-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F4%2F%3FfilterOption%3D3; X_HTTP_TOKEN=172e0c3cf55fc382a0e5482674a1fe82; LG_LOGIN_USER_ID=4f36642c75515029dda99479f322a45ac60ab85139142d2e; _putrc=1DAE39FECF83ADF2; login=true; unick=%E6%9D%8E%E4%BB%8A%E4%B8%9A; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=fde0ad565388e89f4643f5d76b27c76d350d714b8c09a091; _gat=1; TG-TRACK-CODE=index_navigation; SEARCH_ID=8cf4571171f44d00a3e22b488d7fe2d4; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530107149; LGRID=20180627214552-6863f180-7a10-11e8-b19b-525400f775ce'
        cookielist = cookie.split(';')
        cookies = {}
        for c in cookielist:
            cookies[c.split('=')[0]] = c.split('=')[1]
        request.cookies = cookies
        # logging.info('使用cookie' + json.dumps(cookies))
