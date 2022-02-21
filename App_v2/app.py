import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from layout import layout
from server import app

#load basic material and do some shit about material name.
df_db = pd.read_csv("Basic Material v3.csv")
df_db['material'] = df_db['material name'].str.cat(df_db['material variant name'], sep = ' ')
df_db['material'] = df_db['material'].str.cat(df_db['locations'], sep =" - ")

app.layout = html.Div(layout)

if __name__ == '__main__':
    app.run_server(debug=True)
