# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem
from scrapy_redis.spiders import RedisSpider


class WangyiSpider(RedisSpider):
    name = 'wangyi'
    # allowed_domains = ['www.xxxx.com']
    # start_urls = ['https://news.163.com']
    redis_key = 'wangyi'

    def __init__(self):
        # 实例化一个浏览器对象(实例化一次)
        self.bro = webdriver.Chrome(executable_path='/Users/wangjifei/my_useful_file/chromedriver')

    # 必须在整个爬虫结束后，关闭浏览器
    def closed(self, spider):
        print('爬虫结束')
        self.bro.quit()

    def parse(self, response):
        lis = response.xpath('//div[@class="ns_area list"]/ul/li')
        indexs = [3, 4, 6, 7]
        li_list = []  # 存储的就是国内，国际，军事，航空四个板块对应的li标签对象
        for index in indexs:
            li_list.append(lis[index])
        # 获取四个板块中的链接和文字标题
        for li in li_list:
            url = li.xpath('./a/@href').extract_first()
            title = li.xpath('./a/text()').extract_first()

            # print(url+":"+title)

            # 对每一个板块对应的url发起请求，获取页面数据（标题，缩略图，关键字，发布时间，url）
            yield scrapy.Request(url=url, callback=self.parseSecond, meta={'title': title})

    def parseSecond(self, response):
        div_list = response.xpath('//div[@class="data_row news_article clearfix "]')
        # print(len(div_list))
        for div in div_list:
            head = div.xpath('.//div[@class="news_title"]/h3/a/text()').extract_first()
            url = div.xpath('.//div[@class="news_title"]/h3/a/@href').extract_first()
            imgUrl = div.xpath('./a/img/@src').extract_first()
            tag = div.xpath('.//div[@class="news_tag"]//text()').extract()
            tags = []
            for t in tag:
                t = t.strip(' \n \t')
                tags.append(t)
            tag = "".join(tags)

            # 获取meta传递过来的数据值title
            title = response.meta['title']

            # 实例化item对象，将解析到的数据值存储到item对象中
            item = WangyiproItem()
            item['head'] = head
            item['url'] = url
            item['imgUrl'] = imgUrl
            item['tag'] = tag
            item['title'] = title

            # 对url发起请求，获取对应页面中存储的新闻内容数据
            yield scrapy.Request(url=url, callback=self.getContent, meta={'item': item})
            # print(head+":"+url+":"+imgUrl+":"+tag)

    def getContent(self, response):
        # 获取传递过来的item
        item = response.meta['item']

        # 解析当前页面中存储的新闻数据
        content_list = response.xpath('//div[@class="post_text"]/p/text()').extract()
        content = "".join(content_list)
        item['content'] = content

        yield item
