import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs import Figure
from . import data_layer as data
import plotly.graph_objects as go

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
    orientation='h',
    labels={'grupo_idade':'Grupo', 'valor': 'População'},
    )

  graph.update_layout(dict(
    font_family='Segoe UI',
    font_weight=700
  ))

  return graph

def most_populated_cities()->Figure:
  df = data.get_top_population_city()
  
  floriano_idx = df[df['municipio'] == "Floriano"].index[0]
  colors = ['#636EFA'] * len(df) #standard blue of plotly
  colors[floriano_idx] = '#EF553B' #standard red of plotly
  
  graph = go.Bar(
    x=df['populacao'],
    y=df['municipio'],
    orientation='h',
    marker_color=colors
    )
  

  fig = go.Figure(data=[
    graph    
  ])
  
  fig.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis_title="População",
  
    font_family='Segoe UI',
    font_weight=600,
    yaxis_title="Município")
  
  return fig

def race_distribution()->Figure:
  graph = px.pie(
    data_frame=data.get_population_by_race(),
    names='raca',
    values='porcentagem',
    labels={'raca':"Raça", 'porcentagem': "Porcentagem"}
  )

  return graph

def location_distribution()->Figure:
  graph = px.pie(
    data_frame=data.get_population_by_local(),
    names='local',
    values='porcentagem',
    labels={'local':"Zona", 'porcentagem': "Porcentagem"}
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