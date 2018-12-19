import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class PaulaChoiceSpider(scrapy.Spider):
    name = "paula"
    start_urls = [
            'https://www.paulaschoice.com/ingredient-dictionary?crefn1=name-first-letter&crefv1=1',    
    ]
    
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_ingredient_index,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)

    def parse_ingredient_index(self, response):
        #ingredient links
        next_ingredients = response.css('h2.name.ingredient-name a::attr(href)').extract()        
        for next_ingredient in next_ingredients:
            if next_ingredient is not None:
                next_ingredient = response.urljoin(next_ingredient)
                yield response.follow(next_ingredient, callback=self.parse_ingredient)

        #pagination links
        next_pages = response.xpath('//*[@id="tab-0b8d1cba468f6ceb7ba2796a40"]/div/ul').css('a::attr(href)').extract()
        for next_page in next_pages:            
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield response.follow(next_page, callback=self.parse_ingredient_index)
    
    def parse_ingredient(self, response):
        content = response.xpath('//*[@id="primary"]/div[2]/div/div/div/div')
        for info in content:            
            name  = info.css('div.u-miscellaneous-pagetitle h1::text').extract_first()
            rating = info.css('li span::text').extract_first()
            categories = info.xpath('//*[@id="primary"]/div[2]/div/div/div/div/ul/li[2]').css('a::text').extract()
            description = info.css('div.upper-body p::text').extract_first()
            yield {
                'name': name,
                'rating': rating,
                'categories': categories,
                'description': description
            }

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


