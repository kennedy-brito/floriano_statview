import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs import Figure
from . import data_layer as data

def format_pib(value):
    if value >= 1_000_000_000:
        return f"R$ {value / 1_000_000_000:.2f} bi".replace(".", ",")
    elif value >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f} mi".replace(".", ",")
    else:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def age_pyramid()->Figure:
  graph = px.bar(
    data_frame=data.get_age_group(),
    x='valor',
    y='grupo_idade',
    orientation='h')

  return graph

def most_populated_cities()->Figure:
  graph = px.bar(
    data_frame=data.get_top_population_city(),
    x='populacao',
    y='municipio',
    orientation='h',
    )

  graph.update_layout(yaxis=dict(autorange="reversed"))

  return graph

def race_distribution()->Figure:
  graph = px.pie(
    data_frame=data.get_population_by_race(),
    names='raca',
    values='porcentagem'
  )

  return graph

def location_distribution()->Figure:
  graph = px.pie(
    data_frame=data.get_population_by_local(),
    names='local',
    values='porcentagem'
  )

  return graph

def get_metric_total_population():
  return data.get_population_total()['total_populacao']

def get_metric_total_population_info():
  return f"Último Censo: {data.get_population_total()['ano']}"

def get_metric_total_pib():
  value = data.get_total_pib()['total']
  moeda = format_pib(value)
  # moeda = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  return moeda

def get_metric_total_pib_info():
  return f"Último Censo: {data.get_total_pib()['ano']}"

if __name__ == '__main__':
  print(age_pyramid())
  print(most_populated_cities())
  print(race_distribution())
  print(location_distribution())