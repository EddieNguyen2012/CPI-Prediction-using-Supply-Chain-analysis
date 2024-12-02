import dash
import pandas as pd
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from Nav_bar import create_navbar
from app4 import app

#instance variable

RED = '#E84324'
BLUE = '#38499E'
WHITE = '#f7f7e6'
# Load data
ml_prediction = pd.read_csv('~/cs163/src/Data/ML_Prediction.csv', parse_dates=['DATE'], index_col=['DATE'])
ml_prediction['CPI Diff'] = pd.read_csv('~/cs163/src/Data/Diff_CPI.csv', parse_dates=['DATE'], index_col=['DATE'])
other_indices = pd.read_csv('~/cs163/src/Data/mean_only_data.csv', parse_dates=['DATE'], index_col=['DATE'])
PPI_causal = pd.read_csv('~/cs163/src/Data/PPI_granger_causal.csv')
# func = assign("function() {return window.innerWidth}")
main_plot_width = 1000
main_plot_height = 600

# Single plots
def update_background(fig, color):
    fig.update_layout(
        paper_bgcolor='#f7f7e6',
        plot_bgcolor='#f7f7e6',
        xaxis=dict(showgrid=True, gridcolor='#222C62'),  # Change gridline color
        yaxis=dict(showgrid=True, gridcolor='#222C62'),
        font=dict(family='Poppins', color=color),
        title_x=0.5,
        showlegend=False
    )

def update_background_with_grid(fig, color):
    fig.update_layout(
        paper_bgcolor='#f7f7e6',
        plot_bgcolor='#f7f7e6',
        xaxis=dict(showgrid=False, gridcolor=color),  # Change gridline color
        yaxis=dict(showgrid=True, gridcolor='#222C62'),
        font=dict(family='Poppins', color=color),
        title_x=0.5,
        showlegend=False
    )

# Electricity histogram plot
elec_plot = go.Figure()
elec_plot.add_trace(
    go.Histogram(
        x=other_indices['Electricity Price'],
        name='count',
        xbins=dict(size=0.5),
        marker=dict(color='#38499E')
    )
)
elec_plot.update_layout(
        title=dict(
            text='Electricity Price frequency'
        ),
        xaxis=dict(
            title=dict(
                text='Electricity Price (cents/kWh)'
            )
        ),
        yaxis=dict(
            title=dict(
                text='Frequency'
            )
        ),
    )

# Gas histogram plot

gas_plot = go.Figure()
gas_plot.add_trace(
    go.Histogram(
        x=other_indices['Gas Price'],
        name='count',
        xbins=dict(size=0.5),
        marker=dict(color='#E84324')
    )
)
gas_plot.update_layout(
        title=dict(
            text='Gas Price frequency'
        ),
        xaxis=dict(
            title=dict(
                text='Gas Price ($/gallon)'
            )
        ),
        yaxis=dict(
            title=dict(
                text='Frequency'
            )
        ),
    )

update_background_with_grid(gas_plot, '#E84324')
update_background_with_grid(elec_plot, '#38499E')


# Navigation bar
nav = create_navbar('', '#38499E', '#f7f7e6')

