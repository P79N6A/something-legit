from constants import *
from utils import *

from pprint import pprint
import pickle
import json
import time

from process_articles import get_peripheral_entities

import aylien_news_api
from aylien_news_api.rest import ApiException

"""
Bulk dataset fetching from Aylien API
"""

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '28be1c03'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '3503112846c98488f353f3693701a0b1'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

BASE_OPTS = {
  'categories_taxonomy': "iptc-subjectcode",
  'language': ['en'],
  "categories_id": CATEGORIES_ID,
  'source_rankings_alexa_rank_min': 1,
  'source_rankings_alexa_rank_max': 10000, 
}


def fetch_time_series(pycfile, start_dt, end_dt, entities=SEED_ASSETS):
    params = {**BASE_OPTS,
    **{
        'entities_title_links_dbpedia': None,
        'published_at_start': dt_to_iso(start_dt),
        'published_at_end': dt_to_iso(end_dt),
        'period': '+1HOUR',
    }}

    ts_lst = []
    i = 0
    while i < len(entities):
        params['entities_title_links_dbpedia'] = entities[i:i+80]
        api_response = api_instance.list_time_series(**params)
        counts = [ts.count for ts in api_response.time_series]
        print(sum(counts))
        ts_lst.append(api_response)
        i += 80

    print("TOTAL: ", end="")
    print(sum([sum([ts.count for ts in x]) for x in ts_lst]))

    with open(pycfile, "wb") as fp:
        pickle.dump(ts_lst, fp)


def print_ts_all_entities(pycfile, start_dt, end_dt, entities):
    params = {**BASE_OPTS,
    **{
        'entities_title_links_dbpedia': None,
        'published_at_start': dt_to_iso(start_dt),
        'published_at_end': dt_to_iso(end_dt),
        'period': '+10HOURS',
    }}

    ts_lst = []
    count_entity_pairs = []
    i = 0
    while i < len(entities):
        params['entities_title_links_dbpedia'] = [entities[i]]
        try:
            api_response = api_instance.list_time_series(**params)
            time.sleep(1.1)
        except ApiException as e:
            if ( e.status == 429 ):
                print('Usage limit are exceeded')
                time.sleep(1)
                continue

        counts = [ts.count for ts in api_response.time_series]
        p = sum(counts), entities[i]
        count_entity_pairs.append(p)
        print(p)
        ts_lst.append(api_response)
        i += 1

    with open(pycfile, "wb") as fp:
        pickle.dump(ts_lst, fp)

    print(sorted(count_entity_pairs))


def fetch_stories(pycfile, start_dt, end_dt, entities=SEED_ASSETS):
    params = {**BASE_OPTS,
    **{
        'entities_title_links_dbpedia': entities,
        'published_at_start': dt_to_iso(start_dt),
        'published_at_end': dt_to_iso(end_dt),
        'cursor': '*',
        'per_page': 4,
        '_return':["id", "title", "body", "summary", "source", "entities", 
            "categories", "sentiment", "published_at"]
    }}
    fetched_stories = []
    stories = None

    while stories is None or len(stories) > 0:
        try:
            response = api_instance.list_stories(**params)
        except ApiException as e:
            if ( e.status == 429 ):
                print('Usage limit are exceeded. Wating for 60 seconds...')
                time.sleep(60)
                continue

        stories = response.stories
        params['cursor'] = response.next_page_cursor

        fetched_stories += stories
        print("Fetched %d stories. Total story count so far: %d" %
            (len(stories), len(fetched_stories)))

        return fetched_stories

    with open(pycfile, "wb") as fp:
        pickle.dump(fetched_stories, fp)

    return fetched_stories

if __name__ == "__main__":
    with open("data/seed_stories.pyc", "rb") as fp:
        stories = pickle.load(fp)[::-1]


    pe = get_peripheral_entities(stories)
    urls = [x.url for x in pe]
    fetch_time_series("data/ner_article_count_week.pyc", START_TIME, END_TIME, entities = urls)
