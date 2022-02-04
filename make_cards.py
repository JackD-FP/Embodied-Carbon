from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
import plotly.express as px
import dash_bootstrap_components as dbc

import graph_components as gc

import pandas as pd
import numpy as np

def first_card():
    first_card = dbc.Card(
        dbc.CardBody(
            [
                html.H3("Build Parameters", className="card-title"),
                html.Div([
                    html.P("GFA (metres sqr)", className='mb-1'),
                    dcc.Input(id = 'gfa', type = 'number', className='border rounded-3 mb-1', required=True),
                    html.H3(id='embodied_carbon')
                ], className='my-3'),
            ],
            className='mx-3 my-3'
        ),
        className='shadow'
    )
    return first_card

def second_card():
    second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Building Analytics'),
            dbc.Tabs(
                id = "tab_ID",
                active_tab = 'pie_graph_tab',
                children = [
                    dbc.Tab(label='GWP Statistics', tab_id= 'pie_graph_tab'),
                    dbc.Tab(label='Edit Material', tab_id = 'bar_graph_tab'),
                ]
            ),
            html.Div(id='tab_content')
        ],
        className='mx-3 my-3'
    ),
    className='shadow'
    )
    return second_card

    