import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import os
import pandas as pd
import dash_table 

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
articletable=dash_table.DataTable(id=ARTICLETID)

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
    return fig
    


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)