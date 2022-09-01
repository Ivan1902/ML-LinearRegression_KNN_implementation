# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PolovniautomobiliItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field() #marka
    city = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    subcategory = scrapy.Field() #karoserija
    productionYear = scrapy.Field()
    engineCapacity = scrapy.Field() #kubikaza
    enginePower = scrapy.Field() #snaga motora
    kilometers = scrapy.Field() #kilometraza
    gearshift = scrapy.Field() #menjac - 1 - automatski / 0 - manuelni
    seatsNumber = scrapy.Field()
    model = scrapy.Field()
    new_used = scrapy.Field() # stanje - 1 - novo / 0 - polovno
    registrated = scrapy.Field()
    engineClass = scrapy.Field()
