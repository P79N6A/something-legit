from constants import *
from utils import *
import pickle

class Entities:
    def __init__(self, entities):
        self.entities = entities
        self.q_str = " OR ".join([e.q_str for e in entities])

class Entity:
    def __init__(self, uri, types):
        self.uri = uri
        self.types = types
        #self.category_str = get_category(self.types)
        self.q_str = q_str(uri)

if __name__ == "__main__":
    """
    e = Entities([Entity(a, query_types(a)) for a in SEED_ASSETS])
    pickle_obj("seed_entities.pyc", e)
    pprint(vars(e))
    """
    obj = load("seed_entities.pyc")
    print(obj.q_str)
