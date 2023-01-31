import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-righ": "2rem",
    "padding": "2rem 1rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

app = Dash(__name__, serve_locally=False,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

# GeoDataframe built from NYC OpenData geojson files and Ban the Scan NYC dataset.
# Includes Boroughs, Councils, Communities, Congress, State Assembly, and State Senate districts of NYC
# Also includes summation of number of cameras, shooting incidents, and murders in each individual district.
gdf = gpd.read_file(r'Data\districts.geojson')

# High level drop down to select a type of district
district_type_dd = html.Div([

    # Drop down label
    html.Label('District Type'),

    dcc.Dropdown(
        # Create high level drop down options via unique dist_types from the districts GeoDataFrame
        options=[{'label': j, 'value': j}
                 for j in sorted(gdf.dist_type.unique())],
        # Initial value
        value='Borough',
        # Id for call back
        id='district-type',
        # Must chose one
        clearable=False)
])

# Low level drop down to select one or many subsets of the selected district type
district_id_dd = html.Div([
    
    # Drop down label
    html.Label('District Id'),

    dcc.Dropdown(
        # Options to be filled by call back
        options=[],
        # Id for callback
        id='district-id',
        # Ability to select multiple sub-districts
        multi=True)
])

# Dashboard sidebar. Will contain drop downs to control main canvas, links, and possibly a hero message... TBD.
sidebar = html.Div(
    [   # Name of site
        html.H2("Activisla", className="display-4"),
        html.Hr(),
        # Tag line
        html.P(
            "NYC Activist Dashboard", className="lead"
        ),
        # Add the drop downs to the sidebar
        dbc.Nav([district_type_dd, district_id_dd], vertical=True),
    ],

    # Style
    style=SIDEBAR_STYLE,
    # Id for call back
    id="sidebar",
)

# Main canvas
content = html.Div(children=[

    # Map and Leadership Row
    dbc.Row([

        # Mapping Column
        dbc.Col([
            # Tag line
            html.H3("District View"),
            # Choropleth Mapbox Graph
            dcc.Graph(
                # Id for callback to build graph
                id='display-map',
                # Call back will return figure.
                figure={},
                # Ditch the ModeBar
                config= dict(displayModeBar = False)
                ),
        # Set to take the left half of the canvas
        ], width=6),

        # District Leadership Column
        dbc.Col([
            # Tag line
            html.H3("District Leadership"),
            # Accordion. All Accordion items follow same logic, not going to document them all. See the first AccordionItem 
            # This is currently hardcoded for Borough Presidents as an example. Need to collect data on other district leaders. 
            dbc.Accordion( 
                [
                # Manhattan Borough President
                dbc.AccordionItem(
                    [   # Name
                        html.P("Mark D. Levine"),
                        # Link to offical website
                        dbc.Button("Borough President Website", href='https://www.manhattanbp.nyc.gov/about/'),
                        # Link to offical contact page
                        dbc.Button("Contact Page", href='https://www.manhattanbp.nyc.gov/contact/')
                    ],
                    # Item title
                    title="Manhattan Borough President",
                ),
            
                dbc.AccordionItem(
                    [
                        html.P("Antonio Reynoso"),
                        dbc.Button("Borough President Website", href='https://www.brooklyn-usa.org/about-bkbpreynoso/'),
                        dbc.Button("Contact Page", href='https://www.brooklyn-usa.org/contact/')
                    ],
                    title="Brooklyn Borough President",
                ),
            
                dbc.AccordionItem([
                    html.P("Donovan Richards Jr."),
                    dbc.Button("Borough President Website", href='https://queensbp.org/about-bp/'),
                    dbc.Button("Contact Page", href='https://queensbp.org/contact/'),
                    ],
                    title="Queens Borough President",
            )   ,

                dbc.AccordionItem([
                    html.P("Vito Fossella"),
                    dbc.Button("Borough President Website", href='https://www.statenislandusa.com/bp-office.html'),
                    dbc.Button("Contact Page", href='https://www.statenislandusa.com/contact.html'),
                    ],
                    title="Staten Island Borough President",
            ),

                dbc.AccordionItem([
                    html.P("Vanessa L. Gibson"),
                    dbc.Button("Borough President Website", href='https://bronxboropres.nyc.gov/'),
                    dbc.Button("Contact Page", href='https://bronxboropres.nyc.gov/contact/')
                    ],
                    title="The Bronx Borough President",
            ),
        # On page load, accordion is collapsed
        ], start_collapsed=True
    )   # Set to take the right half of the canvas
        ], width=6)
    ]), # End Map and Leadership Row

    # Bar Graphs Row
    dbc.Row(
        [   # Camera Data Column
            dbc.Col([
                # Bar graph of Camera Counts
                dcc.Graph(
                    # Id for call back to build graph
                    id='camera-bar',
                    # Figure will be returned by call back
                    figure={},
                    # Ditch the ModeBar
                    config= dict(displayModeBar = False)
                )
            # Set to take left half of the canvas
            ], width=6),

            # Shooting Incident Data Column
            dbc.Col([
                # Bar Graph of Shooting incidents & Murders
                dcc.Graph(
                    # Id for call back to build graph
                    id='shooting-bar',
                    # Figure will be returned by call back
                    figure={},
                    # Ditch the ModeBar
                    config= dict(displayModeBar = False)
                )
            # Set to take the right half of the canvas
            ], width=6)
        ]

    ), # End Bar Graphs Row

    # Another Bar Graphs Row
    dbc.Row(
        [   # Shooting Incidents & Camera Data Column
            dbc.Col([
                # Bar Graph of Shooting vs Camera Counts
                dcc.Graph(
                    # Id for call back to build graph
                    id='shootCam',
                    # Figure will be returned by call back
                    figure= {},
                    # Ditch the ModeBar
                    config= dict(displayModeBar = False)
                )
            # Set to take the left half of the canvas
            ], width=6),

            # Murders & Camera Data Column
            dbc.Col([
                # Bar Graph of Murder vs Camera Counts
                dcc.Graph(
                    # Id for call back to build graph
                    id='murderCam',
                    # Figure will be returned by call back
                    figure={},
                    # Ditch the ModeBar
                    config= dict(displayModeBar = False)
                )
            # Set to take the right half of the canvas
            ], width=6)
        ]

    ), # End Another Bar Graph Row

    # Regression row
    dbc.Row(
        [   # One column for now.
            dbc.Col([
                # Scatterplot with regression line 
                dcc.Graph(
                    # Id for call back to build graph
                    id='display-regression',
                    # Figure will be returned by call back 
                    figure={},
                    # Ditch the ModeBar
                    config=dict(displayModeBar= False)
                ),
            ]),
        ]
    ) # End Regression Row
],  # End Content Div Children
    style=CONTENT_STYLE
)  # End Content Div

# App layout
app.layout = html.Div([sidebar, content])

########## BEGIN CALL BACKS ##########

# Callback to handle options for low level dropdown based on the high level selection.
@app.callback(
    Output('district-id', 'options'),
    Input('district-type', 'value')
)



def set_district_id_options(selected_type):
    gdff = gdf[gdf.dist_type == selected_type]
    return [{'label': c, 'value': c} for c in sorted(gdff.id.unique())]



# Callback to create the list that will feed into the lower level drop down options
@app.callback(
    Output('district-id', 'value'),
    Input('district-id', 'options')
)



def set_id_values(available_options):
    print(available_options)
    return [x['value'] for x in available_options]



# Callback to update figure on main canvas
@app.callback(
    Output('display-map', 'figure'),
    Input('district-id', 'value'),
    Input('district-type', 'value')
)



def update_graph(selected_id, selected_type):

    print(selected_id)
    print(selected_type)

    if len(selected_id) == 0:
        return Dash.no_update

    else:

        df = gdf[(gdf.dist_type == selected_type) & (gdf.id.isin(selected_id))]

        fig = px.choropleth_mapbox(df,
                                   geojson=df.geometry,
                                   locations=df.index,
                                   color="id",
                                   center={"lat": 40.73, "lon": -73.99},
                                   mapbox_style="carto-positron",
                                   zoom=9.00
                                   )
        fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                        ))

        fig.update_layout(margin=dict(
                        l=0,
                        r=0,
                        b=5,
                        t=0,
                        pad=2
                    ),)

        return fig



