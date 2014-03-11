from scrapy.selector import Selector
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from scraper_app.items import WrapBootstrapTemplate


class WrapBootstrapSpider(CrawlSpider):
    """Spider for scraping template information from wrapbootstrap.com"""
    # http://stackoverflow.com/questions/20158534/xpath-run-text-through-regular-expression-to-return-numbers-only
    name = "wrapbootstrap"
    allowed_domains = ["wrapbootstrap.com"]
    start_urls = ["https://wrapbootstrap.com/"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('theme/', )), callback='parse_template'),
        Rule(SgmlLinkExtractor(allow=('themes/', 'tag/')), follow=True),
    )

    def parse_template(self, response):
        """
        Callback used by Scrapy to process downloaded responses
        """
        response_body = response.body_as_unicode()

        coffee = True if 'cups of coffee' in response_body else False
        released_div_pos = 10
        if 'Uses Sass:' in response_body:
            released_div_pos += 1
        if 'Categories:' in response_body:
            released_div_pos += 1

        item_fields = {
            'item_hash': '//*[@id="offer_sku"]/text()',
            'title': '//*[@id="thing_name"]/text()',
            'thumbnail': '//*[@id="thing_image"]/@src',
            'description': '//*[@id="description"]',
            'creator': '//*[@id="product_manufacturer"]/text()',
            'when': '//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[%d]/table/tbody/tr[%d]/td[2]/text()' % ((4, released_div_pos) if coffee else (3, released_div_pos)),
            'bootstrap_version': 'substring-after(normalize-space(//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/table/tbody/tr[2]/td[2]/text()), "Compatible with ")'.format(4 if coffee else 3),
            'cost_single': 'substring-after(normalize-space(//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/div[1]/span/text()), "$")'.format(3 if coffee else 2),
            'cost_multiple': 'substring-after(normalize-space(//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/div[2]/a/span/text()), "$")'.format(3 if coffee else 2),
            'cost_extended': 'substring-after(normalize-space(//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/div[3]/a/span/text()), "$")'.format(3 if coffee else 2),
            'purchases': '//div[@class="purchases"]/span[@class="count"]/text()',
        }

        selector = Selector(response)

        loader = ItemLoader(WrapBootstrapTemplate(), selector=selector)

        # define processors
        loader.default_input_processor = MapCompose(unicode.strip)
        loader.default_output_processor = Join()

        # iterate over fields and add xpaths to the loader
        for field, xpath in item_fields.iteritems():
            loader.add_xpath(field, xpath)
        yield loader.load_item()
