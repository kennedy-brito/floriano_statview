
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd
from . import graph_layer as graph

code_level_options = {
    'Piauí':{'level': '3', 'code':'22'},
    'São Paulo - SP': {'level': 6, 'code': '3550308'}
}

def card_metric(title: str, value: str, footnote: str = None):
  return html.Div(
      className="metric-card card",
      children=[
          html.P(title),
          html.H3(value),
          html.P(footnote, className='footnote')
      ]
  )


def card_graph(title: str, graph_id: str, figure):
  return html.Div(
      className="graph-card card",
      children=[
          html.P(title),
          dcc.Graph(id=graph_id, figure=figure)
      ]
  )

@callback(
    Output('location-comparison-graph', 'figure'),
    Input('local-code-filter', 'value'),
)
def update_location_interative(location_key):
    location= code_level_options[location_key]
    return graph.location_distribution(level=location['level'], local_code=location['code'])
  
def card_graph_location_interative():
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Zona", id="location-comparison-title"),
            dcc.Dropdown(list(code_level_options.keys()), 'Piauí', id='local-code-filter'),
            dcc.Graph(id="location-comparison-graph")
        ]
    )
    

@callback(
    Output('race-comparison-graph', 'figure'),
    Input('race-code-filter', 'value'),
)
def update_race_interative(location_key):
    location= code_level_options[location_key]
    return graph.race_distribution(level=location['level'], local_code=location['code'])

def card_graph_race_interative():
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Raça", id="race-comparison-title"),
            dcc.Dropdown(list(code_level_options.keys()), 'Piauí', id='race-code-filter'),
            dcc.Graph(id="race-comparison-graph")
        ]
    )