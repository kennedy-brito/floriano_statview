import plotly.express as px
from plotly.graph_objs import Figure
from app.dash_apps.data import population as pop
import plotly.graph_objects as go
from app.dash_apps.graphs.constants import *

def create_age_pyramid(year='last')->Figure:
  """
  Gera um gráfico de pirâmide etária para Floriano baseado no ano informado.

  Args:
    year (str): Ano da consulta (por padrão, 'last' para o mais recente).

  Returns:
    plotly.graph_objs.Figure: Gráfico de barras horizontais com idade versus população.
  """
  graph = px.bar(
    data_frame= pop.get_population_age_group(year),
    x='valor',
    y='grupo_idade',
    orientation='h',
    labels={'grupo_idade':'Grupo', 'valor': 'População'},
    color_discrete_sequence=COLOR_PALETTE,
    )

  graph.update_layout(dict(
    font_family='Segoe UI',
    font_weight=700,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  ))

  return graph

def get_age_pyramid_info(year='last'):
  
  df = pop.get_population_age_group(year)
  return df.iloc[0]['footnote']

def create_most_populated_cities(year='last')->Figure:
  """
  Gera um gráfico de barras horizontais com as 10 cidades mais populosas do Piauí.
  Destaca Floriano com uma cor diferente.

  Returns:
    plotly.graph_objs.Figure: Gráfico com população por município.
  """
  df = pop.get_top_population_cities(year)
  
  floriano_idx = df[df['municipio'] == "Floriano"].index[0]
  colors = [COLOR_PALETTE[0],] * len(df) 
  colors[floriano_idx] = COLOR_PALETTE[3]
  
  graph = go.Bar(
    x=df['populacao'],
    y=df['municipio'],
    orientation='h',
    marker_color=colors,
    hovertemplate=(
      'População: %{x:,}<br>'  
      'Cidade: %{y}<extra></extra>'  
      )
    )
  

  fig = go.Figure(data=[
    graph    
  ])
  
  fig.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis_title="População",
  
    font_family='Segoe UI',
    font_weight=600,
    yaxis_title="Município",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    )
  
  return fig

def get_most_populated_cities_info(year='last'):
  df = pop.get_top_population_cities(year)
  return df.iloc[0]['footnote']

def create_race_distribution(level: str = '6', local_code: str = '2203909', year='last')->Figure:
  """
  Gera um gráfico de pizza com a distribuição racial da população de Floriano.

  Args:
    level (str): Nível territorial (padrão '6' para município).
    local_code (str): Código IBGE do município (padrão Floriano: '2203909').

  Returns:
    plotly.graph_objs.Figure: Gráfico de pizza com porcentagem por raça.
  """
  df = pop.get_population_by_race(level, local_code, year).sort_values(ascending=True,by=['porcentagem'])
  
  formatted_values = [f"{v:.2f}" for v in df['porcentagem']]
  graph = px.bar(
    data_frame=df,
    y='raca',
    x='porcentagem',
    orientation='h',
    labels={'raca':"Raça", 'porcentagem': "Porcentagem"},
    text=formatted_values,
    color_discrete_sequence=COLOR_PALETTE,
  )

  graph.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  )
  
  return graph

def get_race_distribution_info(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
  distribuition = pop.get_population_by_race(level, local_code, year)

  return distribuition.iloc[0]['footnote']

def get_location_distribution_info(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
  distribuition = pop.get_population_by_race(level, local_code, year)

  return distribuition.iloc[0]['footnote']

def create_location_distribution(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
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
    data_frame=pop.get_population_by_local(level, local_code, year),
    names='local',
    values='porcentagem',
    labels={'local':"Zona", 'porcentagem': "Porcentagem"},
    color_discrete_sequence=COLOR_PALETTE,
  )
  
  graph.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  )

  return graph

def get_location_distribution_info(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
  """
  Gera um gráfico de pizza com a distribuição da população entre zonas urbanas e rurais.

  Args:
    level (str): Nível territorial (padrão '6' para município).
    local_code (str): Código IBGE do município.
    year (str): Ano da consulta (padrão 'last' para o mais recente).

  Returns:
    plotly.graph_objs.Figure: Gráfico de pizza com porcentagem por zona (urbana/rural).
  """
  distribuition = pop.get_population_by_local(level, local_code, year)

  return distribuition.iloc[0]['footnote']


def get_metric_total_population(year='last'):
  """
  Obtém a população total de Floriano para o ano especificado.

  Args:
    year (str): Ano da consulta (padrão 'last').

  Returns:
    int: População total.
  """
  return pop.get_population_total(year=year)['total_populacao']

def get_metric_total_population_info(year='last'):
  """
  Retorna o ano de referência da população total consultada.

  Args:
    year (str): Ano da consulta (padrão 'last').

  Returns:
    str: Texto com o ano do censo usado.
  """
  return pop.get_population_total(year=year)['footnote']
