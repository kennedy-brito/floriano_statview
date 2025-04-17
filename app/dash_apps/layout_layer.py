from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd
from . import graph_layer as graph

def create_layout():
    """Cria o layout do aplicativo Dash."""
    return html.Div(
        children = [
          html.Header(
            children= [
              html.P('Floriano StatView - Informações Gerais'),
              html.Main(
                id='content',
                children=[
                  html.Div(
                    id='total-population',
                    children=[
                      html.P("População Total"),
                      html.H3(f"{graph.get_metric_total_population()}")
                    ]
                  ),
                  html.Div(
                    id='local-distribution',
                    children=[
                      html.P("It's working")
                    ]
                  ),
                  html.Div(
                    id='race-distribution',
                    children=[
                      html.P("It's working")
                    ]
                  ),
                  html.Div(
                    id='total-pib',
                    children=[
                      html.P("It's working")
                    ]
                  ),
                  html.Div(
                    id='age-pyramid',
                    children=[
                      html.P("It's working")
                    ]
                  ),
                  html.Div(
                    id='most-populated-cities',
                    children=[
                      html.P("It's working")
                    ]
                  ),
                ]
              )
            ]
          )
        ]
        )

def create_app(url_path, server=None):
    """Cria e retorna o servidor Flask para o app Dash."""
    app = Dash(requests_pathname_prefix=url_path)
    app.title = "Taxa de Alfabetização - Floriano x Piauí x Brasil"

    app.layout = create_layout()

    return app.server
