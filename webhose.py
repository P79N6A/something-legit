import webhoseio
from utils import *
from constants import *
from pprint import pprint
from datetime import date

webhoseio.config(token="6c661f77-9010-47fb-9532-d5fdb563c97a")
def query(start_time , end_time , q_str):
    q = "published:>" + dt_to_posix(start_time) + " published:<" + dt_to_posix(end_time) + \
    " domain_rank:<10000 site_type:news language:english (" + q_str + ")"
    #(site_category:business OR site_category:jobs OR site_category:financial_news OR site_category:international_news OR site_category:internet_technology OR site_category:investing OR site_category:investors_and_patents OR site_category:law_government_and_politics OR site_category:legal_issues OR site_category:national_news OR site_category:finance OR site_category:stocks OR site_category:tech)"

    params = {
        "q":q,
        "format":"json",
    }
    output = webhoseio.query("filterWebContent", params)
    pprint(output)
    print(output['totalResults'])
    print(output['requestsLeft'])

if __name__ == "__main__":
    pass
