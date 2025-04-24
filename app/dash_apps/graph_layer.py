import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs import Figure
from . import data_layer as data
import plotly.graph_objects as go

def format_pib(value) -> str:
  """
  Formata um valor numérico em reais com notação apropriada
  para bilhões, milhões ou unidades simples.

  Args:
    value (int or float): Valor numérico em reais.

  Returns:
    str: Valor formatado como string, com vírgulas e unidade (R$, mi, bi).
  """
  if value >= 1_000_000_000:
    return f"R$ {value / 1_000_000_000:.2f} bi".replace(".", ",")
  elif value >= 1_000_000:
    return f"R$ {value / 1_000_000:.2f} mi".replace(".", ",")
  else:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def age_pyramid(year='last')->Figure:
  """
  Gera um gráfico de pirâmide etária para Floriano baseado no ano informado.

  Args:
    year (str): Ano da consulta (por padrão, 'last' para o mais recente).

  Returns:
    plotly.graph_objs.Figure: Gráfico de barras horizontais com idade versus população.
  """
  graph = px.bar(
    data_frame=data.get_age_group(year),
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
  """
  Gera um gráfico de barras horizontais com as 10 cidades mais populosas do Piauí.
  Destaca Floriano com uma cor diferente.

  Returns:
    plotly.graph_objs.Figure: Gráfico com população por município.
  """
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

def race_distribution(level: str = '6', local_code: str = '2203909')->Figure:
  """
  Gera um gráfico de pizza com a distribuição racial da população de Floriano.

  Args:
    level (str): Nível territorial (padrão '6' para município).
    local_code (str): Código IBGE do município (padrão Floriano: '2203909').

  Returns:
    plotly.graph_objs.Figure: Gráfico de pizza com porcentagem por raça.
  """
  graph = px.pie(
    data_frame=data.get_population_by_race(level, local_code),
    names='raca',
    values='porcentagem',
    labels={'raca':"Raça", 'porcentagem': "Porcentagem"}
  )

  return graph

def location_distribution(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
  """
  Gera um gráfico de pizza com a distribuição da população entre zonas urbanas e rurais.

  Args:
    level (str): Nível territorial (padrão '6' para município).
    local_code (str): Código IBGE do município.
    year (str): Ano da consulta (padrão 'last' para o mais recente).

  Returns:
    plotly.graph_objs.Figure: Gráfico de pizza com porcentagem por zona (urbana/rural).
  """
  graph = px.pie(
    data_frame=data.get_population_by_local(level, local_code, year),
    names='local',
    values='porcentagem',
    labels={'local':"Zona", 'porcentagem': "Porcentagem"}
  )

  return graph

def get_metric_total_population(year='last'):
  """
  Obtém a população total de Floriano para o ano especificado.

  Args:
    year (str): Ano da consulta (padrão 'last').

  Returns:
    int: População total.
  """
  return data.get_population_total(year)['total_populacao']

def get_metric_total_population_info(year='last'):
  """
  Retorna o ano de referência da população total consultada.

  Args:
    year (str): Ano da consulta (padrão 'last').

  Returns:
    str: Texto com o ano do censo usado.
  """
  return f"Censo: {data.get_population_total(year)['ano']}"

def get_metric_total_pib(year='last', format: bool = True):
  """
  Obtém o PIB total de Floriano formatado em reais.

  Args:
    year (str): Ano da consulta (padrão 'last').
    format (bool): Se o valor deve ser formatado com notação de milhar/milhão/bilhão

  Returns:
    str: PIB formatado.
  """
  value = data.get_total_pib(year)['total']
  if format:
    moeda = format_pib(value)
  else: 
    moeda = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  return moeda

def get_metric_total_pib_info(year='last'):
  """
  Retorna o ano de referência do PIB consultado.

  Args:
    year (str): Ano da consulta (padrão 'last').

  Returns:
    str: Texto com o ano do censo usado para o PIB.
  """
  return f"Censo: {data.get_total_pib(year)['ano']}"

def get_metric_pib_per_capita(year='last', format: bool = True):
  """
  Obtém o PIB per capita de Floriano formatado em reais.

  Args:
    year (str): Ano da consulta (padrão 'last').
    format (bool): Se o valor deve ser formatado com notação de milhar/milhão/bilhão

  Returns:
    str: PIB formatado.
  """
  value = data.get_pib_per_capita(year)['pib_per_capita'].item()
  if format:
    moeda = format_pib(value)
  else: 
    moeda = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  return moeda

def get_metric_pib_per_capita_info(year='last'):
  """
  Retorna o ano de referência do PIB consultado.

  Args:
    year (str): Ano da consulta (padrão 'last').

  Returns:
    str: Texto com o ano do censo usado para o PIB.
  """
  return f"Censo: {data.get_pib_per_capita(year)['ano']}"
