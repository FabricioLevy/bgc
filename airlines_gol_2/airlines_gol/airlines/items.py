# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirlinesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    crawler = scrapy.Field()
    scandate = scrapy.Field()
    departuredate = scrapy.Field()
    arrivaldate = scrapy.Field()
    trajeto = scrapy.Field()
    departurestation = scrapy.Field()
    arrivalstation = scrapy.Field()
    fullfare = scrapy.Field()
    productclass = scrapy.Field()
    
    pass