# Callback for camera count bar plot
@app.callback(
    Output('camera-bar', 'figure'),
    Input('district-id', 'value'),
    Input('district-type', 'value')
)



def updateCamBar(selected_id, selected_type):

    print(selected_id)
    print(selected_type)

    if len(selected_id) == 0:
        return Dash.no_update

    else:

        df = gdf[(gdf.dist_type == selected_type) & (gdf.id.isin(selected_id))]

        fig = px.bar(df,
                   x='id',
                   y="n_cameras",
                   text='n_cameras',
                   labels={'id': "District ID", 'n_cameras': 'Number of Cameras'},
                   title="Camera Counts by " + selected_type + " ID."
                   )

        fig.update_layout(margin=dict(
                        l=0,
                        r=0,
                        pad=2
                    ),)

        return fig



# Callback for Shooting Incidents / Murders grouped bar plot
@app.callback(
    Output('shooting-bar', 'figure'),
    Input('district-id', 'value'),
    Input('district-type', 'value')
)



def updateSIBar(selected_id, selected_type):

    print(selected_id)
    print(selected_type)

    if len(selected_id) == 0:
        return Dash.no_update

    else:

        df = gdf[(gdf.dist_type == selected_type) & (gdf.id.isin(selected_id))]

        fig = go.Figure(
            data= [
                go.Bar(name='Shootings',x=df['id'], y=df['n_shootings'], text=df['n_shootings']),
                go.Bar(name='Murders', x=df['id'], y=df['n_murders'], text=df['n_murders'])
                ]
            )

        fig.update_layout(title='Shooting Incidents and Murders by ' + selected_type +" ID.",
                         barmode='group')

        fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99
                        ))

        fig.update_layout(margin=dict(
                        l=0,
                        r=0,
                        pad=2
                    ),)

        return fig



