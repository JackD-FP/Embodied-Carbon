
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

import make_cards as mc

def gwp_bar():
    children = html.Div([
                html.H3('bar graph under constructions')
            ])
    return children

def gwp_pie():
    children = [
        html.Div([
            dbc.Select(
                id='pie_select',
                options = [
                    {'label': 'GWP Material Composition', 'value':'1'},
                    {'label': 'GWP per Floor', 'value':'2'},
                    {'label': 'option 3', 'value':'3'}
                ],
                value='1',
                className='mt-5',
                size='large'
            ),
        ]),
        html.Div(id ='select_pie_div', children = [], className='mt-3'),
    ]
    return children

def select_pie(value, data):
    if value == '1':
        df = pd.read_json(data)
        mat_list = df['Materials Property'].drop_duplicates().tolist()
        mat_list_sum = [] #initiate list for append and sum

        for i in range(len(mat_list)):
            mat = sum(df.loc[mat_list[i] == df['Materials Property'], 'gwp calc'])
            mat_list_sum.append(np.around(mat,3))

        d = {'materials': mat_list, 'gwp value':mat_list_sum}
        df_mat= pd.DataFrame(data = d)
        df_mat = df_mat.sort_values(by=['materials'])
        pie = px.pie(data_frame=df_mat, values='gwp value', names='materials',title='GWP Material Composition (%)')

        return html.Div(
            [
                dash_table.DataTable(
                    data=df_mat.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_mat.columns],
                    page_size=15,
                    style_data={
                        'whiteSpace': 'normal',
                        'width': 'auto',
                        'backgroundColor': '#525252'               
                    },
                    style_header={'background': '#262626' },
                    

                ),
                dcc.Graph(figure=pie,style={'height': '50vh'}, className='mt-3')
            ]
        )
    elif value == '2':
        df = pd.read_json(data)
        floor_list = df['Home Story Name'].drop_duplicates().tolist()
        floor_list_sum = []
        
        for i in range(len(floor_list)):
            floors = sum(df.loc[floor_list[i] == df['Home Story Name'], 'gwp calc'])
            floor_list_sum.append(np.around(floors,3))

        d = {'floor level': floor_list, 'gwp value': floor_list_sum}
        df_floor = pd.DataFrame(data=d)
        pie = px.pie(data_frame=df_floor, values='gwp value', names='floor level',title='GWP per Floor (%)', labels={'Home Story Name'})
        pie.update_traces(textposition='inside')

        return html.Div(
            [
                dcc.Graph(figure=pie ,style={'height': '50vh'})
            ]
        )

    elif value == '3':
        return html.H3('Should be graph 3 but i ceeb to make it atm')