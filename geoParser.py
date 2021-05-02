import argparse
import loader
import sys
from geotext import GeoText



def process_countries(collection, maxitems=sys.maxsize, method=loader._GEOTEXT):
    
    if method==loader._MORDECAI:
        import pycountry
        from mordecai import Geoparser
        mordecai_parser=Geoparser()
    nn=0
    for document in collection.find(): 
        abst=" "+document['abstract'] if 'abstract' in document else ''
        text=document['title']+abst
        if method==loader._GEOTEXT:
            gt=GeoText(text)
            gt=gt.countries
            document["countries"][loader._GEOTEXT]=gt
        elif method==loader._MORDECAI:
            pp=geo.geoparse(text)
            gt=[pycountry.countries.get(alpha_3=x['country_predicted']).name for x in pp]
            document["countries"][loader._MORDECAI]=gt
        qq={'_id': document['_id']}
        collection.update(qq, document)
        nn+=1
        if(nn>maxitems):
            break


def get_args():
    methods="Currently implemented: {}. Default: '{}'".format(list(loader.GEOPARSER.keys()), loader._GEOTEXT)
    parser = argparse.ArgumentParser(description='Update the google scholar mongodb database by parsing countries')
    parser.add_argument('dbpassword', help="password for mongodb")
    parser.add_argument('--dburl', help="url for mongodb connection e.g. 'mongodb+srv://dbUser:{}@cluster0.ridyy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'")
    parser.add_argument('--apikey', '-k', help="Api key for Scraper API")
    parser.add_argument('--maxitems', '-n', help="Maximum articles to process", default=sys.maxsize, type=int)
    parser.add_argument('--method', '-m', help="Geoparser to use.\n"+methods,
                        default=loader._GEOTEXT, type=str, )
    args=parser.parse_args()
    return args


if __name__=="__main__":
    vals=get_args()
    dbclient=loader.connectDB(password=vals.dbpassword)
    db=dbclient["articles"]
    dbcol=db["articlescollection"]
    process_countries(dbcol, maxitems=vals.maxitems, GEOPARSER[vals.method])