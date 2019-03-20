from eventregistry import *
import json
from datetime import date
er = EventRegistry(apiKey = "779f3fab-98fe-4b4d-9e49-fa9e652e1ea3")

TRAINING_STARTDATE = date(year = 2018, month = 1, day = 1) 
TRAINING_ENDDATE = date(year = 2018, month = 12, day = 31)

"""
For each set of query parameter configurations: 
    -check distribution of articles, 
    -check average articles per time bin, 
    -check relevance of articles
Source control:
    -Use rank
    -Hand pick set of trusted sources
params["keywords", "concepts", "categories", "sources", "rankStart", "rankEnd"] 
"""

def query(outfile, params):
    q = QueryArticles(
        keywords = params["keywords"], 
        conceptUri = params["concepts"],
        categoryUri = params["categories"], 
        sourceUri = params["sources"], 
        sourceLocationUri = None,
        sourceGroupUri = None,
        authorUri = None,
        locationUri = None,
        lang = "eng",
        dateStart = TRAINING_STARTDATE,
        dateEnd = TRAINING_ENDDATE,
        dateMentionStart = None,
        dateMentionEnd = None,
        keywordsLoc = "title",
        ignoreKeywords = None,
        ignoreConceptUri = None,
        ignoreCategoryUri = None,
        ignoreSourceUri = None,
        ignoreSourceLocationUri = None,
        ignoreSourceGroupUri = None,
        ignoreAuthorUri = None,
        ignoreLocationUri = None,
        ignoreLang = None,
        ignoreKeywordsLoc = "body",
        isDuplicateFilter = "keepAll",
        hasDuplicateFilter = "keepAll",
        eventFilter = "keepAll",
        startSourceRankPercentile = params["rankStart"], #experiment with this
        endSourceRankPercentile = params["rankEnd"],
        dataType = ["news", "pr", "blogs"])

    r = ReturnInfo(articleInfo = ArticleInfoFlags(
        bodyLen = -1,
        title = True,
        basicInfo = True,
        body = True,
        url = True,
        eventUri = True,
        authors = True,
        concepts = True,
        categories = True,
        links = False,
        videos = False,
        image = False,
        socialScore = True,
        sentiment = True,
        location = False,
        dates = False,
        extractedDates = False,
        duplicateList = False,
        originalArticle = False,
        storyUri = False))

    """
    articles = RequestArticlesInfo(
        page = 1, 
        count = 100, 
        sortBy = "date",
        sortByAsc = False,
        returnInfo = r
        )

    uris = RequestArticlesUriWgtList(
        page = 1,
        count = 50000,
        sortBy = "")
    """

    time = RequestArticlesTimeAggr()

    q.setRequestedResult(time)

    results = er.execQuery(q) 
    print(results)

    with open(outfile, "w") as fp:
        json.dump(results, fp)

#params["keywords", "concepts", "categories", "sources", "rankStart", "rankEnd"] 
if __name__ == "__main__":
    assets1 = ["http://en.wikipedia.org/wiki/3M","http://en.wikipedia.org/wiki/American_Express","http://en.wikipedia.org/wiki/Apple_Inc.","http://en.wikipedia.org/wiki/Boeing","http://en.wikipedia.org/wiki/Caterpillar_Inc.","http://en.wikipedia.org/wiki/Chevron_Corporation","http://en.wikipedia.org/wiki/Cisco_Systems","http://en.wikipedia.org/wiki/Coca-Cola","http://en.wikipedia.org/wiki/ExxonMobil","http://en.wikipedia.org/wiki/Goldman_Sachs","http://en.wikipedia.org/wiki/The_Home_Depot","http://en.wikipedia.org/wiki/IBM","http://en.wikipedia.org/wiki/Intel","http://en.wikipedia.org/wiki/Johnson_%26_Johnson"]
    assets2 = ["http://en.wikipedia.org/wiki/JPMorgan_Chase","http://en.wikipedia.org/wiki/McDonald%27s","http://en.wikipedia.org/wiki/Merck_%26_Co.","http://en.wikipedia.org/wiki/Microsoft","http://en.wikipedia.org/wiki/Nike,_Inc.","http://en.wikipedia.org/wiki/Pfizer","http://en.wikipedia.org/wiki/Procter_%26_Gamble","http://en.wikipedia.org/wiki/The_Travelers_Companies","http://en.wikipedia.org/wiki/UnitedHealth_Group","http://en.wikipedia.org/wiki/United_Technologies","http://en.wikipedia.org/wiki/Verizon_Communications","http://en.wikipedia.org/wiki/Visa_Inc.","http://en.wikipedia.org/wiki/Walmart","http://en.wikipedia.org/wiki/The_Walt_Disney_Company"] 

    query("./data/all_time1.json", {
        "keywords": None, 
        "concepts": QueryItems.OR(assets1),
        "categories": None,
        "sources": None,
        "rankStart": 0,
        "rankEnd": 30
    })   
    
    query("./data/all_time2.json", {
        "keywords": None, 
        "concepts": QueryItems.OR(assets2),
        "categories": None,
        "sources": None,
        "rankStart": 0,
        "rankEnd": 30
    })
