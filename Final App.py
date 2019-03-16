import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from flask import Flask, json
from dash import Dash
from dash.dependencies import Input, Output
import dash_table_experiments as dt


external_css = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css?family=Raleway',
    '//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://codepen.io/amyoshino/pen/jzXypZ.css',
]


layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=10,
        r=20,
        b=0,
        t=0
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)

layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

app = dash.Dash(__name__, external_stylesheets=external_css)

xls = pd.ExcelFile('london_PI_index.xlsx')
df1 = pd.read_excel(xls, sheet_name="london_index",sep='\t')
df2 = df1[["year", "region","market", "dur_stay","mode","purpose","predict_stay","15_more_prob"]]


mapbox_access_token ="pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

colorscale_magnitude = [
    [0, '#ffffb2'],
    [0.25, '#fecc5c'],
    [0.5, '#fd8d3c'],
    [0.75, '#f03b20'],
    [1, '#bd0026'],
]



theme = {
    'font-family': 'Raleway',
    'background-color': '#787878',
}



def create_header(some_string):
    header_style = {
        'background-color': theme['background-color'],
        'padding': '1.5rem',
    }
    header = html.Header(html.H1(children=some_string, style=header_style))
    return header


def create_dropdowns():
    drop1 = dcc.Dropdown(
        options=[
            {'label': 'Light', 'value': 'light'},
            {'label': 'Dark', 'value': 'dark'},
            {'label': 'Satellite', 'value': 'satellite'},
            {
                'label': 'Custom',
                'value': 'mapbox://styles/jackdbd/cj6nva4oi14542rqr3djx1liz'
            }
        ],
        value='dark',
        id='dropdown-map-style',
        className='three columns offset-by-one'
    )
    drop2 = dcc.Dropdown(
        options=[
                    {'label': 'World', 'value': 'world'},
                    {'label': 'Central Africa', 'value': 'Central Africa'},
                    {'label': 'Central America & South America', 'value': 'Central America & South America'},
                    {'label': 'Central Europe', 'value': 'Central Europe'},              
                    {'label': 'Eastern Europe', 'value': 'Eastern Europe'},            
                    {'label': 'Eastern Africa', 'value': 'Eastern Africa'},
                    {'label': 'North & Central Asia', 'value': 'North & Central Asia'},
                    {'label': 'North Africa', 'value': 'North Africa'},            
                    {'label': 'Northern Europe', 'value': 'Northern Europe'},
                    {'label': 'North America', 'value': 'North America'},
                    {'label': 'South Africa', 'value': 'South Africa'},
                    {'label': 'South Asia', 'value': 'South Asia'},
                    {'label': 'Southeast Asia', 'value': 'Southeast Asia'},            
                    {'label': 'Southeast Europe', 'value': 'Southeast Europe'},
                    {'label': 'Southern Europe', 'value': 'Southern Europe'},
                    {'label': 'Southwest Europe', 'value': 'Southwest Europe'},            
                    {'label': 'West Africa', 'value': 'West Africa'},
                    {'label': 'West Asia (midele East or Near East)', 'value': 'West Asia (midele East or Near East)'},
                    {'label': 'Western Europe', 'value': 'Western Europe'},
                    {'label': 'Oceania', 'value': 'Oceania'},                    

        ],
        value='Western Europe',
        id='dropdown-region',
        className='three columns offset-by-four'
    )
    drop3 = dcc.Dropdown(
        options=[
                    {'label': 'Air', 'value': 'Air'},
                    {'label': 'Sea', 'value': 'Sea'},
                    {'label': 'Tunnel', 'value': 'Tunnel'},
        ],
        value='Air',
        id='dropdown-mode',
        className='three columns offset-by-one'
    )
    drop4 = dcc.Dropdown(
        options=[
                    {'label': 'Holiday', 'value': 'Holiday'},
                    {'label': 'Business', 'value': 'Business'},
                    {'label': 'VFR', 'value': 'VFR'},
                    {'label': 'Miscellaneous', 'value': 'Miscellaneous'},
        ],
        value='Holiday',
        id='dropdown-purpose',
        className='three columns offset-by-four'
    )
    return [drop1, drop2,drop3,drop4]





