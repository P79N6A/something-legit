from utils import *
from constants import *
from entity import *

from pprint import pprint
from datetime import date
import json
from math import ceil

import webhoseio

CHAR_LIMIT = 4000
BASE_CHARS = 109
Q_CAP = 3890
webhoseio.config(token="6c661f77-9010-47fb-9532-d5fdb563c97a")

#each keyword in keywords wrapped with " "
def query(start_time, end_time, keywords, dirname):

    q = "published:>" + dt_to_posix(start_time) + " published:<" + dt_to_posix(end_time) + \
        " domain_rank:<10000 site_type:news language:english title:(" + q_str + ")"
        #" site_category:(business OR jobs OR financial_news OR international_news OR internet_technology OR investing OR investors_and_patents OR law_government_and_politics OR legal_issues OR national_news OR finance OR stocks OR tech)"

    params = {
        "q":q,
        "format":"json",
    }
    output = webhoseio.query("filterWebContent", params)
    n = output['totalResults']
    print("TOTAL RESULTS: " + str(n))
    print("REQUESTS REMAINING: " + str(output['requestsLeft']))

    json.dump(output, open("data/articles/" + dirname + "/0.json", "w"))

    if output['totalResults'] >= 1000:
        print("Large requests required")
        return

    for i in range(1, ceil(n/100.0)):
        output = webhoseio.get_next()
        json.dump(output, open("data/articles/" + dirname + "/" + str(i) + ".json", "w"))
        


if __name__ == "__main__":
    obj = load("data/seed.pyc")
    query(START_TIME, END_TIME, obj.redirects, str(START_TIME) + "/" + str(END_TIME))
