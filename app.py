import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
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

# GeoDataframe built from NYC OpenData geojson. Includes Boroughs, Councils, Communities, Congress, Assembly, Senate districts of NYC
gdf = gpd.read_file(r'Data\districts.geojson')

# High level drop down to select a type of district
district_type_dd = html.Div([

    html.Label('District Type'),

    dcc.Dropdown(
        options=[{'label': j, 'value': j}
                 for j in sorted(gdf.dist_type.unique())],
        value='Borough',
        id='district-type',
        clearable=False)
])

# Low level drop down to select one or many subsets of the selected district type
district_id_dd = html.Div([

    html.Label('District Id'),

    dcc.Dropdown(
        options=[],
        id='district-id',
        multi=True)
])

# Dashboard sidebar. Will contain drop downs to control main canvas, links, and possibly a hero message... TBD.
sidebar = html.Div(
    [
        html.H2("Activisla", className="display-4"),
        html.Hr(),
        html.P(
            "NYC Activist Dashboard", className="lead"
        ),
        dbc.Nav([district_type_dd, district_id_dd], vertical=True),
    ],

    style=SIDEBAR_STYLE,
    id="sidebar",
)

# Main content / canvas
content = html.Div(children=[

    # Mapping Row
    dcc.Graph(
        id='display-map',
        figure={}
    ),  # End District Map Row

    # Card Row
    dbc.Row(
        [
            dbc.Col("Hi! I'll be a card! Maybe even a chart!"),
            dbc.Col("Hi! I'll be a card!"),
            dbc.Col("Hi! I'll be a card!")
        ],

        # CSS Styling
        style={"text-align": "center",
               "border-style": "solid", "border-color": "black"}

    ),  # End Middle Row of Three Columns.
],  # End Content Div Children
    style=CONTENT_STYLE
)  # End Content Div


# App layout
app.layout = html.Div([sidebar, content])


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
                                   zoom=8.25)

        return fig


# Run server
if __name__ == '__main__':
    app.run_server()