def create_description():
    div = html.Div(
        children=[
            dcc.Markdown('''
London, the capital of England and the United Kingdom, is a world’s leading tourism destinations. 
According to Wikipedia, the city attracted nearly 20 million international visitors in 2016, which making it one of the world’s most visited in terms of international tourists. Research has been showing that tourists that enter the UK under for significant durations can have a higher probability of staying beyond the legally determined length of visits. International tourists who remain in the Greater London Area (GLA) can influence the city’s KPI levels aligned to job performance and socioeconomic indicators. The current analysis was carried out to construct foundational classification capabilities, centered on detecting patterns regarding individual sovereign nation’s tourism patterns, given their respective socio-economic prosperity indicators to the GLA have the highest probability levels of having citizens stay 15+ days.  The success of the classification model and visualization platform will provide a basis for next generation predictive capabilities in detecting international prosperity measures and London tourism patterns.  

---
            '''),
        ],
    )
    return div

def create_content():
    # create empty figure. It will be updated when _update_graph is triggered
    graph = dcc.Graph(id='graph-geo',hoverData={'points': [{'customdata': df1['market']}]})
    content = html.Div(graph, id='content')
    return content


regions = {
    'world': {'lat': 0, 'lon': 0, 'zoom': 0},

    'Western Europe': {'lat': 50, 'lon': 0, 'zoom': 3},
    'Eastern Europe': {'lat': 40, 'lon': 30, 'zoom': 3},
    'Central Europe': {'lat': 50, 'lon': 0, 'zoom': 2},
    'Northern Europe': {'lat': 70, 'lon': 0, 'zoom': 3},
    'Southeast Europe': {'lat': 40, 'lon': 20, 'zoom': 3},
    'Southern Europe': {'lat': 50, 'lon': 0, 'zoom': 3},
    'Southwest Europe': {'lat': 50, 'lon': -10, 'zoom': 3},


    'North America': {'lat': 40, 'lon': -100, 'zoom': 2},
    'Central America': {'lat': -15, 'lon': -60, 'zoom': 2},

    'Central Africa': {'lat': 0, 'lon': 20, 'zoom': 3},
    'Eastern Africa': {'lat': 10, 'lon': 40, 'zoom': 3},
    'South Africa': {'lat': -20, 'lon': 0, 'zoom': 3},
    'West Africa': {'lat': 20, 'lon': 0, 'zoom': 3},
    'North Africa': {'lat': 30, 'lon': 20, 'zoom': 3},

    'North & Central Asia': {'lat': 30, 'lon': 100, 'zoom': 3},
    'South Asia': {'lat': 0, 'lon': 80, 'zoom': 3},
    'West Asia': {'lat': 30, 'lon': 70, 'zoom': 3},
    'Southeast Asia': {'lat': 0, 'lon': 120, 'zoom': 3},

    'Oceania': {'lat': -10, 'lon': 130, 'zoom': 2},
}



app_name = 'London Tourism'
server = Flask(app_name)
app = Dash(name=app_name, server=server)


app.layout = html.Div(
    children=[
        create_header(app_name),
        create_description(),
        html.Div(
            children=[
                html.Div(create_dropdowns(), className='row'),
                html.Div(
                    dcc.Slider(
                        id='year-slider',
                        min=df1['year'].min(),
                        max=df1['year'].max(),
                        value=df1['year'].min(),
                        marks={str(year): str(year) for year in df1['year'].unique()}),
                    className='row',style={'margin-top': '20','margin-bottom': '20'}),                
                html.Div(create_content(), className='row'),

                html.Div([
                    html.Div([
                        dcc.Graph(id='x-time-series'),], style={'display': 'inline-block', 'width': '49%'},className='six columns'),
                    html.Div([
                        dcc.Graph(id='x-time-scatter'),], style={'display': 'inline-block', 'width': '49%'},className='six columns'),

                    ]),

                html.Div([
                    dt.DataTable(
                        rows=[{}],
                        columns=df2.columns,
                        filterable=True,
                        sortable=True,
                        id='datatable'),
                        ],
                        style = layout_table,
                        className="rows"),
                
            ],
        ),
    ],
    className='container',
    style={'font-family': theme['font-family']}
)







