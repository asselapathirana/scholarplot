from scholarly import scholarly, ProxyGenerator
import argparse
from pymongo import MongoClient
import pandas as pd
import os

from logger import *

pg = ProxyGenerator() # this need to be global it seems. 
COLUMNS_TO_SHOW=['title', "author",  'pub_year', 'venue']
ALLCOUNTRIES=['All Countries']

def open_collection():
    dbclient=connectDB(os.environ.get('DBPASSWD'), user=os.environ.get('DBUSER'))
    db=dbclient["articles"]
    dbcol=db["articlescollection"]
    return dbcol

def get_country_freq(dbcol, kwlist):
    if kwlist and len(kwlist):
        kwmatch=[{'keyword': x} for x in kwlist]
        countryct=dbcol.aggregate(
            [
        { '$match': {'$or': kwmatch} },
        {'$unwind':"$countries"},
        {'$group':{"_id":"$countries","count":{'$sum':1}}},
        {'$group':{"_id":'null',"country_details":{'$push':{"countries":"$_id",
                                                       "count":"$count"}}}},
        {'$project':{"_id":0,"country_details":1}}
        ]).next()
        countryndf=pd.DataFrame([[x['countries'], x['count']] for x in countryct['country_details']], columns=['country', 'count'])
        return countryndf
    else:
        df=pd.DataFrame([['',0],['', 0]], columns=['country', 'count'])
        return df
    
    
def get_articles_countries_keywords(dbcol, countries, keywords):
    if countries==ALLCOUNTRIES:
        query={ "keyword": {'$in'   :keywords}}
    else:
        query={ '$and':[{ "countries": {'$in':countries,},},
                    { "keyword": {'$in'   :keywords ,},},
                    ]}
    columns=COLUMNS_TO_SHOW
    cols={col:1 for col in columns}
    result=list(dbcol.find(query,cols))
    result=[{k: v for k, v in d.items() if k != '_id'} for d in result]
    logging.debug("query results: {}".format(str(result)))
    return result

def connect(API_KEY=None):
    if API_KEY and len(API_KEY)>10:
        print("Using key starting with {}".format(API_KEY[0:5]))
        
        #pg._use_proxy(http="http://scraperapi:{}@proxy-server.scraperapi.com:8001".format(API_KEY))
        pg.ScraperAPI(API_KEY)
        scholarly.use_proxy(pg)
    scholarly.set_timeout(60)   
    return scholarly
def get_args():
    parser = argparse.ArgumentParser(description='Download google scholar hits for a keyword and save in a database')
    parser.add_argument('Keyword', help="Keyword provide quotes for multiple words")
    parser.add_argument('dbpassword', help="password for mongodb")
    parser.add_argument('--dburl', help="url for mongodb connection e.g. 'mongodb+srv://dbUser:{}@cluster0.ridyy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'")
    parser.add_argument('--apikey', '-k', help="Api key for Scraper API")
    parser.add_argument('--maxitems', '-n', help="Maximum articles to process", default=10)
    args=parser.parse_args()
    return args

def query(connection, keyword, maxtries=5):
    for nn in range(maxtries):
        try:
            search_query = connection.search_pubs(keyword)
            print("Worked in n={} attempt.".format(nn))
            return search_query
        except Exception as ex:
            print("Failed n={} ({})".format(nn, ex))
    return None

def process(res, dbcol, keyword, maxitmes=10, maxtries=5):
    for nn in range(maxitmes):
        for kk in range(maxtries):
            try:
                art=scholarly.fill(next(res))
                #print("Worked in n={} attempt.".format(kk))
                break
            except Exception as ex:
                print("Failed n={} ({})".format(kk, ex))

        print("Article no={} in n={} attempt.".format(nn, kk))
        bib=art['bib']
        bib['keyword']=keyword
        for kk in range(maxtries):
            try:
                results=dbcol.insert_one(bib)
                print('Created {}'.format(results.inserted_id))
                break
            except Exception as ex:
                print("DB connection attempt n={} failed {}, ...".format(kk, ex))
          
        

def connectDB(password, user='dbUser', url="mongodb+srv://{}:{}@cluster0.ridyy.mongodb.net/articles?retryWrites=true&w=majority"):
    client = MongoClient(url.format(user, password))
    return client

  

if __name__=="__main__":
    vals=get_args()
    print("getting connection ... ")
    con=connect(API_KEY=vals.apikey)
    print("getting db connection  ... ")
    dbclient=connectDB(password=vals.dbpassword)
    db=dbclient["articles"]
    dbcol=db["articlescollection"]
    if not con:
        print("Did not work!")
    else:
        print("query starting  ... ")
        qu=query(con,vals.Keyword)
        print("processing start  ... ")
        process(qu, dbcol, vals.Keyword, maxitmes=500)
        print(vals)
    

    
 