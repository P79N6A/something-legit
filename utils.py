from flair.data import Sentence
from flair.models import SequenceTagger
import pickle
from pprint import pprint
tagger = SequenceTagger.load('ner')

def url_to_str(url):
    last = url.split("/")[-1]
    tokens = [x for x in last.split("_") if not (x[0] == '(' and x[-1] == ')')]
    return " ".join(tokens)

def classify_NER(s):
    sentence = Sentence(s)
    tagger.predict(sentence)
    #pprint(sentence.get_spans('ner'))
    return len(sentence.get_spans('ner')) > 0

def dt_to_iso(dt):
    return dt.isoformat() + 'Z'

def pprint_pyc(filename):
    with open(filename, "rb") as fp:
        pprint(vars(pickle.load(fp)))


if __name__ == "__main__":
    print(classify_NER(url_to_str('http://dbpedia.org/resource/Instagram')))
