import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.DARKLY] #dbc theme

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, #init the app
                suppress_callback_exceptions=True)
