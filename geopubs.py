from geotext import GeoText

from scholarly import scholarly, ProxyGenerator

pg = ProxyGenerator()
pg.ScraperAPI("aaf452b854ac109163a73a44d5217ad9")
scholarly.use_proxy(pg)
scholarly.set_timeout(60)

#search_query = scholarly.search_pubs('Assela Pathirana')
#res=scholarly.fill(next(search_query))
#print([pub['bib']['title'] for pub in res])
# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_pubs('Water management')
author = scholarly.fill(next(search_query))
# Print the titles of the author's publications
print([pub['bib']['title'] for pub in author['publications']])

# Take a closer look at the first publication
pub = scholarly.fill(author['publications'][0])
print(pub)


places = GeoText("London is a great city")
print(places.cities)
# "London"

# filter by country code
result = GeoText('I loved Rio de Janeiro and Havana', 'BR').cities
# 'Rio de Janeiro'
print(result)

rr=GeoText('New York, Texas, and also China').country_mentions
# OrderedDict([(u'US', 2), (u'CN', 1)])
print(rr)