from unicodedata import name

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import io
from io import StringIO
import base64

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

from dash.dependencies import Output, Input, State, ALL, ALLSMALLER, MATCH
from dash.exceptions import PreventUpdate

#------------------functions and shit-------------------------
#READ CSV DATABASE
df_db = pd.read_csv("Basic Material v3.csv")

#COMBINE TO CREATE MATERIAL NAME
df_db['material'] = df_db['material name'].str.cat(df_db['material variant name'], sep = ' ')
df_db['material'] = df_db['material'].str.cat(df_db['locations'], sep =" - ")

#create the label and value for the dropdown
label_dict = []
for i in range(len(df_db)):
    label_dict.append({'label': df_db['material'][i], 'value': df_db['GWP'][i]})

label_dict2 = []
for i in range(len(df_db)):
    label_dict2.append({'label': df_db['material'][i], 'value': df_db['material'][i]})

#------------------------APP INITIALISE----------------------------
external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

#-----------------------APP LAYOUT-----------------------------------
app.layout = html.Div(children = [
    html.H1(
        children = "Embodied Carbon Calculator",
        style = {'textAlign': 'center'}
    ),
    
    html.Div(
        children = "Calculate the buildings estimated embodied carbon.",
        style = {'textAlign': 'center'}
    ),
    html.Div(
        dcc.Upload(
            id = "upload-data",
            children = html.Div(['Drag and Drop or ',html.A('select Files')]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'marginTop': '1em',
                'marginLeft': 'auto',
                'marginRight': 'auto',
            },
            className = 'bg-primary',
            multiple = True
        ),
        style = {'textAlign': 'center'}
    ),
    
        html.Br(),
        #section 1
        html.Div(id='section_1', children = []),
        #section 2
        html.Div([
            html.Div(
                id='section_2', 
                style = {
                    'textAlign': 'center',
                    #'display': 'inline-block',
                    'width': '35%',
                    'margin': 'auto',
                    #'marginRight': '2rem'
                    }),

            #section 3
            html.Div(
                id='section_3', 
                style={
                    'textAlign':'center',
                    #'display': 'inline-block',
                    'margin': 'auto',
                    'paddingTop': '2rem',
                    'width': 'auto',
                    'height': '720px'
                }),
        ], 
        style = {
            'display': 'block',
            'alignItems': 'top',
        },
        id = 'Container12',),

        #footer-----------------------------------------
        html.Hr(),  # horizontal line

        html.Div('Brought to you by jack jack'),
    ],
        style={
            'paddingLeft': '8em',
            'paddingRight': '8em',
        }
    )

#----------------------------CallBack-------------------------
#callback for section 1
#upload data, and get it ready to calculate
@app.callback(Output('section_1', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename') )
def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n) for c, n in
                zip(list_of_contents, list_of_names)]
            return children

        elif list_of_contents is None:
            return 


#callback for section 2
#make the dropdown list base on number of UNIQUE building elements
@app.callback(Output('section_2', 'children'),
              Input('calcBtn', 'n_clicks'),
              State('data_store', 'data'))
def dropdownList(n_clicks, data):
    children = []
    if n_clicks is None:
        return dash.no_update
    else: 
        df = pd.read_json(data)
        # for i in range(len(df['description'].drop_duplicates())):
        for i in range(len(df['description'])):
            gwp_value = df_db.loc[df_db['material'] == str(df['Materials Property'][i]), 'GWP'].values[0]
            children.append(
                html.Div([
                    # html.P(df['description'].drop_duplicates().to_list()[i],
                    html.P(df['description'].to_list()[i],
                        id = {
                            'type': 'elementName',
                            'index': i
                        },
                        className= 'd-inline-block mb-0 me-4 lead'
                        
                        ),
                    #html.P('{}'.format(gwp_value)),
                    html.P('Embodied Carbon is: ',
                        className= 'd-inline-block me-2 mb-0'
                        ),
                    html.P(
                        id = {
                        'type': 'dynamic-label',
                        'index': i
                        },
                        className= 'd-inline-block mb-0'),
                    dcc.Dropdown(
                        options = label_dict,
                        value = gwp_value,
                        placeholder = 'Choose Material',
                        clearable = True,
                        style = {
                            'width': '100%', 
                            'color': '#171717'
                            },
                        id = {
                            'type': 'dpd',
                            'index': i
                        }
                    ),
                ], className= 'm-5 justify-content-start')
            )
    return children

def str2float(str):
    if str.find(",")!=-1:
        x= str.replace(',',"")
        return float(x)
    else: return float(str)

