from constants import *
from utils import *
import pickle
from datetime import datetime

class Entities:
    def __init__(self, seed):
        self.seed = {e.uri: e for e in seed}
        self.peripheral = {}

class Entity:
    def __init__(self, uri, types):
        self.uri = uri
        self.types = types
        self.redirects = ["\"" + kw + "\"" for kw in query_redirects(uri) + [uri_to_str(uri)]]
        self.mentions = [] #Dict: uuid, start, end, published_time

    @classmethod
    def add_mention(cls, instance, uuid, start, end, published_time):
        instance.mentions.append({
            "uuid":uuid,
            "start":start,
            "end":end,
            "published_time":published_time
    })

class Article:
    def __init__(self, uuid, title, rank, published, crawled, site):
        self.uuid = uuid
        self.title = title
        self.rank = rank
        self.published = datetime.fromisoformat(published)
        self.crawled = datetime.fromisoformat(crawled)
        self.site = site

if __name__ == "__main__":
    e = Entities([Entity(a, query_types(a)) for a in SEED_ASSETS])
    save("data/seed.pyc", e)
