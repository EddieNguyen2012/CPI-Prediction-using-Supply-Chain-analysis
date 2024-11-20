import dash_bootstrap_components as dbc, html

import dash_bootstrap_components as dbc
from dash import html

def create_navbar(project_name, background_fill = 'dark', text_color = 'white'):
    navbar = dbc.Navbar(
        dbc.Container(
            dbc.Row(
                [
                    # Left-aligned brand
                    dbc.Col(
                        dbc.NavbarBrand(
                            "MTN",
                            href="/",
                            style={
                                'color': text_color
                            }
                        ), width="auto"),

                    # Center-aligned project name
                    dbc.Col(
                        html.Div(
                            project_name,
                            style={
                                "text-align": "center",
                                "font-size": "20px",
                                "font-weight": "bold",
                                'color': text_color}),
                        width="auto", className="mx-auto"
                    ),

                    # Right-aligned dropdown menu
                    dbc.Col(
                        dbc.DropdownMenu(
                            nav=True,
                            in_navbar=True,
                            label='Menu',
                            children=[
                                dbc.DropdownMenuItem("Home", href="/"),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem('Proposals', href="/proposals"),
                                dbc.DropdownMenuItem('Data Processing', href="/processing")
                            ], style={'color': text_color}
                        ),
                        width="auto"
                    )
                ],
                align="center",
                className="w-100",
            )
        ),
        color=background_fill,
        dark=True
    )
    return navbar
