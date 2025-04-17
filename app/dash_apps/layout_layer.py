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
              html.P('Floriano StatView - Informações Gerais')
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
