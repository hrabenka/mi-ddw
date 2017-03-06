import scrapy


class BlogSpider(scrapy.Spider):
    name = 'bagr'
    start_urls = ['http://localhost:8000']

    def parse(self, response):
        for person in response.css('div.person'):
            yield {
                'name': person.css('span.name ::text').extract_first(),
                'phone': person.css('span.phone ::text').extract_first(),
                'gender': person.css('span.gender ::text').extract_first(),
                'age': person.css('span.age ::text').extract_first(),
            }

        for next_page in response.css('a ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
