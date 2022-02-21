import io
import base64
import datetime

from server import app

from dash import html, dash_table, dash, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

import layout

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

    # df2.loc[df2['Building Materials (All)'].str.contains('concrete',case=False,regex=True), "concrete"] = 'Concrete Generic OPC'
    # df2.loc[df2['Building Materials (All)'].str.contains('steel',case=False,regex=True), "steel"] = 'Steel Generic Section'
    # df2.loc[df2['Building Materials (All)'].str.contains('timber',case=False,regex=True), "timber"] = 'Structural Timber'
    # df2.loc[df2['Building Materials (All)'].str.contains('glass',case=False,regex=True), "glass"] = 'Glass'
    # df2.loc[df2['Building Materials (All)'].str.contains('plasterboard',case=False,regex=True), "plasterboard"] = 'plasterboard'

    
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
        dcc.Store(id='stored_data', data=df2.to_json()),
        html.Div(id='analytics')
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




@app.callback(
    Output('analytics', 'children'),
    Input('stored_data', 'data')
)
def analytic_cards(data): #this callback is pretty slow... make fast (╯‵□′)╯︵┻━┻
    if data is None:
        return dash.no_update
    else: 
        df = pd.read_json(data)
        total_ec = sum(df['Embodied Carbon'].tolist())

        #i feel like there a better way of doing this (ㆆ_ㆆ)
        #recomposing a new dataframe seem to be the best way to approach it
        #need a better way.
        mat_list_sum = [] 
        opt_list = []
        mat_list = df['Building Materials (All)'].drop_duplicates().tolist()
        for i in range(len(mat_list)):
            mat = sum(df.loc[mat_list[i] == df['Building Materials (All)'], 'Embodied Carbon'])
            mat_list_sum.append(np.around(mat,3)) 
            opt_list.append({"label": mat_list[i], "value": mat_list[i]})

        d = {'materials': mat_list, 'gwp value':mat_list_sum}
        df_mat= pd.DataFrame(data = d)
        df_mat = df_mat.sort_values(by=['materials'])

        pie = px.pie(
            data_frame=df_mat, 
            values='gwp value', 
            names='materials',
            title='Total Embodied Energy (%)')
        pie.update_layout(legend_traceorder='normal')
        
        #-----------
        floor_list_sum = []
        floor_percent = []

        floor_list = df['Home Story Name'].drop_duplicates().tolist()
        for i in range(len(floor_list)): #i feel like there a better way of doing this ¯\_(ツ)_/¯
            floors = sum(df.loc[floor_list[i] == df['Home Story Name'], 'Embodied Carbon'])
            floor_list_sum.append(np.around(floors,3))  
            floor_percent.append(np.around((floor_list_sum[i]/total_ec)*100, 1))  

        d = {'Floor Level': floor_list, 'Percentage': floor_percent,'GWP Value': floor_list_sum}
        df_floor = pd.DataFrame(data=d)
        bar = px.bar(
            data_frame=df_floor, 
            x='Floor Level', 
            y='GWP Value', 
            #log_y=value,
            title='GWP per Floor (%)',
            labels={
                'GWP Value': 'GWP Value in Log'
            },
        )         

        tab_3_contents = html.Div(
            [  
                html.H3('Select Material to Analyse'),
                dbc.Select( 
                    id='material_selection',
                    options = opt_list,
                    placeholder='Choose Material',
                    className='my-3 m-25'
                ),
                html.Div(id='material_per_floor_div'), #div for callback to output graph depending on selection
            ]
        )


        return html.Div([
            dbc.Card(
                dbc.CardBody([
                    html.H2('Building Analytics'),
                    html.H5('Total Embodied Carbon is {} Tco2e'.format(np.around(total_ec/1000))),
                    dbc.Input(id='gfa_bmrk', placeholder="Please input gfa", type='number'),
                    html.Div(id='bmrk_result'),
                    dbc.Tabs([ 
                        dbc.Tab([
                            dcc.Graph(figure=pie,style={'height': '75vh'}, className='mt-3')
                        ], label="Tab 1"),
                        dbc.Tab([
                            dcc.Graph(figure=bar, style={'height': '75vh'},className='my-3', id='log_bar')
                        ], label="Tab 2"),
                        dbc.Tab(tab_3_contents, label="Tab 3"), 
                    ])
                ]),
            ),
        ])  

@app.callback(
    Output('bmrk_result', 'children'),
    Input('gfa_bmrk', 'value'),
    State('stored_data', 'data')
)
def benchmark(value, data):
    df = pd.read_json(data)
    df_super = df[df['Home Story Name'].str.contains('basement', regex=True)==True]
    #finish calculating superstructure 
    #then calcuulate the substructure 
    return html.Div([

    ])



@app.callback(
    Output('material_per_floor_div', 'children'),
    Input('material_selection', 'value'),
    State('stored_data', 'data')
)
def material_select(value, data):
    df = pd.read_json(data)

    mat_list = df['Building Materials (All)'].drop_duplicates().tolist()

    #creates a consolidated floors names in a given value
    _gwp_list = []
    _lvl_drop = df.loc[value == df['Building Materials (All)'], 'Home Story Name'].drop_duplicates().tolist()

    #create special dataframe just for value
    _lvl = df.loc[value == df['Building Materials (All)'], 'Home Story Name'].tolist()
    _gwp = df.loc[value == df['Building Materials (All)'], 'Embodied Carbon'].tolist()
    _df = pd.DataFrame({'floor': _lvl, 'Embodide Carbon (kgCO2e)': _gwp})

    for j in range(len(_lvl_drop)): #consolidates all the gwp per floor per mat_list[i]
        _gwp_consolidate = sum(_df.loc[_lvl_drop[j] == _df['floor'], 'Embodide Carbon (kgCO2e)'].tolist())
        _gwp_list.append(np.around(_gwp_consolidate, 3))

    
    _df = df.groupby(by=['Building Materials (All)', 'Home Story Name'], as_index=False).sum()
    _df = _df.filter(items=['Building Materials (All)', 'Home Story Name', 'Embodied Carbon'])   

    bar_comparison = px.bar(_df, 
        x='Home Story Name', 
        y='Embodied Carbon', 
        log_y=value,
        color='Building Materials (All)', 
        title='GWP Comparison Between Material and Floor')

    _df_consolidate = pd.DataFrame({'floor': _lvl_drop, 'Embodied Carbon': _gwp_list})
    for mat_list in mat_list:
        if value == mat_list:
            bar = px.bar(
                data_frame=_df_consolidate,
                x='floor',
                y='Embodied Carbon',
                title='Embodied Carbon of {} per floor'.format(mat_list)
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
                    dcc.Graph(figure=bar_comparison, style={'height': '50vh'},className='h-50 my-3'),

                    dbc.Switch(
                        id='mat_log_switch', 
                        label='Logarthmic Y-Axis', 
                        value=False),
                ])
            return children 


