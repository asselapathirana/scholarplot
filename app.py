from flask import Flask
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table 
import urllib
from logger import *
from instructions import _instructions

import loader


MAPFIGID='map_figure_id' 
KEYWORDDDID='keyword_dropdown_id'
ENGINEDDID='engine_dropdown_id'
ARTICLELISTCARD='article_table_id'
dbcol = loader.open_collection()
keywords=dbcol.distinct('keyword')
_eng=list(dbcol.find_one()['countries2'].keys())
engines=[{'label': x, 'value': x} for x in _eng]
DEFAULTENGINE=engines[0]['value']

options = [{'label': x, 'value': x} for x in keywords]

server = Flask(__name__) # needed for dokku deploy with gunicorn 
app = dash.Dash(__name__,server=server, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                                              'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'])

def make_map_fig(kwlist=[], engine=DEFAULTENGINE):

    countryndf = loader.get_country_freq(dbcol, kwlist, engine)
    fig = px.scatter_geo(countryndf, locations="country", color="count",
                         hover_name="country", size="count",
                         projection="natural earth", 
                         locationmode= 'country names',)
    return fig


mapgraph=dcc.Graph(figure=make_map_fig(), id=MAPFIGID)
columns=[{"name": i, "id": i} for i in loader.COLUMNS_TO_SHOW]

sepstyle={'marginBottom': '0.2em', 'marginTop': '0.2em', 'thickness': '0px'}

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dbc.Row(
            dbc.Col(
                dbc.Card( html.H1("Geolocating Academic Publications", className = 'align-self-center'), ), 
                width=12),
            ),
        dbc.Row(
            dbc.Col(
            dbc.Alert(_instructions, dismissable=True, fade=True, 
                                  is_open=True, color="light")    
            )
        ),
        html.Hr(style=sepstyle),
        dbc.Row(
            [dbc.Col(
                    dbc.Card( 
                        dcc.Dropdown(options=engines, multi=False, id=ENGINEDDID, value=DEFAULTENGINE)
                        ),
                    width=2),                
                dbc.Col(dbc.Card( 
                    dcc.Dropdown(options=options, multi=True, id=KEYWORDDDID)
                    ),
                width=10),

            ]         
        ),
        html.Hr(style=sepstyle),
        dbc.Row(
            dbc.Col(
                dbc.Card( 
                    children=[mapgraph]
                    ),
                width=12),
        ), 
        html.Hr(style=sepstyle),
        dbc.Row(
            dbc.Col(
                dbc.Card( 
                    id=ARTICLELISTCARD,
                    children=[]
                    ),
                width=12),
        ),    

    ]
)

@app.callback(
    Output(component_id=MAPFIGID, component_property='figure'),
    [Input(component_id=KEYWORDDDID, component_property='value'),
     Input(component_id=ENGINEDDID, component_property='value'),
     ],
)
def set_graph(keywords, engine):

    #if not keywords or not len(keywords):
    #    raise PreventUpdate
    fig = make_map_fig(keywords, engine)
    fig.update_layout(clickmode='event+select')
    return fig
    
@app.callback(
    [Output(component_id=ARTICLELISTCARD, component_property='children')],
    [Input(component_id=MAPFIGID, component_property='selectedData'),
    Input(component_id=KEYWORDDDID, component_property='value'),
    Input(component_id=ENGINEDDID, component_property='value'),
    ]
)
def load_articles(selected_countries, selected_keywords, engine):
    #if not selected_countries or not selected_keywords:
    #    raise PreventUpdate
    if selected_countries:
        countries=[x['hovertext'] for x in selected_countries['points']]
    else:
        countries=loader.ALLCOUNTRIES
        
    ctx = dash.callback_context
    if ctx.triggered:
        _id=ctx.triggered[0]['prop_id'].split('.')[0]
        if _id == KEYWORDDDID:
            countries=loader.ALLCOUNTRIES
        
    if not selected_keywords:
        selected_keywords=[] 
    logging.debug("selected countries: {}, keywords: {}".format(countries, selected_keywords))
    results=loader.get_articles_countries_keywords(dbcol, countries, selected_keywords, engine)
    components=[]
    head="Articles on [{}] in [{}]".format(str(selected_keywords)[1:-1], str(countries)[1:-1])
    components.append(dbc.Card(html.H3(head)))
    for art in results:
        href='https://scholar.google.com/scholar?q='+urllib.parse.quote_plus(art['author']+"; "+art["title"]+"; "+art["venue"]+"; "+art['pub_year']) 
        text=" "+art['author']+'; '+art['title']+'; '+art['venue']+'; '+ art['pub_year']
        link=html.A(html.I(className="fa fa-external-link", **{'aria-hidden': 'true'}, children=None), target='_blank', href=href)
        components.append(html.Li(dbc.Card(html.Span([link, text]))))
    _components=html.Ol( children=components)
    return [_components] 

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)