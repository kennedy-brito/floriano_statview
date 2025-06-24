from dash import Dash, html
from flask import Flask
from app.dash_apps.layout.components import generic_cards as g_card, specific_cards as s_card 

def create_layout():
  """Cria o layout do aplicativo Dash."""
  return html.Div([
      html.Header([
          html.H1('Floriano StatView - Informações Gerais')
      ]),
      html.Main(id='content', children=[
        html.Div([
          g_card.create_year_select_card()
          ], className="year-select"),
        html.Div([
            g_card.create_metric_card("População Total", "total_population_metric", "total_population_footnote"),
            g_card.create_metric_card("PIB de Floriano", "total_pib_metric", "total_pib_footnote"),
            g_card.create_metric_card("PIB Per Capita de Floriano", "pib_per_capita_metric", "pib_per_capita_footnote"),
          
          ], className='metric-row row'),
        
        html.Div([
            g_card.create_graph_card("Distribuição da População por Zona Urbana/Rural - Floriano", 'location-distribution-graph', "location-distribution-footnote"),
            s_card.create_city_location_graph_card(),
            s_card.create_state_location_graph_card(),
          
          ], className='metric-row row'),
          
        html.Div([
            g_card.create_graph_card("Distribuição da População por Raça - Floriano", 'race-distribution-graph', 'race-distribution-footnote'),
            s_card.create_race_city_graph_card(),
            s_card.create_race_state_graph_card(),
            
          ], className='metric-row row'
        ),
        
        html.Div([
            s_card.create_literacy_tabs_card(),
            g_card.create_graph_card("Cidades Mais Populosas do Piauí", 'most-populated-cities-graph', 'most-populated-cities-footnote'),
            g_card.create_graph_card("Faixa Etária da Cidade", 'age-pyramid-graph', 'age-pyramid-footnote'),
          ], className='metric-row row'
        ),
        html.Div([
            s_card.create_production_graph_card(),
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
