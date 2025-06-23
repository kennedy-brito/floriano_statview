import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import plotly.graph_objects as go

from app.dash_apps.data import education as educ
from app.dash_apps.graphs.constants import *

def create_literacy_table(level: str = '6', local_code: str = '2203909', year: str = 'last')->Figure:
  df = educ.get_literacy_rate(level, local_code, year)
  values = []
  
  for value in df['quantidade']:
    values.append(f"{value:.2f}")
    
  graph = go.Figure(
    data=[
      go.Table(
        header=dict(
          values=["Faixa Etária", "Taxa de Alfabetização (%)"],
          fill_color='#A2D8F4',  # Azul suave
          align='left',
          font=dict(color='#2B5C7B')  # Azul escuro
          ),
        cells=dict(
          values=[df['grupo'], values],
          fill_color='lavender',  # Lavanda suave
          align='left',
          font=dict(color='#4A4A4A')  # Texto cinza escuro para melhor legibilidade
          )
        )
      ]
    )

  graph.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  )
  return graph

def create_comparison_literacy(year='last'):
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
  floriano_dt = educ.get_literacy_rate(level= 6,code=2203909, year=year)
    
  piaui_dt = educ.get_literacy_rate(level= 3,code=22, year=year)
  
  brasil_dt = educ.get_literacy_rate(level= 1,code=1, year=year)
  
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
    color_discrete_sequence=COLOR_PALETTE,
  )

  fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        dtick=1
        ),
    yaxis=dict(
        range=[50, 100]
        ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  
  )   
    
  return fig

def get_literacy_rate_info(year='last'):
  floriano_dt = educ.get_literacy_rate(level= 6,code=2203909, year=year)
  return floriano_dt.iloc[0]['footnote']

