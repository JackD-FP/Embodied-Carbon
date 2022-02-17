import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
import plotly.express as px
import dash_bootstrap_components as dbc

from layout import layout
from server import app

app.layout = html.Div(layout)

if __name__ == '__main__':
    app.run_server(debug=True)
