import scrapy
from scrapy.selector import Selector
import unicodedata
from scrapy_splash import SplashRequest
import json

class ListingsSpider(scrapy.Spider):
    name = 'listings'
    allowed_domains = ['www.centris.ca']

    http_user = 'user'
    http_pass = 'userpass'

    position = {
        "startPosition": 0
    }

    script = '''
        function main(splash, args)
            splash:on_request(function(request)
                if request.url:find('css') then
                    request.abort()
                end
            end)
            splash.images_enabled = false
            splash.js_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
    
        end

    '''


    def start_requests(self):
        yield scrapy.Request(
            url='https://www.centris.ca/UserContext/Lock',
            method='POST',
            headers={
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/json'
            },
            body=json.dumps({'uc': 0}),
            callback=self.generate_uck
        )
        

 
    def generate_uck(self, response):
        uck = response.body
        print(uck)
        query = {"query":{"UseGeographyShapes":0,"Filters":[],"FieldsValues":[{"fieldId":"Category","value":"Residential","fieldConditionId":"","valueConditionId":""},{"fieldId":"SellingType","value":"Sale","fieldConditionId":"","valueConditionId":""},
                {"fieldId":"LandArea","value":"SquareFeet","fieldConditionId":"IsLandArea","valueConditionId":""},{"fieldId":"SalePrice","value":0,"fieldConditionId":"ForSale","valueConditionId":""},
                {"fieldId":"SalePrice","value":10000,"fieldConditionId":"ForSale","valueConditionId":""}]},"isHomePage":True}
        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateQuery",
            method="POST",
            body=json.dumps(query),
            headers={
                'Content-Type': 'application/json',
                'x-requested-with': 'XMLHttpRequest',
                'x-centris-uc': 0,
                'x-centris-uck': uck
            },
            callback=self.update_query
        )

    def update_query(self, response):
        yield scrapy.Request(
            url = "https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            body=json.dumps(self.position),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse
        )

    def parse(self, response):
        resp_dict= json.loads(response.body)
        html = resp_dict.get('d').get('Result').get('html')

        # with open('index2.html', 'w') as f:
        #     f.write(html)

        sel = Selector(text=html)

        
        listtings = sel.xpath("//div[@class='property-thumbnail-item thumbnailItem col-12 col-sm-6 col-md-4 col-lg-3']")
        
        print(len(listtings))

        for listing in listtings:
            cat = listing.xpath("normalize-space(.//div[@class='location-container']//span//div//text())").get()
            add = listing.xpath("normalize-space(.//div[@class='location-container']//span[2]//div[1]//text())").get()
            city = listing.xpath("normalize-space(.//div[@class='location-container']//span[2]//div[2]//text())").get()
            pri = listing.xpath("(.//div[@class='price']//span/text())").get()
            
            url = listing.xpath(".//div[@class='thumbnail property-thumbnail-feature']/a/@href").get()
            abs_url = f"https://www.centris.ca{url}"

            yield SplashRequest(
                url = abs_url,
                endpoint = 'execute',
                callback = self.parse_summary,
                args={
                    'lua_source': self.script
                },
                meta={
                    'cat': cat,
                    'pri': pri,
                    'city': city,
                    'url':abs_url

                }

            )

            count = resp_dict.get('d').get('Result').get('count')
            inc_nm = resp_dict.get('d').get('Result').get('inscNumberPerPage')

            if self.position['startPosition'] <= count:
                self.position['startPosition'] += inc_nm

                yield scrapy.Request(
                    url = "https://www.centris.ca/Property/GetInscriptions",
                    method="POST",
                    body=json.dumps(self.position),
                    headers={
                        'Content-Type': 'application/json'
                    },
                    callback=self.parse
                )


    def parse_summary(self,response):
        address = response.xpath("normalize-space(//div[@class='address']/h2[@itemprop='address']//text())").get()
        desc = response.xpath("normalize-space(//div[@itemprop='description']//text())").get()
        category = response.request.meta['cat']
        price = response.request.meta['pri']
        city = response.request.meta['city']
        url = response.request.meta['url']

        yield{
            "Address": address,
            "Description": desc,
            "category": category,
            "Price": price,
            "city": city,
            "url": url
        }
