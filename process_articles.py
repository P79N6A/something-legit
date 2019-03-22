from pprint import pprint
import pickle
import datetime
from constants import *

"""
This file analyzes a news query of X entities over some time range 
    -assigns each article time_bin value, which is based on an interval_length parameter
    -generates a list of peripheral entities by some heuristic; possible heuristics are
        -mentioned in the same sentence as a hot entity
        -mentioned in the same sentence in the summary
        -mentioned in the title
    -calculates number of mentions, statistics on time between mentions, and time introduced.
"""
class PeripheralEntity:
    def __init__(self, url, types):
        self.mentions = []
        self.url = url
        self.types = types

    def mentions_stats(self):
        pass

class StoryWrapper:
    def __init__(self, story):
        self.bin_id = (END_TIME - START_TIME) / INTERVAL_LENGTH
        self.story = story

    def preprocess_title(story):
        pass
    def find_peripheral_title():
        pass

def get_peripheral_entities(stories):
    peripheral_entities = {}
    for story in stories:
        for entity in story.entities.title:
            if not any([t in DBPEDIA_TYPES for t in entity.types]):
                continue
            if not entity.links or not entity.links.dbpedia:
                continue

            url = entity.links.dbpedia
            if url not in peripheral_entities:
                peripheral_entities[url] = PeripheralEntity(url, entity.types)

            peripheral_entities[url].mentions.append(story.published_at)

    #pprint([vars(x) for x in peripheral_entities.values()])
    #print(len(peripheral_entities))

    return peripheral_entities

if __name__ == "__main__":
    with open("data/seed_stories.pyc", "rb") as fp:
        stories = pickle.load(fp)[::-1]

    story = vars(stories[1008])
    print(story["_body"])
    print(story["_summary"])
    print(story["_title"])
    for story in stories:
        if " - " in story.title or "|" in story.title:
            print (story.title)
