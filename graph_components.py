
from click import style
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
                    {'label': 'GWP  per Material', 'value':'1'},
                    {'label': 'GWP per Floor', 'value':'2'},
                    {'label': 'Material GWP per Floor', 'value':'3'}
                ],
                value='1',
                className='my-5',
                size='large'
            ),
        ]),
        html.Div(id ='select_pie_div', children = [], className='mt-3'),
    ]
    return children

def select_pie(value, data, data_sum):
    df = pd.read_json(data)

    mat_list_sum = [] 
    floor_list_sum = []
    floor_percent = []
    opt_list = []

    mat_list = df['Materials Property'].drop_duplicates().tolist()
    floor_list = df['Home Story Name'].drop_duplicates().tolist()

    for i in range(len(mat_list)):
        mat = sum(df.loc[mat_list[i] == df['Materials Property'], 'gwp calc'])
        mat_list_sum.append(np.around(mat,3)) #list of gwp per material
        opt_list.append({"label": mat_list[i], "value": mat_list[i]})

    for i in range(len(floor_list)):
        floors = sum(df.loc[floor_list[i] == df['Home Story Name'], 'gwp calc'])
        floor_list_sum.append(np.around(floors,3))  #list of gwp per floor
        floor_percent.append(np.around((floor_list_sum[i]/data_sum)*100, 3))    #list of % per floor


    if value == '1':  
        d = {'materials': mat_list, 'gwp value':mat_list_sum}
        df_mat= pd.DataFrame(data = d)
        df_mat = df_mat.sort_values(by=['materials'])
        pie = px.pie(
            data_frame=df_mat, 
            values='gwp value', 
            names='materials',
            title='GWP Material Composition (%)')
        pie.update_layout(legend_traceorder='normal')
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
        d = {'Floor Level': floor_list, 'Percentage': floor_percent,'GWP Value': floor_list_sum}
        df_floor = pd.DataFrame(data=d)
        df_floor= df_floor.sort_values(by=['Floor Level'])
        
        pie = px.pie(
            data_frame=df_floor, 
            values='GWP Value', 
            names='Floor Level',
            title='GWP per Floor (%)', 
            labels={'Floor Level'}
            )
        pie.update_traces(textposition='inside')
        pie.update_layout(legend_traceorder='normal')

        return html.Div(
            [
                dash_table.DataTable(
                    data=df_floor.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_floor.columns],
                    page_size=10,
                    style_data={
                        'whiteSpace': 'normal',
                        'width': 'auto',
                        'backgroundColor': '#525252'               
                    },
                    style_header={'background': '#262626' },
                ),
                dcc.Graph(figure=pie ,style={'height': '50vh'}),
            ]
        )

    elif value == '3':

        return html.Div(
            [  
                html.H5('Material'),
                dbc.Select( 
                    id='material_selection',
                    options = opt_list,
                    placeholder='Choose Material',
                    style={
                        'width':'25%'
                    }
                ),
                html.Div(id='material_per_floor_div'), #div for callback to output graph depending on selection
            ]
        )


def material_select_(value, data):
    df = pd.read_json(data)
    mat_list = df['Materials Property'].drop_duplicates().tolist()

    for i in range(len(mat_list)):
        if value == mat_list[i]:
            _gwp = []
            #_gwp = df.loc[mat_list[i] == df['Materials Property'], 'gwp calc']
            _lvl = df.loc[mat_list[i] == df['Materials Property'], 'Home Story Name'].drop_duplicates().tolist()

            for j in range(len(_lvl)):
                _gwp_consolidate = sum(df.loc[_lvl[j] == df['Home Story Name'], 'gwp calc'].tolist())
                _gwp.append(np.around(_gwp_consolidate, 3))
        
            mat = {'story':_lvl, 'gwp':_gwp}
            mat_pd = pd.DataFrame(data=mat)

            pie = px.pie(
                data_frame=mat_pd,
                values='gwp',
                names='story' 
            )
            #pie.update_traces(textposition='inside')

            return html.Div(
                [
                    dash_table.DataTable(
                    data=mat_pd.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in mat_pd.columns],
                    page_size=10,
                    style_data={
                        'whiteSpace': 'normal',
                        'width': 'auto',
                        'backgroundColor': '#525252'               
                    },
                    style_header={'background': '#262626' },
                ),
                    html.P('{}'.format(value)),
                    dcc.Graph(figure=px.pie(
                        data_frame=mat_pd,
                        values='gwp',
                        names='story' 
                        ),style={'height': '50vh'})
                ]
            )