# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.selector import Selector
from w3lib.html import remove_tags  
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def remove_html(re):
    clean =''
    try:
        clean = remove_tags(re)
    except TypeError:
        clean = 'No reviews'
    return clean


def get_platforms(one_class):
    platforms = []
    
    platform = one_class.split(' ')[-1]
    if platform == 'win':
        platforms.append('Windows')
    if platform == 'mac':
        platforms.append('Mac os')
    if platform == 'linux':
        platforms.append('Linux')
    if platform == 'vr_supported':
        platforms.append('vr_supported')
    if platform == 'vr_required':
         platforms.append('VR Only')
    return platforms

def clean_discount(d):
    if d:
        return d.lstrip('-')
    return d

def price(html_markup):
    op = ''
    selector_obj = Selector(text=html_markup)
    div_disscount= selector_obj.xpath(".//div[contains(@class,'search_price discounted')]")
    if len(div_disscount) > 0:
        op = div_disscount.xpath('.//span/strike/text()').get()
    else:
        op = selector_obj.xpath(".//div[contains(@class, 'search_price')]/text()").getall()
    return op

def clean_price (p):
    if p:
        return p.strip()
    return p

class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    game_url            = scrapy.Field(output_processor = TakeFirst())
    img_url             = scrapy.Field(output_processor = TakeFirst())
    game_name           = scrapy.Field(output_processor = TakeFirst())
    release_date        = scrapy.Field(output_processor = TakeFirst())
    platform            = scrapy.Field(
        input_processor = MapCompose(get_platforms)
    )
    review_summary      = scrapy.Field( 
        input_processor = MapCompose(remove_html),
        output_processor = TakeFirst()
    )
    original_price      = scrapy.Field(
        input_processor = MapCompose(price,str.strip),
        output_processor = Join('')
    )
    discounted_price    = scrapy.Field( 
        input_processor = MapCompose(clean_price),
        output_processor = TakeFirst()

    )
    discounted_rate     = scrapy.Field(
        input_processor = MapCompose(clean_discount),
        output_processor = TakeFirst()

    )
    
