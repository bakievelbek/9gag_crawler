# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NinegagItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    interaction_statistics = scrapy.Field()
    created_at = scrapy.Field()
