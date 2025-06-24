from dash import html, dcc
from app.dash_apps.layout.components.callbacks import *

def create_graph_card_with_dropdown(
    title: str,
    options: list,
    default_value: str,
    dropdown_id: str,
    graph_id: str,
    footnote_id: str
) -> html.Div:
    """Cria um card de gráfico com dropdown interativo e rodapé."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P(title, id=f"{graph_id}-title"),
            dcc.Dropdown(
                options,
                default_value,
                id=dropdown_id,
                className="dropdown"
            ),
            dcc.Graph(id=graph_id),
            html.P(id=footnote_id, className='footnote')
        ]
    )

def create_year_select_card():
    return html.Div(
        children=[
            html.P("Selecione o ano dos dados:"),
            dcc.Dropdown(
                list(years), 
                'Mais Recente', 
                id='year-filter',
                className="dropdown"
            ),
            html.P("Algumas informações podem não estar disponíveis para todos os anos.", className='footnote')
        ], className='year-select-card card'
    )

def create_metric_card(title: str, value_id, footnote_id) -> html.Div:
  """Retorna um card de métrica simples."""
  return html.Div(
      className="metric-card card",
      children=[
          html.P(title),
          html.H3(id=value_id),
          html.P(id=footnote_id, className='footnote')
      ]
  )

def create_graph_card(title: str, graph_id: str, footnote_id) -> html.Div:
  """Retorna um card contendo um gráfico."""
  return html.Div(
      className="graph-card card",
      children=[
          html.P(title),
          dcc.Graph(id=graph_id),
          html.P(id=footnote_id, className='footnote')
      ]
  )
