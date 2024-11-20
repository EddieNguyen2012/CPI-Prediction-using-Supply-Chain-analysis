import pandas as pd
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from Nav_bar import create_navbar
from app4 import app

# Load data
ml_prediction = pd.read_csv('~/cs163/src/Data/ML_Prediction.csv', parse_dates=['DATE'], index_col=['DATE'])
ml_prediction['CPI Diff'] = pd.read_csv('~/cs163/src/Data/Diff_CPI.csv', parse_dates=['DATE'], index_col=['DATE'])
other_indices = pd.read_csv('~/cs163/src/Data/mean_only_data.csv', parse_dates=['DATE'], index_col=['DATE'])
main_plot_width = 1200
main_plot_height = 600

# Single plots
def update_background(fig, color):
    fig.update_layout(
        paper_bgcolor='#f7f7e6',
        plot_bgcolor='#f7f7e6',
        xaxis=dict(showgrid=False, gridcolor='#38499E'),  # Change gridline color
        yaxis=dict(showgrid=False, gridcolor='#38499E'),
        font=dict(family='Poppins', color=color),
        title_x=0.5,
        showlegend=False
    )

def update_background_with_grid(fig, color):
    fig.update_layout(
        paper_bgcolor='#f7f7e6',
        plot_bgcolor='#f7f7e6',
        xaxis=dict(showgrid=False, gridcolor=color),  # Change gridline color
        yaxis=dict(showgrid=True, gridcolor=color),
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
            'width': '90%',
            'height': 'auto',
            'display': 'block',
            'margin-top': '5%',
            'margin-left': '5%',
            # 'margin-right': '2%',
            'margin-bottom': '5%'
        }),
    html.Img(
        src='assets/images/Splitter 2.png',
        style={
            'width': '100%',
            'height': 'auto',
        }
    ),
    html.Div(
        ['How did the supply chain prices changed historically?',
         html.Div(
             [
                 dcc.Graph(
                     id='CPI-plot'
                 ),
                 dcc.Graph(
                     id='diff-CPI-plot'
                 ),
             ],

             style={
                 'align-items': 'center',
                 'display': 'flex',
                 'flex-direction': 'row',
                 'justify-content': 'center'
             }
         ),
         html.Div(
             [
                 dcc.Graph(id='PPI-plot'),
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
                 dcc.Graph(id='CE-plot')
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
                 dcc.Graph(id='Electricity-plot'),
                 dcc.Graph(id='RPI-plot')
             ],
             style={
                 'display': 'flex',
                 'flex-direction': 'row',
                 'justify-content': 'space-between',
                 'align-items': 'center',
             }
         )
            ,
         ],
        style={

            'font-size': '30px',

        },
        className='first-plots'
    ),
    html.Div([
        "What are the 'usual' prices for gas and electricity?",
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
            className='energy-hist-flex-box'
        ),
    ],
        style={
            'margin-left': '5%',
            'margin-right': '5%',
            'margin-top': '5%',
            'font-size': '30px'
        }

    )

], style={
    'background-color': '#f7f7e6',
    'color': '#38499E',
    'text-align': 'center',
    'margin': '0 auto'
})

footer = html.Div(
    className='footer',
    children=[
        'You reached footer'
    ],

)

# Page layout function
def create_page_home():
    layout = html.Div([
        nav,
        body,
        footer
    ])
    return layout


def get_presidency_and_color(president):
    time_range = None
    color = None
    if president == 'Biden':
        time_range = pd.date_range(start='2021-01-01', end='2024-08-01', freq='MS')
        color = '#E84324'
    elif president == 'Trump':
        time_range = pd.date_range(start='2017-01-01', end='2021-01-01', freq='MS')
        color = '#38499E'
    elif president == 'Obama':
        time_range = pd.date_range(start='2009-01-01', end='2017-01-01', freq='MS')
        color = '#E84324'
    else:
        time_range = pd.date_range(start='2006-10-01', end='2009-01-01', freq='MS')
        color = '#38499E'
    return time_range, color


@app.callback(
    Output(component_id='CPI-plot', component_property='figure'),
    Input(component_id='president-dropdown', component_property='value')
)
def display_CPI(president):
    time_range, color = get_presidency_and_color(president)
    plot_data = ml_prediction.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['CPI'],
        x=plot_data.index,
        name='CPI Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color)
    ))
    fig.update_layout(
        width=main_plot_width/1.75,
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
            )
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
    plot_data = ml_prediction.loc[time_range]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=plot_data['CPI Diff'],
        x=plot_data.index,
        name='CPI Change Value',
        # labels={'x': 'Timespan', 'y': 'CPI'},
        mode='lines+markers',
        line=dict(color=color)
    ))
    fig.update_layout(
        width=main_plot_width/1.75,
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
            )
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
        width=main_plot_width / 2.5,
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
        width=main_plot_width / 2.5,
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
        width=main_plot_width / 2.5,
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
        width=main_plot_width /2.5,
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
        width=main_plot_width / 2.5,
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

