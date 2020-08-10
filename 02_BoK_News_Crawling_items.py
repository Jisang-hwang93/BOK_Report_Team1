# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NaverNewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    media = scrapy.Field()
    upload_date = scrapy.Field()
    final_date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
