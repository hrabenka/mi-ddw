import scrapy


class DamejidloSpider(scrapy.Spider):
    name = 'Damejidlo'
    allowed_domains = ['damejidlo.cz', 'www.damejidlo.cz']
    start_urls = ['http://damejidlo.cz/']

    def parse(self, response):
        for link in response.css('a'):

            url = link.css('a ::attr(href)').extract_first()

            if url.startswith(''):
                yield {'url': url}

            for next_page in response.css('a ::attr(href)').extract():
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
