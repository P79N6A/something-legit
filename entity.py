from constants import *
from utils import *
import pickle

class Entities:
    def __init__(self, entities):
        self.entities = {e.uri: e for e in entities}
        self.tracked =  set(self.entities.keys())

    def redirects(self):
        return [x for e in self.entities.values() for x in e.redirects]
class Entity:
    def __init__(self, uri, types):
        self.uri = uri
        self.types = types
        self.redirects = ["\"" + kw + "\"" for kw in query_redirects(uri) + [uri_to_str(uri)]]

if __name__ == "__main__":
    e = Entities([Entity(a, query_types(a)) for a in SEED_ASSETS])
    save("data/seed.pyc", e)
