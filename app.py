import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table 
from logger import *

import loader

MAPFIGID='map_figure_id'
KEYWORDDDID='keyword_dropdown_id'
ARTICLETID='article_table_id'
dbcol = loader.open_collection()
keywords=dbcol.distinct('keyword')
options = [{'label': x, 'value': x} for x in keywords]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def make_map_fig(kwlist=[]):

    countryndf = loader.get_country_freq(dbcol, kwlist)
    fig = px.scatter_geo(countryndf, locations="country", color="count",
                         hover_name="country", size="count",
                         projection="natural earth", 
                         locationmode= 'country names',)
    return fig


mapgraph=dcc.Graph(figure=make_map_fig(), id=MAPFIGID)
columns=[{"name": i, "id": i} for i in loader.COLUMNS_TO_SHOW]
articletable=dash_table.DataTable(id=ARTICLETID, columns=columns,
                                  fixed_rows={'headers': True},
                                          style_table={#'height': '30vh', 
                                                       'overflowY': 'auto', 
                                                       'overflowX': 'auto'},
                                          style_cell={
                                                 'overflow': 'hidden',
                                                 'textOverflow': 'ellipsis',
                                                 'maxWidth': 0
                                             },
                                          style_data={
                                              'whiteSpace': 'normal',
                                              'height': 'auto',
                                          },                                          
                                          style_cell_conditional=[
                                                  {'if': {'column_id': 'title'},
                                                   'width': '40%'},
                                                  {'if': {'column_id': 'pub_year'},
                                                   'width': '10%'},        
                                                  {'if': {'column_id': 'venue'},
                                                   'width': '20%'},     
                                                  {'if': {'column_id': 'author'},
                                                   'width': '30%'},                                                   
                                                  #['title', "author", 'journal', 'pub_year', 'venue']
                                              ],
                                          #row_selectable='single',                                  
                                  )

sepstyle={'margin-bottom': '0.2em', 'margin-top': '0.2em', 'thickness': '0px'}
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dbc.Row(
            dbc.Col(
                dbc.Card( html.H1("Dynamically rendered tab content", className = 'align-self-center'), ), 
                width=12),
            ),
        html.Hr(style=sepstyle),
        dbc.Row(
            dbc.Col(
                dbc.Card( 
                    dcc.Dropdown(options=options, multi=True, id=KEYWORDDDID)
                    ),
                width=12),
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
                    children=[articletable]
                    ),
                width=12),
        ),    

    ]
)

@app.callback(
    Output(component_id=MAPFIGID, component_property='figure'),
    Input(component_id=KEYWORDDDID, component_property='value')
)
def set_graph(keywords):

    #if not keywords or not len(keywords):
    #    raise PreventUpdate
    fig = make_map_fig(keywords)
    fig.update_layout(clickmode='event+select')
    return fig
    
@app.callback(
    Output(component_id=ARTICLETID, component_property='data'),
    Input(component_id=MAPFIGID, component_property='selectedData'),
    Input(component_id=MAPFIGID, component_property='figure'),
    State(component_id=KEYWORDDDID, component_property='value')
)
def load_articles(selected_countries, data, selected_keywords):
    #if not selected_countries or not selected_keywords:
    #    raise PreventUpdate
    if selected_countries:
        countries=[x['hovertext'] for x in selected_countries['points']]
    else:
        countries=[]
    if not selected_keywords:
        selected_keywords=[] 
    logging.debug("selected countries: {}, keywords: {}".format(countries, selected_keywords))
    results=loader.get_articles_countries_keywords(dbcol, countries, selected_keywords)
    return results 

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)