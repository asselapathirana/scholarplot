import dash_core_components as dcc

text=dcc.Markdown("""

(After reading, click on the cross (right >) to get this message out of the way.)

# What is this and how it works
Using Natural Language Processing to 'Geoparsing' google scholar search results.  Select a keyword (or more) and see where the publications refer to.  Click on a bubble of a country to see its publications listed below the map. 
## Background
Python provides all the tools needed to do Natural Language Processing, including
*	Web scraping e.g. [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
*	Parsing and identifying entities e.g. [NLTK toolkit](https://www.nltk.org/)
*	Flag geographical locations mentioned in the text and geolocating them (Geoparsing) 
e.g. [Mordecai](https://github.com/openeventdata/mordecai), [CLAVIN](https://github.com/Novetta/CLAVIN), [geography3](https://pypi.org/project/geograpy3/) and 
 [geotext] (https://pypi.org/project/geotext/) (simple).  

## What it does
* Downloads Google Scholar search hits for each keyword (In this demo, I have limited each to 500 top hits, to keep things simple)
* Store them in a NoSQL database (MongoDB)
* Run geoparsers (geotext and mordecai in this case) to locate mentions of countries in the title or the abstract. 
* Feed the data to this app, so that the user can interactively look at them. 

## How to use
* (After closing these instructions) Select a keyword. The locations of the publications will be shown on the map. A list of all the publications will be shown below the map. 
* Change the geoparsing engine and see how it changes the results. 
* Click on the bubbles on the map to filter by country. Then the list will be updated to cover only that country. 
* It is possible to select more than one keyword (simply select from the dropdown list)
* It's also possible to select several countries. Either SHIFT+Click on the map or use the select tools (top-right). 
* Click on the link below each record to see it on google scholar. 

## What is missing
* Many publications concerning the United States of America, typically does not write the country name (e.g. A statewide assessment of mercury dynamics in North Carolina water bodies and fish). 
NLP tools are usually smart enough to detect these (North Carolina is in the USA so tag as 'USA'), but the current (demo) implementation misses some obscure names. 
* 'The United Kingdom vs. England' tagging is complicated. This issue has to be fixed (That's why no articles are tagged for England).

## Next step?
This demo provides a framework for Natural Language Processing of online material to make sense of information (e.g. geoparsing). 
It combines several Big-data constructs (Unstructured data, NoSQL (Jason) data lakes, NLP tricks). 
While a web app is not the right place to scale up these to the big-data level, the framework presented here can easily be implemented to do large-scale processing using a decent cluster computer system.

With large scale applications some of the possibilities are:

* Identify temporal trends in publications. 
* Locate 'hotspots' as well as locations with few (or no) studies (geographical gaps)

(After reading, click on the cross (top right) to get this message out of the way.)

""")


_instructions=text