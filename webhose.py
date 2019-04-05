from utils import *
from constants import *
from entity import *

from pprint import pprint
from datetime import date
import json
from math import ceil
import os

import webhoseio

CHAR_LIMIT = 4000
BASE_CHARS = 109
Q_CAP = 3100
webhoseio.config(token="6c661f77-9010-47fb-9532-d5fdb563c97a")

#Return list of articles while filtering and updating entities
def parse_and_update(entities, output):
    articles = []
    for post in output["posts"]:
        el = spotlight(post["title"])

        if el is None or "Resources" not in el:
            print("NOT PARSED: " + post["title"])
            continue

        el = el["Resources"]

        if not any([e['@URI'] in entities.seed for e in el]):
            print("NO MATCHING ENTITIES: " + post["title"])
            continue

        for e in el:
            uri = e['@URI']
            if not uri in entities.seed and not uri in entities.peripheral:
                types = [t for t in e['@types'].split(",") if t in DBPEDIA_TYPES_3]

                if not types:
                    continue

                #make new entity
                entities.peripheral[uri] = Entity(uri, types)

            #if it reached here, it must either be in seed or peripheral, or just added to peripheral
            entity = entities.seed[uri] if uri in entities.seed else entities.peripheral[uri]

            Entity.add_mention(entity, post["uuid"], e["@offset"], \
                str(int(e["@offset"]) + len(e["@surfaceForm"])), post["published"])

        articles.append(Article(post["uuid"], post["title"], post["thread"]["domain_rank"], \
            post["published"], post["crawled"], post["thread"]["site"]))

    return articles

#each keyword in keywords wrapped with " "
def query(start_time, end_time, keywords, entities):
    q_str = " OR ".join(keywords)
    #"published:>" + dt_to_posix(start_time) + " published:<" + dt_to_posix(end_time) + \
    q = " domain_rank:<10000 site_type:news language:english title:(" + q_str + ")" + \
        " site_category:(business OR jobs OR financial_news OR international_news OR internet_technology OR investing OR investors_and_patents OR law_government_and_politics OR legal_issues OR national_news OR finance OR stocks OR tech)"

    params = {
        "q":q,
        "format":"json",
        "ts": str(start_time)
    }

    output = webhoseio.query("filterWebContent", params)

    n = output['totalResults']
    print("TOTAL RESULTS: " + str(n))
    print("REQUESTS REMAINING: " + str(output['requestsLeft']))

    """
    if not os.path.isdir("data/articles/" + dirname):
        os.mkdir("data/articles/" + dirname)

    json.dump(output, open("data/articles/" + dirname + "/0.json", "w"))
    """

    articles = parse_and_update(entities, output)

    for i in range(1, ceil(n/100.0)):
        output = webhoseio.get_next()
        articles += parse_and_update(entities, output)
        #json.dump(output, open("data/articles/" + dirname + "/" + str(i) + ".json", "w"))

    return articles

def query_seed(start_time, end_time, entities):
    keywords = [x for e in entities.seed.values() for x in e.redirects]

    #dirname = str(start_time).split(" ")[0] + "_" + str(end_time).split(" ")[0]

    current_batch = []
    current_sum = 0
    i = 0

    #Potentially need intermediate saving if can't fit all articles into RAM
    all_articles = []
    for kw in keywords:
        if len(kw) + 4 + current_sum > Q_CAP:
            all_articles += query(start_time, end_time, current_batch, entities)#, str(i) + "_" + dirname)
            current_batch = []
            current_sum = 0
            i += 1
        else:
            current_batch.append(kw)
            current_sum += len(kw) + 4
    if current_batch:
        all_articles += query(start_time, end_time, current_batch, entities)#, str(i) + "_" + dirname)

    save("data/articles/all_articles.pyc", all_articles)
    save("data/articles/entities.pyc", entities)

if __name__ == "__main__":
    entities = load("data/seed.pyc")
    t = time.time() * 1000
    start = t - 259200000
    query_seed(start, END_TIME, entities)
    print(t)
    """
    articles = load("data/articles/all_articles.pyc")
    for a in articles:
        pprint(vars(a))

    print(len(articles))
    """
