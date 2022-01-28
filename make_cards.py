def make_cards(n):
    if n is None:
        return dash.no_update
    else:
        first_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Build Parameters", className="card-title"),
                    html.Div([
                        html.P("Building Perimeter (meters)", className='mb-1'),
                        dcc.Input(id = 'perimeter', type = 'number', className='border rounded-3'),
                    ], className='my-3'),
                    html.Div([
                        html.P("Building Footprint (sq m)", className='mb-1'),
                        dcc.Input(id = 'footprint', type = 'number', className='border rounded-3'),
                    ], className='my-3'),
                    html.Div([
                        html.P("Floor to Floor Height (meters)", className='mb-1'),
                        dcc.Input(id = 'f2f', type = 'number', className='border rounded-3'),
                    ], className='my-3'),
                    html.Div([
                        html.P("Number of Floors", className='mb-1'),
                        dcc.Input(id = 'f2f', type = 'number', className='border rounded-3'),
                    ], className='my-3'),
                ]
            ),
            className='shadow'
        )


        second_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Card title", className="card-title"),
                    html.P(
                        "This card also has some text content and not much else, but "
                        "it is twice as wide as the first card."
                    ),
                    dbc.Button("Go somewhere", color="primary"),
                ]
            ),
            className='shadow'
        )
        children = dbc.Row(
            [
                dbc.Col(first_card, width = 4),
                dbc.Col(second_card, width = 8)
            ]
        )
        return children