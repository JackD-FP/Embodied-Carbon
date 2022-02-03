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
                html.H3('under constructions')
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

def select_pie(value, data):
    df = pd.read_json(data)

    mat_list_sum = [] 
    opt_list = []

    mat_list = df['Materials Property'].drop_duplicates().tolist()

    for i in range(len(mat_list)):
        mat = sum(df.loc[mat_list[i] == df['Materials Property'], 'gwp calc'])
        mat_list_sum.append(np.around(mat,3)) #list of gwp per material
        opt_list.append({"label": mat_list[i], "value": mat_list[i]})

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
        return html.Div(
            [
                html.Div(id='gwp floor bar'),
                dbc.Switch(
                    id='log_switch',
                    label='Logarithmic Y-axis',
                    value=False,
                )
            ]
        )
        
    elif value == '3':
        return html.Div(
            [  
                html.H5('Material', ),
                dbc.Select( 
                    id='material_selection',
                    #value=opt_list[0], #this should work but the graphs don't load instantly
                    options = opt_list,
                    placeholder='Choose Material',
                    style={
                        'width':'25%'
                    },
                    className='my-3'
                ),
                html.Div(id='material_per_floor_div'), #div for callback to output graph depending on selection
            ]
        )

def gwp_floor_bar(value, data, data_sum):
    df = pd.read_json(data)

    floor_list_sum = []
    floor_percent = []

    floor_list = df['Home Story Name'].drop_duplicates().tolist()
    for i in range(len(floor_list)):
        floors = sum(df.loc[floor_list[i] == df['Home Story Name'], 'gwp calc'])
        floor_list_sum.append(np.around(floors,3))  #list of gwp per floor
        floor_percent.append(np.around((floor_list_sum[i]/data_sum)*100, 1))    #list of % per floo

    d = {'Floor Level': floor_list, 'Percentage': floor_percent,'GWP Value': floor_list_sum}
    df_floor = pd.DataFrame(data=d)
    bar = px.bar(
        data_frame=df_floor, 
        x='Floor Level', 
        y='GWP Value', 
        log_y=value,
        title='GWP per Floor (%)',
        labels={
            'GWP Value': 'GWP Value in Log'
        }
    ) 
    return [
        dash_table.DataTable(
            data=df_floor.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_floor.columns],
            page_size=10,
            style_data={
                'whiteSpace': 'normal',
                'width': 'auto',
                'backgroundColor': '#525252'               
            },
            style_header={'background': '#262626'},
        ),
        dcc.Graph(figure=bar, style={'height': '50vh'},className='my-3', id='log_bar'),
    ]
    

def material_select_(value, data):
    df = pd.read_json(data)

    mat_list = df['Materials Property'].drop_duplicates().tolist()

    #creates a consolidated floors names in a given value
    _gwp_list = []
    _lvl_drop = df.loc[value == df['Materials Property'], 'Home Story Name'].drop_duplicates().tolist()

    #create special dataframe just for value
    _lvl = df.loc[value == df['Materials Property'], 'Home Story Name'].tolist()
    _gwp = df.loc[value == df['Materials Property'], 'gwp calc'].tolist()
    _df = pd.DataFrame({'floor': _lvl, 'gwp': _gwp})

    for j in range(len(_lvl_drop)): #consolidates all the gwp per floor per mat_list[i]
        _gwp_consolidate = sum(_df.loc[_lvl_drop[j] == _df['floor'], 'gwp'].tolist())
        _gwp_list.append(np.around(_gwp_consolidate, 3))

    _df_consolidate = pd.DataFrame({'floor': _lvl_drop, 'gwp': _gwp_list})
    for i in range(len(mat_list)):
        if value == mat_list[i]:
            bar = px.bar(
                data_frame=_df_consolidate,
                x='floor',
                y='gwp',
                title='GWP of {} per floor'.format(mat_list[i])
            )

            children =  html.Div(
                [
                    dash_table.DataTable(
                    data=_df_consolidate.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in _df_consolidate.columns],
                    page_size=10,
                    style_data={
                        'whiteSpace': 'normal',
                        'width': 'auto',
                        'backgroundColor': '#525252'               
                    },
                    style_header={'background': '#262626'},
                ),
                    dcc.Graph(figure=bar, style={'height': '50vh'},className='mt-3'),
                    html.Div(id='bar comparison', className='my=3'),
                    dbc.Switch(
                        id='mat_log_switch', 
                        label='Logarthmic Y-Axis', 
                        value=False),
                ])
            return children

def log_material_select(value, data):
    df = pd.read_json(data)

    df_new = df.filter(items=['Home Story Name', 'Materials Property', 'gwp calc'])
    df_new = df_new.rename(columns={'Home Story Name':'floors', 'Materials Property': 'materials', 'gwp calc': 'gwp'})

    bar_comparison = px.bar(df_new, x='floors', y='gwp', log_y=value ,color='materials', title='GWP Comparison Between Material and Floor')
    return dcc.Graph(figure=bar_comparison, style={'height': '50vh'})