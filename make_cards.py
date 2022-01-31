import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

import graph_components as gc

def first_cards():
    first_card = dbc.Card(
        dbc.CardBody(
            [
                html.H3("Build Parameters", className="card-title"),
                html.Div([
                    html.P("Building Perimeter (meters)", className='mb-1'),
                    dcc.Input(id = 'perimeter', type = 'number', className='border rounded-3'),
                ], className='my-3'),
                html.Div([
                    html.P("Building Footprint (sq m)", className='mb-1'),
                    dcc.Input(id = 'footprint', type = 'number', className='border rounded-3'),
                ], className='my-3'),
                html.Div([
                    html.P("Floor to Floor Height (meters)", className='mb-1'),
                    dcc.Input(id = 'f2f', type = 'number', className='border rounded-3'),
                ], className='my-3'),
                html.Div([
                    html.P("Number of Floors", className='mb-1'),
                    dcc.Input(id = 'f2f', type = 'number', className='border rounded-3'),
                ], className='my-3'),
            ]
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
                active_tab = 'bar_graph_tab',
                children = [
                    dbc.Tab(label='Bar Graphs', tab_id = 'bar_graph_tab'),
                    dbc.Tab(label='Pie Graph', tab_id= 'pie_graph_tab'),
                ]
            ),
            html.Div(id='tab_content')
        ]
    ),
    className='shadow'
    )
    return second_card