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

with open("data/seed_stories.pyc", "rb") as fp:
    stories = pickle.load(fp)[::-1]

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

    def find_peripheral_sentence():
        pass

story = vars(stories[850])
print(story["_body"])
print(story["_summary"])
print(story["_title"])
