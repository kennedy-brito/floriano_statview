from dash import html, dcc
from app.dash_apps.layout.components.callbacks import *

def create_city_location_graph_card()-> html.Div:
    """Retorna o card de comparação de zona urbana/rural com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Zona Urbana/Rural - Capitais", id="city-comparison-title"),
            dcc.Dropdown(
                list(city_code_options.keys()), 
                'Teresina - PI', 
                id='city-code-filter',
                className="dropdown"),
            dcc.Graph(id="city-comparison-graph"),
            html.P(id='city-comparison-footnote', className='footnote')
        ]
    )


def get_year_select_card():
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

def create_state_location_graph_card()-> html.Div:
    """Retorna o card de comparação de zona urbana/rural com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Zona Urbana/Rural - Estados", id="state-comparison-title"),
            dcc.Dropdown(
                list(state_code_options.keys()), 
                'Piauí', 
                id='state-code-filter',
                className="dropdown"),
            dcc.Graph(id="state-comparison-graph"),
            html.P(id='state-comparison-footnote', className='footnote')
        ]
    )
   
def create_race_city_graph_card()-> html.Div:
    """Retorna o card de comparação de raça com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Raça - Capitais", id="city-race-comparison-title"),
            dcc.Dropdown(list(city_code_options.keys()), 'Teresina - PI', id='race-city-code-filter', className="dropdown"),
            dcc.Graph(id="city-race-comparison-graph"),
            html.P(id='city-race-comparison-footnote', className='footnote')
        ]
    )

def create_race_state_graph_card()-> html.Div:
    """Retorna o card de comparação de raça com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Raça - Estados", id="state-race-comparison-title"),
            dcc.Dropdown(list(state_code_options.keys()), 'Piauí', id='race-state-code-filter', className="dropdown"),
            dcc.Graph(id="state-race-comparison-graph"),
            html.P(id='state-race-comparison-footnote', className='footnote')
        ]
    )

def create_literacy_tabs_card()-> html.Div:
    """Retorna o card com abas para visualização da taxa de alfabetização."""
    return html.Div(
        children=[
            html.P("Taxa de Alfabetização"),
            dcc.Tabs(
                id="tabs",
                value="tab-1",
                children=[
                    dcc.Tab(
                        label="Floriano",
                        value="tab-1",
                        children=[
                            dcc.Graph(
                                id="literacy-table", 
                                figure=create_literacy_table()
                                )
                            ],
                        ),
                    dcc.Tab(
                        label="Floriano x Piauí x Brasil",
                        value="tab-2",
                        children=[
                            dcc.Graph(
                                id="comparison-literacy",
                                figure=create_comparison_literacy()
                                )
                            ],
                        ),
                    ],
                )
            ,html.P(get_literacy_rate_info() ,id="literacy-rate-footnote", className='footnote')
            ],
        className="graph-card card",
        )

def create_production_graph_card() -> html.Div:
    """Retorna o card de Maiores Produções com filtros de ano e quantidade de maiores produções."""
    return html.Div(
        className="full-width-card graph-card card",
        children=[
            html.P("Maiores Produções Agrícolas", id="production-title"),

            html.Div(
                className="production-controls-container",
                children=[
                    html.Div(
                        className="year-selectors",
                        children=[
                            html.Label("Ano Inicial", htmlFor="ano-inicial"),
                            dcc.Dropdown(
                                id='start-year',
                                options=[{'label': str(ano), 'value': ano} for ano in range(2010, 2024)],
                                value=2010,
                                className="dropdown"
                            ),
                            html.Label("Ano Final", htmlFor="ano-final"),
                            dcc.Dropdown(
                                id='end-year',
                                options=[{'label': str(ano), 'value': ano} for ano in range(2010, 2024)],
                                value=2023,
                                className="dropdown"
                            )
                        ]
                    ),
                    html.Div(
                        className="quantidade-maiores-selector",
                        children=[
                            html.Label("Top N Produções", htmlFor="top-n-producoes"),
                            dcc.Dropdown(
                                id='top-n-producoes',
                                options=[{'label': f'Top {n}', 'value': n} for n in range(1, 11)],
                                value=3,
                                className="dropdown"
                            )
                        ]
                    )
                ]
            ),

            dcc.Graph(id="top_crops_productions_graph"),
            
            html.P(id='crops_footnote',className='footnote alert')
        ]
    )
