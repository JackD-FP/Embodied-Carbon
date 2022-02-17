import io
import base64
import datetime

from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
from server import app
import pandas as pd
# import numpy as np

import layout
#------------------------------------------------------------------------
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    df = df.rename(columns=df.iloc[0], )
    df2 = df.drop([0,0])


    
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        dash_table.DataTable(
            data=df2.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df2.columns],
            page_size=15,
            style_data={
                'whiteSpace': 'normal',
                'width': 'auto',
                'backgroundColor': '#525252'               
            },
            style_header={'background': '#262626', 'color':"#fafafa" },
            id='df2 tbl',
            editable=True,
        ),
    ],
    className='mx-5')

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children