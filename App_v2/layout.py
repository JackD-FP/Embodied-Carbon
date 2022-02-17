from base64 import encode
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from callback_uploader import update_output
from server import app

layout = [
    html.H1('Embodied Carbon', className="text-center my-5"),
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
        Nunc at velit id libero commodo auctor. Aliquam mauris nibh, euismod sed tristique sit amet, \
        dictum quis nibh. Duis viverra, nunc iaculis pharetra ultrices, \
        urna nisl aliquet sem, at ultricies quam purus vitae nunc. Quisque semper eu turpis vel consequat. \
        Donec mattis varius dui quis vulputate. Phasellus ut dui placerat, tincidunt neque et, volutpat est.\
        Nulla ut vulputate odio. Mauris maximus urna imperdiet tellus suscipit tempus vel sed ex. Mauris id felis turpis. \
        Aenean dictum turpis id viverra volutpat. Aliquam rhoncus quam nibh,\
        a dapibus purus faucibus vel. Vestibulum ornare velit id.', className='w-50 mx-auto mb-3'),
    #html.P('First we need to upload your building schedule', className='w-50 mx-auto mb-3'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Schedule Files')
        ], id='uploader_ui', className='shadow bg-secondary'),
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
    dbc.Tooltip("We need you to upload \
        your building embodied carbon schedule",
        target="uploader_ui",
        placement='bottom'),
    html.Div(id='output-data-upload')  
]

