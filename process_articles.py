from pprint import pprint
import pickle
import datetime

"""
This file analyzes an input unstructured Aylien query of X entities over some time range 
    -assigns each article time_bin value, which is based on an interval_length parameter
    -generates a list of peripheral entities by some heuristic, experimenting with which one
        -mentioned in the same sentence as a hot entity
        -mentioned in the same sentence in the summary
        -mentioned in the title
    -calculates number of mentions, statistics on time between mentions, and time introduced.
"""

with open("data/seed_stories.pyc", "rb") as fp:
    stories = pickle.load(fp)[::-1]
pprint(stories[0].published_at)
pprint(stories[-1].published_at)
class PeripheralEntity:
    def __init__(self, url, types):
        self.mentions = []
        self.url = url
        self.types = types

    def mentions_stats(self):
        pass

class StoryWrapper:
    def __init__(self, story):
        bin_id = 0
