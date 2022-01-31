
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import make_cards as mc

def gwp_bar():
    children = html.Div([
                html.H3('bar graph under constructions')
            ])
    return children

def gwp_pie():
    children = [
        html.Div([
            html.H3('pie graph under constructions')
        ])
    ]
    return children