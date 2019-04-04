import pickle
import time
import requests
from pprint import pprint
from constants import *
import json
import time

from urllib.parse import unquote

from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

import re
parentheses = re.compile(r'\(.*\)')

"""
from flair.data import Sentence
from flair.models import SequenceTagger

tagger = SequenceTagger.load('ner')

def classify_NER(s):
    sentence = Sentence(s)
    tagger.predict(sentence)
    #pprint(sentence.get_spans('ner'))
    return len(sentence.get_spans('ner')) > 0
"""

def uri_to_str(url):
    last = re.sub(parentheses, "", url.split("/")[-1])
    return " ".join([x for x in last.split("_") if x])

def query_redirects(uri):
    sparql.setQuery(
        "select distinct * where {?x dbo:wikiPageRedirects <" + unquote(uri) + ">}"
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return [uri_to_str(d['x']['value']) \
            for d in results['results']['bindings'] \
            if d['x']['type'] == "uri"]

def query_types(uri):
    sparql.setQuery(
            "select ?x where { <" + unquote(uri) + "> rdf:type* ?x; a ?x . ?x a owl:Class .}"
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    s = set()
    for d in results['results']['bindings']:
        t = d['x']['value'].split("/")
        if t[-2] == "ontology":
            s.add(t[-1])
    return s

def category_str(types):
    if 'Person' in types:
        return "person:"
    elif 'Organisation' in types:
        return "organization:"
    return ""

def q_str(uri):
    return " OR ".join(["\"" + kw + "\"" for kw in query_redirects(uri) + [uri_to_str(uri)]])

def dt_to_iso(dt):
    return dt.isoformat() + 'Z'

def dt_to_posix(dt):
    return str(int(dt.timestamp() * 1000))

def save(filename, obj):
    with open(filename, "wb") as fp:
        pickle.dump(obj, fp)

def load(filename):
    with open(filename, "rb") as fp:
        return pickle.load(fp)

#el = "https://api.dbpedia-spotlight.org/en/annotate"
el = "http://localhost:2222/rest/annotate"
def spotlight(s):
    params = {
        "text": s,
        "confidence":0.5,
        #types
    }
    headers = {'Accept': 'application/json'}
    r = requests.get(el, params=params, headers=headers)
    pprint(r.json())

if __name__ == "__main__":
    u1 = "COM, Cisco, Utimaco, Verint, ZTE Corporation Leading the Competition - ResearchAndMarkets.com"
    u2 = "Jack founded ALIBABA in Hangzhou with investments from SoftBank and Goldman"
    u3 = "Walmart's CTO Jeremy King leaves company as e-commerce wars flare - ETtech"
