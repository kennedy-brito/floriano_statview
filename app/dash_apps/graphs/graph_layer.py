import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objs import Figure
from app.dash_apps.data import data_layer as data
import plotly.graph_objects as go

def format_pib_value(value) -> str:
  """
  Formata um valor numérico em reais com notação apropriada
  para bilhões, milhões ou unidades simples.

  Args:
    value (int or float): Valor numérico em reais.

  Returns:
    str: Valor formatado como string, com vírgulas e unidade (R$, mi, bi).
  """
  if value >= 1_000_000_000:
    return f"R$ {value / 1_000_000_000:.2f} bilhões".replace(".", ",")
  elif value >= 1_000_000:
    return f"R$ {value / 1_000_000:.2f} milhões".replace(".", ",")
  else:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def create_age_pyramid(year='last')->Figure:
  """
  Gera um gráfico de pirâmide etária para Floriano baseado no ano informado.

  Args:
    year (str): Ano da consulta (por padrão, 'last' para o mais recente).

  Returns:
    plotly.graph_objs.Figure: Gráfico de barras horizontais com idade versus população.
  """
  graph = px.bar(
    data_frame=data.get_population_age_group(year),
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

def create_most_populated_cities()->Figure:
  """
  Gera um gráfico de barras horizontais com as 10 cidades mais populosas do Piauí.
  Destaca Floriano com uma cor diferente.

  Returns:
    plotly.graph_objs.Figure: Gráfico com população por município.
  """
  df = data.get_top_population_cities()
  
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

def create_race_distribution(level: str = '6', local_code: str = '2203909')->Figure:
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
    data_frame=data.get_population_by_local(level, local_code, year),
    names='local',
    values='porcentagem',
    labels={'local':"Zona", 'porcentagem': "Porcentagem"}
  )

  return graph

def create_literacy_table(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
  df = data.get_literacy_rate(level, local_code, year)
  values = []
  
  for value in df['quantidade']:
    values.append(f"{value:.2f}")
    
  graph = go.Figure(data=[go.Table(
    header=dict(values=["Faixa Etária", "Taxa de Alfabetização (%)"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df['grupo'], values ],
               fill_color='lavender',
               align='left'))
])

  return graph


def create_comparison_literacy():
  """
  Compara graficamente a taxa de alfabetização por faixa etária entre Floriano (PI), o estado do Piauí e o Brasil.

  Esta função utiliza dados da tabela SIDRA sobre a taxa de alfabetismo, gera um gráfico de linha usando Plotly Express
  e retorna a figura. A comparação é feita com base em faixas etárias, e o gráfico permite visualizar as diferenças
  regionais nos níveis de alfabetização.

  Dados utilizados:
      - Floriano: nível territorial 6, código IBGE 2203909
      - Piauí: nível territorial 3, código IBGE 22
      - Brasil: nível territorial 1, código IBGE 1

  Returns:
      plotly.graph_objs._figure.Figure: Objeto de figura contendo o gráfico de linha com os dados de alfabetização.
  """
  floriano_dt = data.get_literacy_rate(level= 6,code=2203909)
    
  piaui_dt = data.get_literacy_rate(level= 3,code=22)
  
  brasil_dt = data.get_literacy_rate(level= 1,code=1)
  
  df = pd.concat(
    [floriano_dt, piaui_dt, brasil_dt],
    ignore_index=True
  )
  
  fig = px.line(
    data_frame=df,
    y="quantidade",
    x="grupo",
    color="local",
    labels={"quantidade": "Taxa de Alfabetização (%)", "grupo": "Faixa Etária", "local": "Localidade"},
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Set2,
  )

  fig.update_layout(
    xaxis=dict(
        
        tickmode='linear',
        dtick=1
    ),
    yaxis=dict(
        range=[50, 100])
  )   
    
  return fig

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
  return data.get_population_total(year)['footnote']

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
    moeda = format_pib_value(value)
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
  return data.get_total_pib(year)['footnote']

def get_metric_pib_per_capita(year='last', format: bool = True):
  """
  Obtém o PIB per capita de Floriano formatado em reais.

  Args:
    year (str): Ano da consulta (padrão 'last').
    format (bool): Se o valor deve ser formatado com notação de milhar/milhão/bilhão

  Returns:
    str: PIB formatado.
  """
  value = data.get_pib_per_capita(year)['pib_per_capita']
  if format:
    moeda = format_pib_value(value)
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
  return data.get_pib_per_capita(year)['footnote']
