from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd
from . import graph_layer as graph

def card_metric(title: str, value: str):
  return html.Div(
      className="metric-card",
      children=[
          html.P(title),
          html.H3(value)
      ]
  )


def card_graph(title: str, graph_id: str, figure):
  return html.Div(
      className="graph-card",
      children=[
          html.P(title),
          dcc.Graph(id=graph_id, figure=figure)
      ]
  )


def create_layout():
  """Cria o layout do aplicativo Dash."""
  return html.Div([
      html.Header([
          html.H1('Floriano StatView - Informações Gerais')
      ]),
      html.Main(id='content', children=[
          card_metric("População Total", graph.get_metric_total_population()),
          card_graph("Distribuição da População por Local", 'location-distribution-graph', graph.location_distribution()),
          card_graph("Distribuição da População por Cor", 'race-distribution-graph', graph.race_distribution()),
          card_metric("PIB de Floriano", graph.get_metric_total_pib()),
          card_graph("Faixa Etária da Cidade", 'age-pyramid-graph', graph.age_pyramid()),
          card_graph("Cidades Mais Populosas do Piauí", 'most-populated-cities-graph', graph.most_populated_cities())
      ])
  ])

def create_app(url_path, server=None):
    """Cria e retorna o servidor Flask para o app Dash."""
    app = Dash(requests_pathname_prefix=url_path)
    app.title = "Taxa de Alfabetização - Floriano x Piauí x Brasil"

    app.layout = create_layout()

    return app.server
