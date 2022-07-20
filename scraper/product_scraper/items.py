import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from unidecode import unidecode


class BaseItem(scrapy.Item):
    source = scrapy.Field()
    default_fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_fields()

    def set_default_fields(self):
        """
        Function that sets default values for items
        For example an AmazonProductItem might want
        set the source to amazon.
        """
        for field, value in self.default_fields.items():
            self[field] = value


class ProductItem(BaseItem):
    url = scrapy.Field(
        input_processor=MapCompose(remove_tags, lambda url: unidecode(url)),
        output_processor=TakeFirst(),
    )
    time_scraped = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            lambda x: x.lower()
            .replace("EU", "")
            .replace("EUR", "")
            .replace("€", "")
            .strip(),
        ),
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )


class OlxItem(ProductItem):
    default_fields = {
        "source": "olx",
    }


class OkaziiItem(OlxItem):
    default_fields = {
        "source": "okazii",
    }
    location_scraped = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    time_posted = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
