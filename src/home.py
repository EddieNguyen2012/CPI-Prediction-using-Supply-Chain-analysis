import pandas as pd
from dash import html, dcc, Input, Output
import plotly.express as px
from Nav_bar import create_navbar
from app4 import app

# Load data
ml_prediction = pd.read_csv('Data/ML_Prediction.csv', parse_dates=['DATE'], index_col=['DATE'])

fig = px.line(ml_prediction.loc['2023-01-01':], title="CPI Prediction Over Time", labels={'x': 'Timespan', 'y': 'CPI'})

fig.update_xaxes(rangeslider_visible=True)

# Navigation bar
nav = create_navbar('Food and Beverages CPI Prediction using cost pass-through in the supply chain')


# Page layout function
def create_page_home():
    layout = html.Div([
        nav,
        html.Div(
            'Welcome to my Food and Beverages CPI Prediction project where I explore a new way to estimate the inflation of the Food and Beverages industry instead of using the traditional item basket price method',
            style={
                'padding-top': '100px',
                'padding-left': '10%',
                'padding-right': '10%',
                'font-size': '25px',
                'font-weight': '700',
                'text-align': 'center'
            }
        ),
        html.Img(src='assets/images/Supply Chain Diagram.png',
                 height=520, width=1024, alt='Supply Chain Diagram',
                 style={
                     'display': 'block',
                     'margin-top': '60px',
                     'margin-left': 'auto',
                     'margin-right': 'auto',
                 })

    ])
    return layout
