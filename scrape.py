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
        dataType = ["pr"]) #"news", "pr", "blogs"]

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

    articles = RequestArticlesInfo(
        page = 1, 
        count = 100, 
        sortBy = "date",
        sortByAsc = False,
        returnInfo = r
        )

    """
    uris = RequestArticlesUriWgtList(
        page = 1,
        count = 50000,
        sortBy = "")

    time = RequestArticlesTimeAggr()
    """

    q.setRequestedResult(articles)

    results = er.execQuery(q) 
    print(results)

    with open(outfile, "w") as fp:
        json.dump(results, fp)

#params["keywords", "concepts", "categories", "sources", "rankStart", "rankEnd"] 
if __name__ == "__main__":

    query("./data/pr.json", {
        "keywords": None, 
        "concepts": QueryItems.OR(["http://en.wikipedia.org/wiki/Apple_Inc.", "http://en.wikipedia.org/wiki/The_Travelers_Companies"]),
        "categories": None,
        "sources": None,
        "rankStart": 0,
        "rankEnd": 30
    })
