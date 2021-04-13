import scrapy
from scrapy_selenium import SeleniumRequest

class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'

    def remove_char(self, value):
        return value.strip('\xa0')
    
    def start_requests(self):
        yield SeleniumRequest (
            url= 'https://slickdeals.net/computer-deals/',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )


    def parse(self, response):

       products = response.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
       
       for p in products:
           yield{
               'Name': p.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/text()").get(),
               'Link': p.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get(),
               'Store_Name': p.xpath(".//button[@class='itemStore bp-p-storeLink bp-c-linkableButton  bp-c-button js-button bp-c-button--link']/text()").get(),
               'Price': p.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
           }

       nxt_pg = response.xpath("//a[@data-role='next-page']/@href" ).get()
       
       if nxt_pg:
           ab_url = f"https://slickdeals.net{nxt_pg}"
           yield SeleniumRequest(
               url=ab_url,
               wait_time=3,
               screenshot=True,
               callback=self.parse
           )
