import plotly.express as px
from app.dash_apps.data import economy as econ
from app.dash_apps.graphs.utils import format_pib_value
from app.dash_apps.graphs.constants import *

def get_metric_total_pib(year='last', format: bool = True):
  """
  Obtém o PIB total de Floriano formatado em reais.

  Args:
    year (str): Ano da consulta (padrão 'last').
    format (bool): Se o valor deve ser formatado com notação de milhar/milhão/bilhão

  Returns:
    str: PIB formatado.
  """
  value = econ.get_total_pib(year)['total']
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
  return econ.get_total_pib(year)['footnote']

def get_metric_pib_per_capita(year='last', format: bool = True):
  """
  Obtém o PIB per capita de Floriano formatado em reais.

  Args:
    year (str): Ano da consulta (padrão 'last').
    format (bool): Se o valor deve ser formatado com notação de milhar/milhão/bilhão

  Returns:
    str: PIB formatado.
  """
  value = econ.get_pib_per_capita(year)['pib_per_capita']
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
  return econ.get_pib_per_capita(year)['footnote']

def create_top_crops(level="6",local_code="2203909", start_year=2010, end_year=2025, top_crops=3):
  top_crops = econ.get_crop_production(level, local_code, start_year, end_year, top_crops)
  fig = None
  
  if start_year < end_year:  
    fig = px.bar(
      data_frame=top_crops,
      y="quantidade",
      x="ano",
      text="quantidade",
      labels={'ano': 'Ano', 'quantidade': 'Produção em Toneladas', 'produto': 'Cultura'},
      orientation="v",
      color="produto",
      category_orders={'produto': CROPS_COLOR_PALETTE.keys()},
      color_discrete_map=CROPS_COLOR_PALETTE,
    )
  elif start_year == end_year:
    fig = px.bar(
      data_frame=top_crops,
      y="quantidade",
      x="produto",
      text="quantidade",
      labels={'produto': 'Cultura', 'quantidade': 'Produção em Toneladas'},
      orientation="v",
      color="produto",
      category_orders={'produto': CROPS_COLOR_PALETTE.keys()},
      color_discrete_map=CROPS_COLOR_PALETTE,
    )
  
  fig.update_layout(  
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  )

  return fig