#calculation of the GWP
@app.callback(
    Output({'type': 'dynamic-label', 'index': MATCH}, 'children'),
    Input({'type': 'dpd', 'index': MATCH},'value'),
    State({'type': 'elementName', 'index': MATCH}, 'children'),
    State('data_store', 'data'),
    )
def dynamicLabel(gwpValue, elName, data):
    if gwpValue is None:
        return html.P(0)
    else:
        df = pd.read_json(data)
        unit = df_db.loc[df_db['GWP'] == gwpValue, 'units'].values[0]
        #unit = df_db.loc[df_db['GWP'] == gwpValue, 'units']
        if unit == 'm3': #volume calc
           elGwp = gwpValue * sum(df.loc[df['description'] == elName, 'Net Volume'])

        elif unit == 'm2': #area calc
            elGwp = gwpValue * sum(pd.to_numeric(df.loc[df['description'] == elName, 'Area'], downcast='float'))

        elif unit == 'Lm': #area calc
           elGwp = gwpValue * sum(pd.to_numeric(df.loc[df['description'] == elName, '3D Length'].values[0]))

        elif unit == 'kg': #Kg calc
            elGwp = sum(df.loc[df['description'] == elName, 'Net Volume']) * df_db.loc[df_db['GWP'] == gwpValue, 'density'].values[0]

        elif unit == 'T': #T calc
            #elGwp = sum(df.loc[df['description'] == elName, 'Net Volume']) * df_db.loc[df_db['GWP'] == gwpValue, 'density'].values[0] * 1000
            elGwp = sum(df.loc[df['description'] == elName, 'Net Volume']) * df_db.loc[df_db['GWP'] == gwpValue, 'density'].values[0]
        return np.around(elGwp, 4)

#callback for Section 3
@app.callback(Output('section_3', 'children'),
    [Input('calcBtn', 'n_clicks'),
    Input({'type':'dynamic-label', 'index': ALL}, component_property = 'children')],
    State({'type': 'elementName', 'index': ALL}, 'children'),
    #Input({'type': 'dpd', 'index': ALL},'value'),
    State('data_store', 'data'),
    )
def totGwp(btn, value, names, data):
    if btn != 0:
        return PreventUpdate
    try:
        sumVal = sum(value)
        #df = pd.DataFrame(value)
        #df2 = pd.DataFrame(data)
        #df = df.append(df2['description'])
        #df3 = df.insert(1, 'Names', df2['description'])
        #TotGwpPie= px.pie(df, values = value, names = names, hover_name = names) #<==== ADD NAME TO THE GRAPH
        #total_bar = px.line(df)
        children = [
            html.H3('Total Embodied Carbon is: {} CO2e'.format(np.around(sumVal, 3))), 
           # dcc.Graph(figure = TotGwpPie, )
            ]
    except:
        children = [html.H3('Please Fill in all Dropdown')]

    return children
    
#------------------functions for parse-------------------------
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    #df2 = df.drop(columns = ['id'])
        #sorts out description column----------------
    height = df.insert(1,"height", df['Cross Section Height at Bottom/Start (cut)'].replace('---',0))
    width = df.insert(1,"width", df['Cross Section Width at Bottom/Start (cut)'].replace('---',0))
    thickness = df.insert(1, "thickness", df['Thickness'].replace('---',0))
    df['description'] = df['Home Story Name'].str.cat(df['Element Type'].apply(str), sep =" | ")
    df['description'] = df['description'].str.cat(df['height'].apply(str), sep =" | ")
    df['description'] = df['description'].str.cat(df['width'].apply(str), sep =" x ")
    df['description'] = df['description'].str.cat(df['thickness'].apply(str), sep =" x ")
    df = df.sort_values(by=['description'])
   #initialise main body and also styles it
    body_1 = html.Div([
        dbc.Alert(
            [
                html.H3('Upload Success!', className = 'alert-heading'),
                html.P('{} has been uploaded.'.format(filename),)
            ],
            id = 'uploadAlert',
            dismissable = True,
            is_open = True,
        ),
        html.H5('{} has been uploaded.'.format(filename),
               style ={'marginBottom': '1em'}
              ),
        html.P('Click "Calculate" to proceed'),
        dbc.Button('Calculate', id='calcBtn', n_clicks=0,),
        #html.P(str(df.to_json())),
        dcc.Store(id = 'data_store', data=df.to_json())

    ], 
    style = {
        'textAlign': 'center'
    },
    id = "id_body_1")
    return body_1

#---------------parse total gwp--------------------

#some shit that make things work...
#app.run_server(mode = 'jupyterlab', port = 8090, dev_tools_ui = True, dev_tools_hot_reload = True, threaded = True)
app.run_server(debug=True, dev_tools_ui = True)
