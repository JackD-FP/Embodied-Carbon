import base64
import datetime
import io



import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import graph_components as gc
import make_cards as mc

#import database of materials property df_db
#READ CSV DATABASE
df_db = pd.read_csv("Basic Material v3.csv")

#COMBINE TO CREATE MATERIAL NAME
df_db['material'] = df_db['material name'].str.cat(df_db['material variant name'], sep = ' ')
df_db['material'] = df_db['material'].str.cat(df_db['locations'], sep =" - ")

external_stylesheets = [dbc.themes.DARKLY] #dbc theme

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, #init the app
                suppress_callback_exceptions=True)

app.layout = html.Div([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ], className='shadow'),
        style={
            'width': '50%',
            'lineHeight': '60px',
            'textAlign': 'center',
            'margin': 'auto',
            'marginTop': '2rem',
        },
        className = 'text-center mb-5 border border-1 rounded-3',
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-datatable', className='mb-5'),
    html.Div(id='output-div'),
    html.Div(id='section_2'),
    html.Hr(className='mt-5'),  # horizontal line
    html.Div('Brought to you by Jack Jack', className='my-5'),

], className='px-5')


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

    df['description'] = df['Home Story Name'].str.cat(df['Element Type'].apply(str), sep =" | ")
    df['description'] = df['description'].str.cat(df['Cross Section Height at Bottom/Start (cut)'].apply(str), sep =" | ")
    df['description'] = df['description'].str.cat(df['Cross Section Width at Bottom/Start (cut)'].apply(str), sep =" x ")
    df['description'] = df['description'].str.cat(df['Thickness'].apply(str), sep =" x ")
    df = df.sort_values(by=['description'])
    df = df.replace('---', 0)
    
    gwp_list = []
    for i in range(len(df)):
        unit = df_db.loc[df_db['material'] == df['Materials Property'][i], 'units'].values[0]
        gwp = df_db.loc[df_db['material'] == df['Materials Property'][i], 'GWP'].values[0]
        density = df_db.loc[df_db['material'] == df['Materials Property'][i], 'density'].values[0]
        
        if unit == 'm3': #volume gwp calculation
            gwp_solution = gwp * pd.to_numeric(df['Net Volume'][i], downcast='float')
            gwp_list.append(np.around(gwp_solution, 4))
        elif unit == 'm2': #Area gwp calculation
            gwp_solution = gwp * df['Area'][i]
            gwp_list.append(np.around(gwp_solution, 4))  
        elif unit == 'lm': #Area gwp calculation
            gwp_solution = gwp * df['3D Length'][i]
            gwp_list.append(np.around(gwp_solution, 4))
        elif unit == 'T': #Tonnes gwp calculation
            gwp_solution = gwp * pd.to_numeric(df['Net Volume'][i], downcast='float') * pd.to_numeric(density, downcast='float')
            gwp_list.append(np.around(gwp_solution, 4))
        elif unit == 'kg': #kg gwp calculation
            gwp_solution = gwp * pd.to_numeric(df['Net Volume'][i], downcast='float') * pd.to_numeric(density, downcast='float')  #MAY NEED TO CONVERT TO TONNES DOUBLE CHECK UNITS
            gwp_list.append(np.around(gwp_solution, 4))
    
    df_gwp = pd.DataFrame(gwp_list, columns=['gwp calc'])
    df2 = pd.concat([df['description'], df['Materials Property'],df['3D Length'], df['Area'], df['Net Volume']], axis = 1)
    df2 = df2.join(df_gwp['gwp calc'])#for tabulation
    df = df.join(df_gwp['gwp calc'])#for storage to get data later
    gwp_sum = np.around(sum(df2['gwp calc']), 3) #sum of all gwp values

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
            style_header={'background': '#262626' }

        ),
        html.H3('Total embodied carbon is {:,} TCO2e.'.format(gwp_sum/1000)),
        dcc.Store(id='stored_data', data=df.to_json()),
        dcc.Store(id = 'stored_sum', data = gwp_sum),

    ],
    className='')

# def update_table_edit_tabs(active_tab):
#     if active_tab == 'table_tab':
#         return 

@app.callback(
    Output('output-datatable', 'children'),
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


@app.callback(
    Output('output-div', 'children'),
    Input('stored_sum','data'),
)
def make_cards(n):
    if n is None:
        return dash.no_update
    else:

        children = dbc.Row(
            [
                dbc.Col(mc.first_card(), width = 4),
                dbc.Col(mc.second_card(), width = 8)
            ]
    )
    return children


@app.callback(
    Output('embodied_carbon', 'children'),
    Input('gfa', 'value'),
    State('stored_sum', 'data')
)
def benchmark(value, store_sum):
    if value is None:
        return dash.no_update
    else:
        benchmark = store_sum/value
        children = html.Div([
            html.H5('Building Benchmark is {} CO2e per sqm'.format(np.around(benchmark, 3)))
        ])
    return children


@app.callback( #WE NEED TO CHANGE THIS TO A CLIENT SIDE CALL BACK! NID MUCH FEST MUST SPID MUCH ZOOMIES
    Output('tab_content', 'children'),
    Input('tab_ID', 'active_tab'),
)
def tab_render(tab):
    if tab == 'pie_graph_tab':            
        return gc.gwp_pie()
    elif tab == 'bar_graph_tab':            
        return gc.gwp_bar()

@app.callback( #I CHANGED THISSSSS 
    Output('select_pie_div', 'children'),
    Input('pie_select', 'value'),
    State('stored_data', 'data'),
    State('stored_sum', 'data')
)
def select_div(value, data, data_sum):
    return gc.select_pie(value, data, data_sum)

@app.callback(
    Output('material_per_floor_div', 'children'),
    Input('material_selection', 'value'),
    State('stored_data', 'data')
)
def material_select(value, data):
    return gc.material_select_(value, data)


if __name__ == '__main__':
    app.run_server(debug=True)
