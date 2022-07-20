from product_scraper.utils.url_builder import OlxUrlBuilder
from product_scraper.utils.url_config import OLX_CATEGORIES, OLX_CITIES
import unittest
import random
import requests
from scrapy.crawler import CrawlerProcess
import json
import os


class TestOlxUrlBuilder(unittest.TestCase):
    # Invalid values for parameters test cases

    # Invalid category case
    def testInvalidCategory(self):
        with self.assertRaises(ValueError):
            city = random.choice(list(OLX_CITIES.keys()))
            OlxUrlBuilder.build("invalid", city)

    # Invalid city case
    def testInvalidCity(self):
        with self.assertRaises(ValueError):
            category = random.choice(list(OLX_CATEGORIES.keys()))
            OlxUrlBuilder.build(category, "invalid")

    # Invalid page number case
    def testStringForPage(self):
        with self.assertRaises(ValueError):
            category = random.choice(list(OLX_CATEGORIES.keys()))
            city = random.choice(list(OLX_CITIES.keys()))
            OlxUrlBuilder.build(category, city, page="invalid")

    # Invalid page number case
    def testNegativePageNo(self):
        with self.assertRaises(ValueError):
            category = random.choice(list(OLX_CATEGORIES.keys()))
            city = random.choice(list(OLX_CITIES.keys()))
            OlxUrlBuilder.build(category, city, page=-2)

    # Testing behavior with empty params

    # No category
    def testNoCategory(self):
        city = random.choice(list(OLX_CITIES.keys()))
        assert OlxUrlBuilder.build(category=None, city=city)

    # No city
    def testNoCity(self):
        category = random.choice(list(OLX_CATEGORIES.keys()))
        assert OlxUrlBuilder.build(category=category)

    # Testing all URL combinations
    # For now we skip because it just takes too long
    # TODO: Remove skip
    @unittest.skip
    def testAllUrlCombinations(self):
        categories = [*OLX_CATEGORIES.keys(), None]
        cities = [*OLX_CITIES.keys(), None]

        for category in categories:
            for city in cities:
                url = OlxUrlBuilder.build(category, city)
                assert requests.get(url).status_code == 200
