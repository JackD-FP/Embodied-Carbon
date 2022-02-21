
from server import app

from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import numpy as np

import layout
import callback_uploader

@app.callback(
    Output('analytics', 'children'),
    Input('stored_data', 'data')
)
def analytic_cards(data):
    if data is None:
        return dash.no_update
    else: 
        return html.Div([
            dbc.Card(
                dbc.CardBody(
                    html.H1('TEST')
                ),
            ),
        ])  
