from dash import html, dcc
from dash.dependencies import Input, Output
from home import create_page_home
from proposal import create_page_proposal
from processing import create_page_processing
from app4 import app
import pandas as pd

application = app.server
app.config.suppress_callback_exceptions = True

original_data = pd.read_csv('Data/final.csv')
ml_prediction = pd.read_csv('Data/ML_Prediction.csv')
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    # dcc.Store(id='original-data', data=original_data.to_dict('records')),
    # dcc.Store(id='ml-prediction', data=ml_prediction.to_dict('records'))
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/proposals':
        return create_page_proposal()
    if pathname == '/processing':
        return create_page_processing()
    else:
        return create_page_home()

if __name__ == '__main__':
    app.run_server(debug=False)