# Body content
body = html.Div([
    html.Img(
        src='assets/images/General Election Day Instagram Story.svg',
        style={
            'text-align': 'center',
            'width': '100%',
            'height': 'auto'
        }
    ),
    html.Div(
        'Welcome to my Food and Beverages CPI Prediction project where I explore a new way to estimate the inflation of the Food and Beverages industry instead of using the traditional item basket price method',
        style={
            'padding-top': '5%',
            'padding-left': '10%',
            'padding-right': '10%',
            'font-size': '25px',
            'font-weight': 'normal',
            'text-align': 'center',
        }
    ),
    html.Img(
        src='assets/images/Supply Chain Diagram.png',
        alt='Supply Chain Diagram',
        style={
            'width': '70%',
            'height': '70%',
            'display': 'bloc',
            'margin-top': '5%',
            'margin-right': 'auto',
            'margin-left': 'auto',
            'margin-bottom': '5%',

        }),
    html.Img(
        src='assets/images/Splitter 2.png',
        style={
            'width': '100%',
            'height': 'auto',
        }
    ),
    html.Div(
        [
            html.H2(className='subheading-1', children='How did the supply chain prices changed historically?'),

            html.Div(
                [
                    html.Div(children=[
                        dcc.Graph(
                            id='CPI-plot'
                        ),
                        html.Div(className='image-description',
                                 children='*F&B CPI: Consumer Price Index, the inflation indicator for Food and Beverages'),

                    ]),

                    html.Div(
                        [
                            'Under President ',
                            dcc.Dropdown(
                                id='president-dropdown',
                                placeholder='Select President',
                                value='Biden',
                                searchable=False,
                                clearable=False,
                                options=[
                                    {'label': 'Joe Biden', 'value': 'Biden'},
                                    {'label': 'Donald Trump', 'value': 'Trump'},
                                    {'label': 'Barrack Obama', 'value': 'Obama'},
                                    {'label': 'George W. Bush', 'value': 'Bush'}
                                ],
                                style={
                                    'font-size': '15px',
                                    'width': '300px',
                                    'background-color': '#f7f7e6',
                                    'color': '#38499E',
                                }
                            )
                        ],
                        style={
                            'display': 'inline-box',
                            # 'flex-direction': 'inline',
                            'justify-content': 'center',
                            'align-items': 'center',
                            # 'gap': '20px',
                            'font-size': '25px',

                        }
                    )
                    ,
                    html.Div(children=[

                        dcc.Graph(
                            id='diff-CPI-plot'
                        ),
                        html.Div(className='image-description',
                                 children='*Differenced CPI: the change of CPI using current value - last value'),
                    ]),
                ],

                style={
                    'align-items': 'center',
                    'display': 'flex',
                    'flex-direction': 'row',
                    'justify-content': 'space-between'
                }
            ),
            html.Div(
                [
                    html.Div(children=[

                        dcc.Graph(
                            id='PPI-plot'
                        ),
                        html.Div(className='image-description',
                                 children='*PPI: Producer Price Index - average change over time in the selling prices received by domestic producers for their outputs'),
                    ]),
                    html.Div(children=[

                        dcc.Graph(
                            id='RPI-plot'
                        ),
                        html.Div(className='image-description',
                                 children='*RPI: Price Received Index - estimate the prices producers receive for approximately 100 crop and livestock commodities'),
                    ]),

                    html.Div(children=[

                        dcc.Graph(
                            id='CE-plot'
                        ),
                        html.Div(className='image-description',
                                 children='*CE: Consumer Expenditures - Average annual expenditures for all consumer units'),
                    ]),
                ],
                style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'justify-content': 'space-between',
                    'align-items': 'center',

                })
            ,
            html.Div(
                [
                    dcc.Graph(id='Gas-plot'),
                    dcc.Graph(id='Electricity-plot')
                ],
                style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'justify-content': 'center',
                    'align-items': 'center',
                }
            )
            ,
        ],
        style={
            'font-size': '30px',
            'padding-left': '5%',
            'padding-right': '5%'
        },
        className='first-plots'
    ),
    html.Div([
        html.H2(className='subheading-1', children="What are the 'usual' prices for gas and electricity?"),
        html.Div(
            [
                dcc.Graph(
                    id='hist-gas',
                    figure=gas_plot
                ),
                dcc.Graph(
                    id='hist-elec',
                    figure=elec_plot
                )
            ],
            className='energy-hist-flex-box',
            style={
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center'
            }
        ),
    ],
        style={
            'margin-left': '5%',
            'margin-right': '5%',
            'margin-top': '5%',
            'font-size': '30px',

        }
    ),
    html.Div(children=[
        html.H2(className='subheading-1', children='Which PPI sector affect CPI the most?'),
        html.Div(className='image-description', children='*PPI sector: The specific PPI calculated from each sector'),
        dcc.Graph(
            figure=
                px.pie(
                    width=main_plot_width,
                    names=PPI_causal.iloc[:,0],
                    values=PPI_causal.iloc[:,1],
                    ).update_layout(
                    legend=dict(
                        orientation="v",  # Horizontal layout
                        yanchor="middle",  # Place the legend at the bottom
                        y=0.5,  # Adjust the vertical position (negative value places it below the plot)
                    ),
                    font=dict(color=BLUE),
                    paper_bgcolor='#f7f7e6',
                    plot_bgcolor='#f7f7e6',
                )

        )
    ],
    style={
        'margin-left': '10%',
        'margin-right': '10%'
    }),
    html.Img(
        src='assets/images/Splitter 2.png',
        style={
            'width': '100%',
            'height': 'auto',
        }
    ),

], style={
    'background-color': '#f7f7e6',
    'color': '#38499E',
    'text-align': 'center',
    'margin': '0 auto'
})