for css in external_css:
    app.css.append_css({'external_url': css})


@app.callback(
    output=Output('graph-geo', 'figure'),
    inputs=[Input('dropdown-map-style', 'value'),
            Input('dropdown-region', 'value'),
            Input('year-slider', 'value'),
            Input('dropdown-mode', 'value'),
            Input('dropdown-purpose', 'value')])

def _update_graph(map_style, region, selected_year,selected_mode,selected_purpose):
    dff = df1[df1['year'] == selected_year]
    dff = dff[df1['mode'] == selected_mode]
    dff = dff[df1['purpose'] == selected_purpose]

    radius_multiplier = {'outer': 10}
    dff['text1'] = dff['market'] +' Actual_Dur_stay = '+ dff['actual_dur_stay'].map(str) + ' Predict_dur_stay ='+ dff['predict_stay'].map(str) + ' Prob_stay_morethan15days = '+ dff['15_more_prob'].map(str)

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        height=550,
        font=dict(family=theme['font-family']),
        margin=go.Margin(l=0, r=0, t=40, b=20),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=regions[region]['lat'],
                lon=regions[region]['lon'],
            ),
            pitch=0,
            zoom=regions[region]['zoom'],
            style=map_style,
        ),
    )

    data = go.Data([
        go.Scattermapbox(
            lat=dff['lat'],
            lon=dff['lon'],
            mode='markers',
            marker=go.Marker(
                size=(dff['15_more_prob'])*radius_multiplier['outer'],
                colorscale=colorscale_magnitude,
                color=dff['15_more_prob'],
                opacity=1,
            ),
            customdata= dff['market'],
            text=dff['text1'],
            showlegend=False,
        ),
    ])

    figure = go.Figure(data=data, layout=layout)
    return figure

def create_time_series(dff, title):
    return {
        'data': [go.Box(
            x=dff['year'],
            y=dff['15_more_prob'],
        )],
        'layout': {
            'height': 400,
            'margin': {'l': 30, 'b': 40, 'r': 20, 't': 20},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

def create_country_series(dff, title):
    return {
        'data': [go.Box(
            x=dff['actual_dur_stay'],
            y=dff['15_more_prob'],
        )],
        'layout': {
            'height': 400,
            'margin': {'l': 30, 'b': 40, 'r': 20, 't': 20},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    Output('x-time-series', 'figure'),
    [Input('graph-geo', 'hoverData'),
     Input('dropdown-region', 'value'),   
     Input('dropdown-mode', 'value'),
     Input('dropdown-purpose', 'value')])

def update_y_timeseries(hoverData,region,selected_mode,selected_purpose):
    country_name = hoverData['points'][0]['customdata']
    dff = df1[df1['mode'] == selected_mode]
    dff = dff[df1['purpose'] == selected_purpose]
    dff = dff[df1['market'] == country_name]
    title = '<b>{}</b><br>{}'.format(country_name, region)
    return create_time_series(dff, title)

@app.callback(
    Output('x-time-scatter', 'figure'),
    [Input('graph-geo', 'hoverData'),   
     Input('dropdown-mode', 'value'),
     Input('dropdown-purpose', 'value'),
     Input('year-slider', 'value')])

def update_x_countrygraph(hoverData,selected_mode,selected_purpose,years):
    country_name = hoverData['points'][0]['customdata']
    dff = df1[df1['mode'] == selected_mode]
    dff = dff[df1['purpose'] == selected_purpose]
    dff = dff[df1['market'] == country_name]
    title = '<b>{}</b><br>{}'.format(country_name, years)
    return create_country_series(dff, title)

@app.callback(
    Output('datatable', 'rows'),
    [Input('graph-geo', 'hoverData'),
     Input('year-slider', 'value')])

def update_selected_row_indices(hoverData, selected_year):
    country_name = hoverData['points'][0]['customdata']
    dff= df2[df2['year'] == selected_year]
    dff = dff[df2['market'] == country_name]

    
    rows = dff.to_dict('records')

    return rows




if __name__ == '__main__':
    app.run_server(debug=True)

