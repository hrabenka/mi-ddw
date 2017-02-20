import scrapy


class BlogSpider(scrapy.Spider):
    name = 'bagr'
    allowed_domains = 'petrhejna.org'
    start_urls = ['http://petrhejna.org']

    def parse(self, response):
        for link in response.css('a'):

            name = link.css('a ::text').extract_first()
            if name is not None and name.strip() == '':
                name = link.css('a ::attr(title)').extract_first()

            if name is not None:
                name = name.strip()

            yield {
                'link': link.css('a ::attr(href)').extract_first(),
                'name': name
            }

            for next_page in response.css('a ::attr(href)').extract():
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
