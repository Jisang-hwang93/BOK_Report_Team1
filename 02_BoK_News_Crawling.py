from naver_news.items import NaverNewsItem
from datetime import datetime

import scrapy, re
import pandas as pd

class CrawlNewsSpider(scrapy.Spider):
    name = 'crawl_news'
    allowed_domains = ['naver.com']
    url_format = "https://search.naver.com/search.naver?&where=news&query={}&sm=tab_pge&sort=2&photo=0&field=0&reporter_article=&pd=2&ds={}&de={}&docid=&nso=so:da,p:1m,a:all&mynews=0&start=1&refresh_start=0"
    
    def __init__(
        self, keyword="", start="", end="", **kwargs
    ):
        # 날짜를 0000-00-00으로 입력했을 때 날짜 데이터로 변환해줌
        startdate = datetime.strptime(start, "%Y-%m-%d")
        enddate = datetime.strptime(end, "%Y-%m-%d")
        # 날짜 형식으로 넘겨줌
        self.start_urls = []
        for cur_date in pd.date_range(startdate, enddate):
            self.start_urls.append(self.url_format.format(keyword, cur_date.strftime("%Y-%m-%d"), cur_date.strftime("%Y-%m-%d")))

    def parse(self, response):
        # 페이지 넘버를 가져오는 코드
        # curpage = int(re.search(r"(&start=[0-9]*)", response.url).group().split("=")[1]) # r을 사용하면 \를 사용하지 않아도 됨
        
        for item in response.css("ul.type01 li"):
            if item.css("a._sp_each_url"): # 네이버 뉴스 링크가 존재하면 url을 가져옴
                url = item.css("a._sp_each_url::attr(href)").get()
                yield scrapy.Request(url, callback=self.parse_detail)

        # a.next가 존재하면 페이지를 넘김
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_detail(self, response):
        item = NaverNewsItem()
        # items.py에 있는 item을 가져오기
        item['url'] = response.url
        item['title'] = response.css("h3#articleTitle::text").get()
        item['media'] = response.css("div.press_logo img::attr(title)").get()
        item['upload_date'] = response.css("span.t11::text").getall()[0]
        if len(response.css("span.t11::text").getall()) == 2: # 최종수정 날짜가 없는 오류 해결
            item['final_date'] = response.css("span.t11::text").getall()[1]
        item['content'] = ''.join(response.css("div#articleBodyContents::text").getall()).replace("\n", "").replace("   ", " ")

        yield item
