from bs4 import BeautifulSoup
import pickle
import lxml

import requests

class Entity:
    def __init__(self, url):
        self.db = url
        self.nicknames = self.get_nicknames(url)


    def get_nicknames(self, url):
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        tags = soup.select('a[rev="dbo:wikiPageRedirects"]')
        return [t.get('href') for t in tags]


class KG:
    def __init__(self, db_string_list):
        self.entities = [Entity(x) for x in db_string_list]

    def to_keyword(self, url):
        s = url.split("/")[-1]
        words = [x for x in s.split("_") if not (x[0] == "(" and x[-1] == ")")]
        return " ".join(words)

if __name__ == "__main__":
    """
    assets = ["http://dbpedia.org/resource/3M","http://dbpedia.org/resource/American_Express", \
        "http://dbpedia.org/resource/Apple_Inc.","http://dbpedia.org/resource/Boeing", \
        "http://dbpedia.org/resource/Caterpillar_Inc.", \
        "http://dbpedia.org/resource/Chevron_Corporation",\
        "http://dbpedia.org/resource/Cisco_Systems","http://dbpedia.org/resource/Coca-Cola", \
        "http://dbpedia.org/resource/ExxonMobil","http://dbpedia.org/resource/Goldman_Sachs", \
        "http://dbpedia.org/resource/The_Home_Depot","http://dbpedia.org/resource/IBM", \
        "http://dbpedia.org/resource/Intel","http://dbpedia.org/resource/Johnson_%26_Johnson", \
        "http://dbpedia.org/resource/JPMorgan_Chase","http://dbpedia.org/resource/McDonald%27s",\
        "http://dbpedia.org/resource/Merck_%26_Co.","http://dbpedia.org/resource/Microsoft", \
        "http://dbpedia.org/resource/Procter_%26_Gamble", \
        "http://dbpedia.org/resource/Nike,_Inc.","http://dbpedia.org/resource/Pfizer",\
        "http://dbpedia.org/resource/The_Travelers_Companies",\
        "http://dbpedia.org/resource/UnitedHealth_Group",\
        "http://dbpedia.org/resource/United_Technologies",\
        "http://dbpedia.org/resource/Verizon_Communications",\
        "http://dbpedia.org/resource/Visa_Inc.","http://dbpedia.org/resource/Walmart",\
        "http://dbpedia.org/resource/The_Walt_Disney_Company"] 

    kg = KG(assets)
    print([kg.to_keyword(entity.nicknames[0]) for entity in kg.entities])        
    with open("data/entities.pyc", "wb") as fp:
        pickle.dump(kg, fp)
    """
    with open("data/entities.pyc", "rb") as fp:
        kg = pickle.load(fp)
    print ([kg.to_keyword(x) for x in kg.entities[0].nicknames])



