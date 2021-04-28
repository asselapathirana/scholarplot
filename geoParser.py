import argparse
import loader
import sys
from geotext import GeoText


def process_countries(collection, maxitems=sys.maxsize):
    nn=0
    for document in collection.find(): 
        abst=" "+document['abstract'] if 'abstract' in document else ''
        text=document['title']+abst
        gt=GeoText(text)
        #countries=[{'country': x} for x in gt.countries]
        print(gt.countries, document) # iterate the cursor
        qq={'_id': document['_id']}
        document["countries"]=gt.countries
        collection.update(qq, document)
        nn+=1
        if(nn>maxitems):
            break


def get_args():
    parser = argparse.ArgumentParser(description='Update the google scholar mongodb database by parsing countries')
    parser.add_argument('dbpassword', help="password for mongodb")
    parser.add_argument('--dburl', help="url for mongodb connection e.g. 'mongodb+srv://dbUser:{}@cluster0.ridyy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'")
    parser.add_argument('--apikey', '-k', help="Api key for Scraper API")
    parser.add_argument('--maxitems', '-n', help="Maximum articles to process", default=sys.maxsize, type=int)
    args=parser.parse_args()
    return args


if __name__=="__main__":
    vals=get_args()
    dbclient=loader.connectDB(password=vals.dbpassword)
    db=dbclient["articles"]
    dbcol=db["articlescollection"]
    process_countries(dbcol, maxitems=vals.maxitems)