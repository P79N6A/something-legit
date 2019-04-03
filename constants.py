import datetime

SEED_ASSETS = ["http://dbpedia.org/resource/3M",\
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
        "http://dbpedia.org/resource/New_York_Stock_Exchange",\
        "http://dbpedia.org/resource/NASDAQ",\
        "http://dbpedia.org/resource/United_States_dollar",\
        "http://dbpedia.org/resource/Economy_of_the_United_States",
        "http://dbpedia.org/resource/Stock_market",
        ] 

CATEGORIES_ID = ["01026002", "02000000", "03000000", "04000000", "09000000", "11000000", "13000000"]

START_TIME = datetime.datetime(2019, 3, 14, 4, 40, 14)
END_TIME = datetime.datetime(2019, 3, 21, 4, 40, 14)

INTERVAL_LENGTH = datetime.timedelta(minutes=10)

DBPEDIA_TYPES = {"Currency", "Employer", "Broadcaster", "Company", \
    "EducationalInstitution", "EmployersOrganisation", "GeopoliticalOrganisation",\
    "GovernmentAgency", "InternationalOrganisation", "Legislature", "Non-ProfitOrganisation",\
    "PoliticalParty", "ReligiousOrganisation", "TermOfOffice", "TradeUnion", "Artist", \
    "Athlete", "BusinessPerson", "Criminal", "Economist", "Engineer", "Journalist", "Judge",\
    "Lawyer", "OfficeHolder", "Politician", "Scientist", "Writer", \
    "Meeting", "AcademicConference", "Convention", "Software", "product", "Country", "Person"}

DBPEDIA_TYPES_2 = {"Currency", "Company", "GovernmentAgency", "Person", "Country", "product", "Software"}
