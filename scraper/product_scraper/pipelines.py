import pymongo
import json
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter
from pykafka import KafkaClient


class KafkaPipeline:

    topic_name = "scraped_history"

    def __init__(self, host):
        self.client = KafkaClient(hosts = host)    
        self.producer = self.client.topics[self.topic_name].get_sync_producer()

    

class MongoPipeline:

    collection_name = "scraped_history"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("DB_CONN_STRING"),
            mongo_db=crawler.settings.get("DB_NAME", "scraped_history"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        except pymongo.errors.DuplicateKeyError:
            print(f"Skipping duplicate item {json.dumps(item, indent=4)}")
        return item
