#scrapy crawl polovniautomobili - runovanje
#scrapy shell "https://www.polovniautomobili.com/"
from http import HTTPStatus
from unicodedata import decimal
from urllib import response
from urllib.parse import urlparse
import requests
import scrapy
from scrapy import Selector
from ..items import PolovniautomobiliItem
import re
import json
import httplib2
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import TextResponse

class PolovniAutomobiliSpider(scrapy.Spider):
    name = 'polovniautomobili'
    page = 2
    start_urls = ['https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=basic&city_distance=0&showOldNew=all&without_price=1']
    #baseUrl = 'https://www.polovniautomobili.com/Homepage/refreshAds/26/'
    while(page < 850):
        urlToCrawl = 'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=' + str(page) + '&sort=basic&city_distance=0&showOldNew=all&without_price=1'
        start_urls.append(urlToCrawl)
        page = page + 1 

    def parse(self, response):
        
        urls = response.css('a.firstImage::attr(href)').extract()

        for url in urls:
            urlToGo = 'https://www.polovniautomobili.com' + url
            yield scrapy.Request(urlToGo, callback=self.parse_item)
            
        
    def parse_item(self, response):
        
        item = PolovniautomobiliItem()

        infoBoxes = response.css('div.infoBox').extract()
        for infoBox in infoBoxes:
            infoBox = self.makeHttpFromString(infoBox)
            if(infoBox.css('h2.classified-title::text').extract_first()== 'Opšte informacije'):
                dividers = infoBox.css('div.divider').extract()
                for divider in dividers:
                    divider = self.makeHttpFromString(divider)
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Marka'):
                        item['brand'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()

                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Model'):
                        item['model'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Godište'):
                        item['productionYear'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if(item['productionYear'] is not None):
                            item['productionYear'] = int(item['productionYear'].removesuffix('.'))
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Kilometraža'):
                        item['kilometers'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if(item['kilometers'] is not None):
                            item['kilometers'] = float(item['kilometers'].removesuffix('km').replace('.', ''))
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Karoserija'):
                        item['subcategory'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Kubikaža'):
                        item['engineCapacity'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if(item['engineCapacity'] is not None):
                            item['engineCapacity'] = float(item['engineCapacity'].removesuffix('cm'))
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Snaga motora'):
                        item['enginePower'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if(item['enginePower'] is not None):
                            item['enginePower'] = item['enginePower'].removesuffix('(kW/KS)').strip().split('/')[0]

                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Stanje:'):
                        item['new_used'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if(item['new_used'] is not None):
                            if("NOVO" in item['new_used'].upper()):
                                item['new_used'] = True
                            else:
                                item['new_used'] = False
            
            elif(infoBox.css('h2.classified-title::text').extract_first() == 'Dodatne informacije '):
                dividers = infoBox.css('div.divider').extract()
                for divider in dividers:
                    divider = self.makeHttpFromString(divider)
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Menjač'):
                        item['gearshift'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if("AUTOMATSKI" in item['gearshift'].upper()):
                            item['gearshift'] = True
                        elif("MANUELNI" in item['gearshift'].upper()):
                            item['gearshift'] = False
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Boja'):
                        item['color'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()

                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Emisiona klasa motora'):
                        item['engineClass'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                    
                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Broj sedišta'):
                        item['seatsNumber'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if(item['seatsNumber'] is not None):
                            item['seatsNumber'] = int(item['seatsNumber'].replace('sedišta', '').strip())

                    if(divider.css('div.uk-width-1-2::text').extract_first() == 'Registrovan do'):
                        item['registrated'] = divider.css('div.uk-width-1-2.uk-text-bold::text').extract_first()
                        if("NIJE" in item['registrated'].upper()):
                            item['registrated'] = False
                        else:
                            item['registrated'] = True
        
        item['city'] = response.css('aside.table-cell.side.uk-hidden-medium.uk-hidden-small.width-320').css('div.uk-grid.uk-margin-top-remove').css('div.uk-width-1-2::text').extract_first()
        if(item['city'] is not None):
            item['city'] = item['city'].strip()

        item['price'] = response.css('span.priceClassified.discountedPriceColor::text').extract_first() 
        if(item['price'] is None):
            item['price'] = response.css('span.priceClassified.regularPriceColor::text').extract_first()       
        
        if(item['price'] is not None):
            item['price'] = float(item['price'].removesuffix('€').strip().replace('.', ''))
       
        yield item

    def makeHttpFromString(self, text):
        return (TextResponse( encoding='utf-8',url='optional',body=bytes(text, 'utf-8')))

