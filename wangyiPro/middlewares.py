from scrapy.http import HtmlResponse
import time
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random
#UA池代码的编写（单独给UA池封装一个下载中间件的一个类）
#1，导包UserAgentMiddlware类
class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        #从列表中随机抽选出一个ua值
        ua = random.choice(user_agent_list)
        #ua值进行当前拦截到请求的ua的写入操作
        request.headers.setdefault('User-Agent',ua)

#批量对拦截到的请求进行ip更换
class Proxy(object):
    def process_request(self, request, spider):
        #对拦截到请求的url进行判断（协议头到底是http还是https）
        #request.url返回值：http://www.xxx.com
        h = request.url.split(':')[0]  #请求的协议头
        if h == 'https':
            ip = random.choice(PROXY_https)
            request.meta['proxy'] = 'https://'+ip
        else:
            ip = random.choice(PROXY_http)
            request.meta['proxy'] = 'http://' + ip

class WangyiproDownloaderMiddleware(object):
    #拦截到响应对象（下载器传递给Spider的响应对象）
    #request：响应对象对应的请求对象
    #response：拦截到的响应对象
    #spider：爬虫文件中对应的爬虫类的实例
    def process_response(self, request, response, spider):
        #响应对象中存储页面数据的篡改
        if request.url in['http://news.163.com/domestic/','http://news.163.com/world/','http://news.163.com/air/','http://war.163.com/']:
            spider.bro.get(url=request.url)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            spider.bro.execute_script(js)
            time.sleep(2)  #一定要给与浏览器一定的缓冲加载数据的时间
            #页面数据就是包含了动态加载出来的新闻数据对应的页面数据
            page_text = spider.bro.page_source
            #篡改响应对象
            return HtmlResponse(url=spider.bro.current_url,body=page_text,encoding='utf-8',request=request)
        else:
            return response

PROXY_http = [
    '153.180.102.104:80',
    '195.208.131.189:56055',
]
PROXY_https = [
    '120.83.49.90:9000',
    '95.189.112.214:35508',
]

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
