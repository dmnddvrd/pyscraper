import scrapy
from product_scraper.utils.url_builder import OlxUrlBuilder
from product_scraper.utils.url_config import OLX_CATEGORIES, OLX_CITIES
from product_scraper.items import OlxItem, OkaziiItem
from scrapy.loader import ItemLoader
from datetime import datetime


class BaseSpider(scrapy.Spider):
    """
    :param css_item_fields: a dictionary where each key is the name of the field in the corresponding ItemLoader
        and each value is the css selector to it
    :type css_item_fields: dict
    :param xpath_item_fields: a dictionary where each key is the name of the field in the corresponding ItemLoader
        and each value is the xpath selector to it
    :type xpath_item_fields: dict
    :param base_field_css: css selector to the item to be scraped
    :type base_field_css: str
    :param base_field_xpath: xpath selector to the item to be scraped
    :type base_field_css: str
    :param item_loader_cls: a Class that is a subclass of scrapy.Item
    :type item_loader_cls: scrapy.Item
    NOTE: Only one of the above should be declared
    """

    css_item_fields = {}
    xpath_item_fields = {}
    base_field_css = None
    base_field_xpath = None
    item_loader_cls = None

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        # If no fields are specified to be extracted we raise an error
        if not (self.css_item_fields) and not (self.xpath_item_fields):
            raise ValueError(
                "You must set at least one of css_item_fields or xpath_item_fields dictionaries containing item_field, css_field pairs."
            )
        # If both were declared we raise an error
        if self.base_field_css and self.base_field_xpath:
            raise ValueError(
                "You must set only either of the base-field_css or base_field_xpath."
            )
        elif not self.base_field_css and not self.base_field_xpath:
            raise ValueError(
                "You must set at least one of the base-field_css or base_field_xpath."
            )
        if not self.item_loader_cls:
            raise ValueError("You must provide the item_loader_cls to the spider")
        if not issubclass(self.item_loader_cls, scrapy.Item):
            raise ValueError(
                "Class attribute item_loader_cls has to be subclass of scrapy.Item"
            )

    def parse(self, response):
        if self.base_field_css:
            items = response.css(self.base_field_css)
        elif self.base_field_xpath:
            items = response.xpath(self.xpath_item_fields)
        for item in items:
            item_loader = ItemLoader(item=self.item_loader_cls(), selector=item)
            # Css fields
            for item_field, css_field in self.css_item_fields.items():
                item_loader.add_css(item_field, css_field)
            # XPath fields
            for item_field, xpath_field in self.xpath_item_fields.items():
                item_loader.add_css(item_field, xpath_field)
            # Default field:
            item_loader.add_value(
                "time_scraped", datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
            )
            yield item_loader.load_item()


class OkaziiSpider(BaseSpider):
    name = "okazii"
    item_loader_cls = OkaziiItem
    start_urls = ["https://www.okazii.ro/telefoane-huawei/?pret_curr=EUR"]
    base_field_css = ".list-item"
    css_item_fields = {
        "url": ".item-title h2 a::attr(href)",
        "title": ".item-title h2 a::text",
        "price": "span.prSup span::text",
    }


class OlxSpider(BaseSpider):
    name = "olx"
    item_loader_cls = OlxItem
    base_field_css = "li.wrap"
    start_urls = [
        OlxUrlBuilder.build(category, city, page)
        for category in OLX_CATEGORIES.keys()
        for city in OLX_CITIES.keys()
        for page in range(1, 2)
    ]
    css_item_fields = {
        "title": "a::attr(title)",
        "price": "div.price::text",
        "url": "li.wrap a.link::attr(href)",
        "time_posted": "ul.date-location li:nth-child(even)::text",
        "location_scraped": "ul.date-location li:nth-child(odd)::text",
    }
