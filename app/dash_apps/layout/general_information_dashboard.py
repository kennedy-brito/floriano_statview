from dash import Dash, html
from flask import Flask
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
          comp.get_year_select_card()
          ], className="year-select"),
        html.Div([
            comp.create_metric_card("População Total", "total_population_metric", "total_population_footnote"),
            # comp.create_metric_card("PIB de Floriano", graph.get_metric_total_pib(), graph.get_metric_total_pib_info()),
            # comp.create_metric_card("PIB Per Capita de Floriano", graph.get_metric_pib_per_capita(), graph.get_metric_pib_per_capita_info()),
          
          ], className='metric-row row'),
        
        html.Div([
            # comp.create_graph_card("Distribuição da População por Zona Urbana/Rural - Floriano", 'location-distribution-graph', graph.create_location_distribution()),
            # comp.create_location_graph_card(),
            # comp.create_graph_card("Faixa Etária da Cidade", 'age-pyramid-graph', graph.create_age_pyramid()),
          
          ], className='metric-row row'),
          
        html.Div([
            # comp.create_graph_card("Distribuição da População por Raça - Floriano", 'race-distribution-graph', graph.create_race_distribution()),
            # comp.create_race_graph_card(),
            # comp.create_graph_card("Cidades Mais Populosas do Piauí", 'most-populated-cities-graph', graph.create_most_populated_cities()),
          ], className='metric-row row'
        ),
        
        html.Div([
            # comp.create_literacy_tabs_card()
          ], className='metric-row row'
        )
      ])
  ])

def create_app(url_path: str, server: Flask=None):
  """Cria e retorna o servidor Flask para o app Dash."""
  app = Dash(requests_pathname_prefix=url_path)
  app.title = "Taxa de Alfabetização - Floriano x Piauí x Brasil"

  app.layout = create_layout()

  return app.server
