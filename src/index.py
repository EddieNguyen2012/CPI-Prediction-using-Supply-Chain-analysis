from dash import html, dcc
from dash.dependencies import Input, Output
from home import create_page_home
from proposal import create_page_proposal
from processing import create_page_processing
from prediction import create_page_prediction
from app4 import app
import pandas as pd

application = app.server
app.config.suppress_callback_exceptions = True

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
    if pathname == '/methodology':
        return create_page_processing()
    if pathname == '/prediction':
        return create_page_prediction()
    else:
        return create_page_home()

if __name__ == '__main__':
    app.run_server(debug=False)