# Callback for Cameras - Shootings histogram
@app.callback(
    Output('shootCam', 'figure'),
    Input('district-id', 'value'),
    Input('district-type', 'value')
)



def updateShootCam(selected_id, selected_type):

    print(selected_id)
    print(selected_type)

    if len(selected_id) == 0:
        return Dash.no_update

    else:
        
        df = gdf[(gdf.dist_type == selected_type) & (gdf.id.isin(selected_id))]

        fig = go.Figure(
            data= [
                go.Bar(name='Cameras',x=df['id'], y=df['n_cameras'], text=df['n_cameras']),
                go.Bar(name='Shootings', x=df['id'], y=df['n_shootings'], text=df['n_shootings'])
                ]
            )

        fig.update_layout(title='Shooting Incidents & Camera Presence by ' + selected_type +" ID.",
                         barmode='group')

        fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99
                        ))

        fig.update_layout(margin=dict(
                        l=0,
                        r=0,
                        pad=2
                    ),)

        return fig



# Callback for Cameras - Murders bar graph
@app.callback(
    Output('murderCam', 'figure'),
    Input('district-id', 'value'),
    Input('district-type', 'value')
)
def updateMurderCam(selected_id, selected_type):

    print(selected_id)
    print(selected_type)

    if len(selected_id) == 0:
        return Dash.no_update

    else:
        df = gdf[(gdf.dist_type == selected_type) & (gdf.id.isin(selected_id))]

        fig = go.Figure(
            data= [
                go.Bar(name='Cameras',x=df['id'], y=df['n_cameras'], text=df['n_cameras']),
                go.Bar(name='Murders', x=df['id'], y=df['n_murders'], text=df['n_murders'])
                ]
            )

        fig.update_layout(title='Murders & Camera Presence by ' + selected_type +" ID.",
                         barmode='group')

        fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99
                        ))

        fig.update_layout(margin=dict(
                        l=0,
                        r=0,
                        pad=2
                    ),)

        return fig



# Callback for scatter plot regression
@app.callback(
    Output('display-regression', 'figure'),
    Input('district-id', 'value'),
    Input('district-type', 'value')
)
def updateRegression(selected_id, selected_type):

    print(selected_id)
    print(selected_type)

    if len(selected_id) == 0:
        return Dash.no_update

    else:

        df = gdf[(gdf.dist_type == selected_type) & (gdf.id.isin(selected_id))]

        fig = px.scatter(
                    df,
                    x='n_cameras',
                    y='n_shootings',
                    opacity=0.65,
                    trendline='ols',
                    trendline_color_override='darkblue'
                )

        fig.update_layout(title="Regression")

        fig.update_layout(margin=dict(
                        l=0,
                        r=0,
                        pad=2
                    ),)
        
        return fig



# Run server
if __name__ == '__main__':
    app.run_server()

