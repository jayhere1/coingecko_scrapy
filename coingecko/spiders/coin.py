import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.coingecko.com/en']

    script = '''
        function main(splash, args)
      
              headers = {
                ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            
              }
              splash:set_custom_headers(headers)
              splash.private_mode_enabled = false
              
              url=args.url
              assert(splash:go(url))
              assert(splash:wait(5))
              return {
              image = splash:png(),
              html = splash:html()
                }
        end
    
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.coingecko.com/en",
                            callback=self.parse,
                            endpoint="execute",
                            args={"lua_source": self.script})

    def parse(self, response):
        for currency in response.xpath(
                '//table[@class="sort table mb-0 text-sm text-lg-normal table-scrollable"]/tbody/tr'):
            yield {
                "Currency": currency.xpath('normalize-space(.//div[@class="tw-flex"]/div[@class="center"]/a[1]/text())').get(),
                "Currency Price": currency.xpath('.//td[@class="td-price price text-right"]/span/text()').get()
            }

        next_page = response.xpath(
            '//li[@class="page-item next"]/a/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page,
                                 callback=self.parse
                                 )


# scrapy crawl coin -o coinlist.json
