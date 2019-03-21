import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint
import pickle
import json

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '28be1c03'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '3503112846c98488f353f3693701a0b1'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

ASSETS = ["http://dbpedia.org/resource/3M",\
        "http://dbpedia.org/resource/American_Express",\
        "http://dbpedia.org/resource/Apple_Inc.",\
        "http://dbpedia.org/resource/Boeing",\
        "http://dbpedia.org/resource/Caterpillar_Inc.",\
        "http://dbpedia.org/resource/Chevron_Corporation",\
        "http://dbpedia.org/resource/Cisco_Systems",\
        "http://dbpedia.org/resource/Coca-Cola",\
        "http://dbpedia.org/resource/ExxonMobil",\
        "http://dbpedia.org/resource/Goldman_Sachs",\
        "http://dbpedia.org/resource/The_Home_Depot",\
        "http://dbpedia.org/resource/IBM",\
        "http://dbpedia.org/resource/Intel",\
        "http://dbpedia.org/resource/Johnson_%26_Johnson",\
        "http://dbpedia.org/resource/JPMorgan_Chase",\
        "http://dbpedia.org/resource/McDonald%27s",\
        "http://dbpedia.org/resource/Merck_%26_Co.",\
        "http://dbpedia.org/resource/Microsoft",\
        "http://dbpedia.org/resource/Nike,_Inc.",\
        "http://dbpedia.org/resource/Pfizer",\
        "http://dbpedia.org/resource/Procter_%26_Gamble",\
        "http://dbpedia.org/resource/The_Travelers_Companies",\
        "http://dbpedia.org/resource/UnitedHealth_Group",\
        "http://dbpedia.org/resource/United_Technologies",\
        "http://dbpedia.org/resource/Verizon_Communications",\
        "http://dbpedia.org/resource/Visa_Inc.",\
        "http://dbpedia.org/resource/Walmart",\
        "http://dbpedia.org/resource/The_Walt_Disney_Company",\
        "http://dbpedia.org/resource/Dow_Jones_Industrial_Average",\
        "http://dbpedia.org/page/New_York_Stock_Exchange",\
        "http://dbpedia.org/page/NASDAQ",\
        "http://dbpedia.org/page/United_States_dollar",\
        "http://dbpedia.org/page/Economy_of_the_United_States"\
        ] 

DBPEDIA_TYPES = {"Currency", "Employer", "Broadcaster", "Company", \
    "EducationalInstitution", "EmployersOrganisation", "GeopoliticalOrganisation",\
    "GovernmentAgency", "InternationalOrganisation", "Legislature", "Non-ProfitOrganisation",\
    "PoliticalParty", "ReligiousOrganisation", "TermOfOffice", "TradeUnion", "Artist", \
    "Athlete", "BusinessPerson", "Criminal", "Economist", "Engineer", "Journalist", "Judge",\
    "Lawyer", "MilitaryPerson", "OfficeHolder", "Politician", "Scientist", "Writer", \
    "Meeting", "AcademicConference", "Convention", "Election", "Software"}

CATEGORIES_ID = ["01026002", "02000000", "03000000", "04000000", "09000000", "11000000", "13000000"]

#Potentially cut down noise by sentiment polarity
opts = {
  'categories_taxonomy': "iptc-subjectcode",
  'language': ['en'],
  'published_at_start': 'NOW-7DAYS',
  'published_at_end': 'NOW',
  'entities_title_links_dbpedia': ASSETS,
  "categories_id": CATEGORIES_ID,
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
