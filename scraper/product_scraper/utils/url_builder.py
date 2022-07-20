from multiprocessing.sharedctypes import Value
from .url_config import OLX_CATEGORIES, OLX_CITIES


class OlxUrlBuilder(object):
    BASE_URL = "https://www.olx.ro"
    VIEW_FILTER = "view=galleryWide"
    CURRENCY_FILTER = "currency=EUR"

    @classmethod
    def build(cls, category=None, city=None, page=1):
        """
        :param category: a key from the ./url_config.py file pointing to slug
        :type category: string
        :param city: same as category but for cities
        :type city: string
        :param page: pagination for page
        :type page: int
        """
        slugs = [cls.BASE_URL]
        try:
            page = int(page)
            if page < 0:
                raise ValueError("Page must be a positive integer")
        except ValueError as ex:
            raise ValueError(f"Page number was not an integer")

        # Checking if it's valid
        if category and category not in OLX_CATEGORIES.keys():
            raise ValueError(f"Invalid category {category}")
        if city and city not in OLX_CITIES.keys():
            raise ValueError(f"Invalid city {city}")

        # Getting slug if it's valid and appending
        if category and OLX_CATEGORIES.get(category):
            slugs.append(OLX_CATEGORIES.get(category))
        if city and OLX_CITIES.get(city):
            slugs.append(OLX_CITIES.get(city))

        filters = [cls.VIEW_FILTER, cls.CURRENCY_FILTER, f"page={page}"]
        # View and page no. are always last
        slugs.append("?" + "&".join(filters))
        return "/".join(slugs)


class OkaziiUrlBilder(object):
    """
    For some reason Okazii does not offer a
    Url param for querying for location based filtering
    """

    BASE_URL = "https://www.okazii.ro"
    CURRENCY_FILTER = "pret_curr=EUR"

    @classmethod
    def build(cls, category=None, page=1):
        slugs = [cls.BASE_URL]
        try:
            page = int(page)
            if page < 0:
                raise ValueError("Page must be a positive integer")
        except ValueError as ex:
            raise ValueError(f"Page number was not an integer")
        # Checking if it's valid
        if category and category not in OLX_CATEGORIES.keys():
            raise ValueError(f"Invalid category {category}")
        # Getting slug if it's valid and appending
        if category and OLX_CATEGORIES.get(category):
            slugs.append(OLX_CATEGORIES.get(category))