footer = html.Div(
    className='footer',
    children=[
        html.Div(
            className='footer-content-blue',
            children=[
                'Manh Tuong Nguyen',
                html.Br(),
                'Email: tuong62642@gmail.com',
                html.Br(),
                'GitHub: https://github.com/EddieNguyen2012',
                html.Br(),
                'LinkedIn: www.linkedin.com/in/manh-tuong-nguyen'
            ]
        )
    ],
)

# Page layout function
def create_page_home():
    layout = html.Div([
        nav,
        dcc.Store(id='window-width-store', storage_type='session'),
        body,
        footer
    ])
    return layout


def get_presidency_and_color(president):
    time_range = None
    color = None
    if president == 'Biden':
        time_range = pd.date_range(start='2021-01-01', end='2024-08-01', freq='MS')
        color = BLUE
    elif president == 'Trump':
        time_range = pd.date_range(start='2017-01-01', end='2021-01-01', freq='MS')
        color = RED
    elif president == 'Obama':
        time_range = pd.date_range(start='2009-01-01', end='2017-01-01', freq='MS')
        color = BLUE
    else:
        time_range = pd.date_range(start='2007-10-01', end='2009-01-01', freq='MS')
        color = RED
    return time_range, color


@app.callback(
    Output(component_id='CPI-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_CPI(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = ml_prediction.loc[time_range]['CPI']
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data,
        x=plot_data.index,
        name='CPI Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color)
    ))
    fig.update_layout(
        width=main_plot_width/2.2,
        height=main_plot_height/1.5,
        title=dict(
            text='CPI under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='CPI'
            ),
            range=[plot_data.min() - 5, plot_data.min() + 60]
        ),

    )
    update_background(fig, color)

    return fig

@app.callback(
    Output(component_id='diff-CPI-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_d_CPI(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = ml_prediction.loc[time_range]['CPI Diff']
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data,
        x=plot_data.index,
        name='CPI Change Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color),
    ))
    fig.update_layout(
        width=main_plot_width/2.2,
        height=main_plot_height/1.5,
        title=dict(
            text='CPI monthly change under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='CPI change'
            ),
            range=[-5,5]
        ),
    )
    update_background(fig, color)

    return fig

@app.callback(
    Output(component_id='PPI-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_PPI(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = other_indices.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['PPI'],
        x=plot_data.index,
        name='PPI Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color),

    ))
    fig.update_layout(
        width=main_plot_width / 2.6,
        height=main_plot_height / 1.5,
        title=dict(
            text='PPI under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='PPI'
            )
        ),
    )
    update_background(fig, color)

    return fig


@app.callback(
    Output(component_id='RPI-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_RPI(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = other_indices.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['RPI'],
        x=plot_data.index,
        name='RPI Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color),

    ))
    fig.update_layout(
        width=main_plot_width / 2.6,
        height=main_plot_height / 1.5,
        title=dict(
            text='RPI under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='RPI'
            )
        ),
    )
    update_background(fig, color)

    return fig


@app.callback(
    Output(component_id='CE-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_CE(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = other_indices.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['CE'],
        x=plot_data.index,
        name='CE Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color),

    ))
    fig.update_layout(
        width=main_plot_width / 2.6,
        height=main_plot_height / 1.5,
        title=dict(
            text='CE under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='CE'
            )
        ),
    )
    update_background(fig, color)

    return fig


@app.callback(
    Output(component_id='Gas-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_gas(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = other_indices.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['Gas Price'],
        x=plot_data.index,
        name='Gas Price',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color),

    ))
    fig.update_layout(
        width=main_plot_width /2.4,
        height=main_plot_height / 1.5,
        title=dict(
            text='Gas Price under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='Gas Price ($/gallon)'
            )
        ),
    )
    update_background(fig, color)

    return fig


@app.callback(
    Output(component_id='Electricity-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_gas(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = other_indices.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['Electricity Price'],
        x=plot_data.index,
        name='Electricity Price',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color),

    ))
    fig.update_layout(
        width=main_plot_width / 2.4,
        height=main_plot_height / 1.5,
        title=dict(
            text='Electricity Price under President ' + president
        ),
        xaxis=dict(
            title=dict(
                text='Timespan'
            )
        ),
        yaxis=dict(
            title=dict(
                text='Electricity Price (cents/kWh)'
            )
        ),
    )
    update_background(fig, color)

    return fig
