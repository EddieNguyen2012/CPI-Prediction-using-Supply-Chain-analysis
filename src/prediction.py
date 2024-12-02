from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from Nav_bar import create_navbar
import pandas as pd
from app4 import app

RED = '#D85840'
CHERRY = '#5D241A'
WHITE = '#F7F7E6'

ml_prediction = pd.read_csv('~/cs163/src/Data/ML_Prediction.csv', parse_dates=['DATE'], index_col=['DATE'])


# mean_only = pd.read_csv('Data/mean_only_data.csv', parse_dates=['DATE'], index_col=['DATE'])


def update_background(fig, color):
    fig.update_layout(
        paper_bgcolor='#f7f7e6',
        plot_bgcolor='#f7f7e6',
        xaxis=dict(showgrid=True, gridcolor='#5D241A'),  # Change gridline color
        yaxis=dict(showgrid=True, gridcolor='#5D241A', zeroline=True, zerolinecolor='#5D241A'),
        font=dict(family='Poppins', color=color),
        title_x=0.5,
        showlegend=True
    )
    return fig


nav = create_navbar('Prediction Model Interaction',
                    background_fill=RED, text_color=WHITE)

body = html.Div(
    className='prediction-body',
    children=[
        html.H1(className='heading-red', children='Prediction from models'),
        html.Div(
            className='paragraph-red',
            children=[
                'Interact with the model below to see how each model performs vs true CPI',
                dcc.Graph(id='prediction-figure'),
                html.Div(
                    className='prediction-button',
                    children=[
                        dcc.Slider(0,2, 1,
                            id='slider',
                            marks={
                                0: {'label': 'Pr Obama (2009-2016)', 'style': {'color': CHERRY}},
                                1: {'label': 'Pr Trump (2017-2020)', 'style': {'color': CHERRY}},
                                2: {'label': 'Pr Biden (2021-2024) (Test)', 'style': {'color': CHERRY}}
                            },

                            value=2,
                            className='slider'
                        ),
                        dcc.RadioItems(
                            id='type-select',
                            options=['CPI Values', 'CPI Changes'],
                            value='CPI Values',
                            inline=True,
                            style={'text-align': 'center'},
                            inputStyle={
                                'margin-right': '10px',
                                'margin-left': '10px'
                            }
                        )
                    ]
                )
            ],
            style={'margin': '0 auto'}),
        html.Br()
    ]
)

footer = html.Div(
    className='footer-red',
    children=[
        html.Div(
            className='footer-content-red',
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


def create_page_prediction():
    layout = html.Div(
        className='methodology-page',
        children=[
            nav,
            body,
            footer
        ])
    return layout


def get_presidency(president):
    time_range = None
    if president == 2:
        time_range = pd.date_range(start='2021-01-01', end='2024-08-01', freq='MS')
    elif president == 1:
        time_range = pd.date_range(start='2017-01-01', end='2021-01-01', freq='MS')
    elif president == 0:
        time_range = pd.date_range(start='2009-01-01', end='2017-01-01', freq='MS')
    return time_range


@app.callback(
    Output('prediction-figure', 'figure'),
    [Input('type-select', 'value'),
     Input(component_id='slider', component_property='value')]
)
def update_figure(value, slider_value):
    time_frame = get_presidency(slider_value)
    data = ml_prediction.loc[time_frame]
    diff_or_not = ''
    if value != 'CPI Values':
        diff_or_not = 'Diff_'
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[diff_or_not + 'LSTM'],
        mode='lines+markers',
        name='LSTM'
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[diff_or_not + 'XGBoost'],
        mode='lines+markers',
        name='XGBoost'
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[diff_or_not + 'SARIMAX'],
        mode='lines+markers',
        name='SARIMAX'
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[diff_or_not + 'CPI'],
        mode='lines+markers',
        name='True CPI'
    ))
    fig.update_layout(
        title='Predicted vs ' + diff_or_not + 'CPI (Values)',
        showlegend=True
    )
    return update_background(fig, CHERRY)


