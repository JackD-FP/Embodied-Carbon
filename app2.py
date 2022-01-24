import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import io
from io import StringIO
import base64

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

from dash.dependencies import Output, Input, State, ALL, ALLSMALLER, MATCH
from dash.exceptions import PreventUpdate

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Number of students per education level", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
)

app.run_server(debug=True, dev_tools_ui = True, port=3000)
