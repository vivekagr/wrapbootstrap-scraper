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

    def parse(self, response):
        """
        Callback used by Scrapy to process downloaded responses
        //*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[4]/table/tbody/tr[10]/td[2]
        """
        response_body = response.body_as_unicode()

        # Checking if coffee beans are present in the source, since it shifts down the divs
        coffee = True if 'cups of coffee' in response_body else False

        prop_xpath = '//div[@class="info_wrapper"]//tr[td[@class="key"]/strong/text() = "{}:"]/td[@class="value"]/text()'
        substr_xpath = 'substring-after(normalize-space({}), "{}")'

        item_fields = {
            'item_hash': '//*[@id="offer_sku"]/text()',
            'title': '//*[@id="thing_name"]/text()',
            'thumbnail': '//*[@id="thing_image"]/@src',
            'description': '//*[@id="description"]',
            'creator': '//*[@id="product_manufacturer"]/text()',
            'when': prop_xpath.format('Released'),
            'bootstrap_version': substr_xpath.format(prop_xpath.format('Bootstrap'), 'Compatible with '),
            'cost_single': substr_xpath.format('//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/div[1]//span/text()'.format(3 if coffee else 2), '$'),
            'cost_multiple': substr_xpath.format('//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/div[2]//span/text()'.format(3 if coffee else 2), '$'),
            'cost_extended': substr_xpath.format('//*[@id="page_theme"]/div[2]/div/div/div/div[2]/div[{}]/div[3]//span/text()'.format(3 if coffee else 2), '$'),
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
