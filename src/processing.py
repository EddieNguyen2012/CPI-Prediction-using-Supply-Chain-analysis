from dash import html
from Nav_bar import create_navbar

nav = create_navbar('Food and Beverages CPI Prediction using cost pass-through in the supply chain')

header = html.H3('Here is Processing Page')

def create_page_processing():
    layout = html.Div([
        nav,
        header,
    ])
    return layout