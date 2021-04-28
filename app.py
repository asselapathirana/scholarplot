import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import os

import loader

dbclient=loader.connectDB(os.environ.get('DBPASSWD'), user=os.environ.get('DBUSER'))
db=dbclient["articles"]
dbcol=db["articlescollection"]
keywords=dbcol.distinct('keyword')
options = [{'label': x, 'value': x} for x in keywords]
print(options)
print(os.environ.get('DBUSER'), os.environ.get('DBPASSWD'))

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dbc.Row(
            dbc.Col(
                dbc.Card( html.H1("Dynamically rendered tab content", className = 'align-self-center'), ), 
                width=12),
            ),
        html.Hr(style={'margin-bottom': '0.5em', 'margin-top': '0.5em'}),
        dbc.Row(
            dbc.Col(
                dbc.Card( 
                    dcc.Dropdown(options=options, multi=True)
                    ),
                width=12),
        ),

    ]
)


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)