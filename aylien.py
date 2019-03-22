from pprint import pprint
import pickle
import json
from constants import *

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

#Potentially cut down noise by sentiment polarity
opts = {
  'categories_taxonomy': "iptc-subjectcode",
  'language': ['en'],
  'published_at_start': 'NOW-7DAYS',
  'published_at_end': 'NOW',
  'entities_title_links_dbpedia': constants.ASSETS,
  "categories_id": constants.CATEGORIES_ID,
  'source_rankings_alexa_rank_min': 1,
  'source_rankings_alexa_rank_max': 10000, 
  'cursor': '*',
  'per_page': 100,
  '_return':["id", "title", "body", "summary", "source", "entities", "categories", "sentiment", "published_at"]
#  'period': '+10MINUTES',
#  'field': 'entities.title.type'
}

"""
try:
    api_response = api_instance.list_trends(**opts)
    with open("data/trends_type.pyc", "wb") as fp:
        pickle.dump(api_response, fp)
#    counts = [ts.count for ts in api_response.time_series]
#    print(counts)
#    print(sum(counts))
    pprint(vars(api_response))
except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %sn" % e)

#with open("data/aylien_test_article.pyc", "rb") as fp:
#    res = pickle.load(fp)
#    pprint(vars(res))
"""

def fetch_new_stories(params={}):
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

with open("data/seed_stories.pyc", "wb") as fp:
    pickle.dump(fetch_new_stories(opts), fp)
