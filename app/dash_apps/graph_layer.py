import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs import Figure
from . import data_layer as data

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

if __name__ == '__main__':
  print(age_pyramid())
  print(most_populated_cities())
  print(race_distribution())
  print(location_distribution())