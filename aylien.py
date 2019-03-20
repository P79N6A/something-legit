import aylien_news_api
import pickle
from aylien_news_api.rest import ApiException
import json

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '28be1c03'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '3503112846c98488f353f3693701a0b1'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

assets = ["http://dbpedia.org/resource/3M","http://dbpedia.org/resource/American_Express","http://dbpedia.org/resource/Apple_Inc.","http://dbpedia.org/resource/Boeing","http://dbpedia.org/resource/Caterpillar_Inc.","http://dbpedia.org/resource/Chevron_Corporation","http://dbpedia.org/resource/Cisco_Systems","http://dbpedia.org/resource/Coca-Cola","http://dbpedia.org/resource/ExxonMobil","http://dbpedia.org/resource/Goldman_Sachs","http://dbpedia.org/resource/The_Home_Depot","http://dbpedia.org/resource/IBM","http://dbpedia.org/resource/Intel","http://dbpedia.org/resource/Johnson_%26_Johnson","http://dbpedia.org/resource/JPMorgan_Chase","http://dbpedia.org/resource/McDonald%27s","http://dbpedia.org/resource/Merck_%26_Co.","http://dbpedia.org/resource/Microsoft","http://dbpedia.org/resource/Nike,_Inc.","http://dbpedia.org/resource/Pfizer","http://dbpedia.org/resource/Procter_%26_Gamble","http://dbpedia.org/resource/The_Travelers_Companies","http://dbpedia.org/resource/UnitedHealth_Group","http://dbpedia.org/resource/United_Technologies","http://dbpedia.org/resource/Verizon_Communications","http://dbpedia.org/resource/Visa_Inc.","http://dbpedia.org/resource/Walmart","http://dbpedia.org/resource/The_Walt_Disney_Company"] 

opts = {
  'categories_taxonomy': "iptc-subjectcode",
  'language': ['en'],
  'published_at_start': 'NOW-7DAYS',
  'published_at_end': 'NOW',
  'source_rankings_alexa_rank_min': 1,
  'entities_title_links_dbpedia': assets,
  'source_rankings_alexa_rank_max': 10000, 
  'per_page': 1,
#  'period': '+10MINUTES',
  '_return':["id", "title", "body", "summary", "source", "entities", "categories", \
      "sentiment", "published_at"]
}

#Potentially cut down noise by: categories, sentiment polarity, relevance, entity in title

try:
#    api_response = api_instance.list_stories(**opts)
#    with open("data/aylien_test_article.pyc", "wb") as fp:
#        pickle.dump(api_response, fp)
#    counts = [ts.count for ts in api_response.time_series]
#    print(counts)
#    print(sum(counts))
    pass
except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %sn" % e)

from pprint import pprint
with open("data/aylien_test_article.pyc", "rb") as fp:
    res = pickle.load(fp)
    pprint(vars(res))
