import scrapy


class DamejidloSpider(scrapy.Spider):
    name = 'Damejidlo'
    allowed_domains = ['damejidlo.cz', 'www.damejidlo.cz']
    start_urls = ['http://damejidlo.cz']

    def parse(self, response):
        food_selector = './/li[@class="menu__list-item" or @class="menu__list-item menu__list-item--without-image"]'
        for food in response.xpath(food_selector):
            food_text = food.css('div.food-text')

            food_title = food_text.css('h5.food-text__title')

            name = food_title.css('a ::text').extract_first()
            description = food_text.css('div.food-text__description ::text').extract_first()

            food_right_box = food.css('div.food-lastbox')
            food_values = food_right_box.css('div.food-values')

            food_price = food_values.css('span.food-values__price ::text').extract_first()

            yield {
                'name': name.strip() if name is not None else None,
                'description': description.strip() if description is not None else None,
                'url': food_title.css('a ::attr(href)').extract_first().strip(),
                'price': food_price.strip() if food_price is not None else None,
            }

        for next_page in response.css('a ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
