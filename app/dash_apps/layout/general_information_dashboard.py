from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd
from app.dash_apps.graphs import graph_layer as graph
from . import components as comp

def create_layout():
  """Cria o layout do aplicativo Dash."""
  return html.Div([
      html.Header([
          html.H1('Floriano StatView - Informações Gerais')
      ]),
      html.Main(id='content', children=[
        
        html.Div([
            comp.card_metric("População Total", graph.get_metric_total_population(), graph.get_metric_total_population_info()),
            comp.card_metric("PIB de Floriano", graph.get_metric_total_pib(), graph.get_metric_total_pib_info()),
            comp.card_metric("PIB Per Capita de Floriano", graph.get_metric_pib_per_capita(), graph.get_metric_pib_per_capita_info()),
          
          ], className='metric-row row'),
        
        html.Div([
            comp.card_graph("Distribuição da População por Zona - Floriano", 'location-distribution-graph', graph.location_distribution()),
            comp.card_graph_location_interative(),
            comp.card_graph("Faixa Etária da Cidade", 'age-pyramid-graph', graph.age_pyramid()),
          
          ], className='metric-row row'),
          
        html.Div([
            comp.card_graph("Distribuição da População por Raça - Floriano", 'race-distribution-graph', graph.race_distribution()),
            comp.card_graph_race_interative(),
            comp.card_graph("Cidades Mais Populosas do Piauí", 'most-populated-cities-graph', graph.most_populated_cities()),
          ], className='metric-row row'
        ),
        
        html.Div([
            comp.card_graph("Taxa de Alfabetização - Brasil x Piauí x Floriano", 'comparison-literacy-graph', graph.comparison_population_literacy())
          ], className='metric-row row'
        )
      ])
  ])

def create_app(url_path, server=None):
  """Cria e retorna o servidor Flask para o app Dash."""
  app = Dash(requests_pathname_prefix=url_path)
  app.title = "Taxa de Alfabetização - Floriano x Piauí x Brasil"

  app.layout = create_layout()

  return app.server
