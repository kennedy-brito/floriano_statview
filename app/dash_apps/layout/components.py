
from dash import html, dcc, callback, Output, Input
from app.dash_apps.graphs import graph_layer as graph

code_level_options = {
    'Piauí':{'level': '3', 'code':'22'},
    'São Paulo - SP': {'level': 6, 'code': '3550308'}
}

years = ['Mais Recente'] + [i for i in range(2010,2026)] 

def get_year_select_card():
    return dcc.Dropdown(
        list(years), 
        'Piauí', 
        id='year-filter',
        className="dropdown"
    )

def create_metric_card(title: str, value: str, footnote: str = None) -> html.Div:
  """Retorna um card de métrica simples."""
  return html.Div(
      className="metric-card card",
      children=[
          html.P(title),
          html.H3(value),
          html.P(footnote, className='footnote') if footnote else None
      ]
  )


def create_graph_card(title: str, graph_id: str, figure) -> html.Div:
  """Retorna um card contendo um gráfico."""
  return html.Div(
      className="graph-card card",
      children=[
          html.P(title),
          dcc.Graph(id=graph_id, figure=figure)
      ]
  )

@callback(
    Output('location-comparison-graph', 'figure'),
    Input('local-code-filter', 'value'),
)
def update_location_interactive(location_key)-> dict:
    """Atualiza o gráfico de distribuição urbana/rural baseado na localização selecionada."""
    location= code_level_options[location_key]
    return graph.create_location_distribution(level=location['level'], local_code=location['code'])
  
def create_location_graph_card()-> html.Div:
    """Retorna o card de comparação de zona urbana/rural com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Zona Urbana/Rural - Outros Locais", id="location-comparison-title"),
            dcc.Dropdown(
                list(code_level_options.keys()), 
                'Piauí', 
                id='local-code-filter',
                className="dropdown"),
            dcc.Graph(id="location-comparison-graph")
        ]
    )
    

@callback(
    Output('race-comparison-graph', 'figure'),
    Input('race-code-filter', 'value'),
)
def update_race_interactive(location_key):
    """Atualiza o gráfico de distribuição racial baseado na localização selecionada."""
    location= code_level_options[location_key]
    return graph.create_race_distribution(level=location['level'], local_code=location['code'])

def create_race_graph_card()-> html.Div:
    """Retorna o card de comparação de raça com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Raça", id="race-comparison-title"),
            dcc.Dropdown(list(code_level_options.keys()), 'Piauí', id='race-code-filter', className="dropdown"),
            dcc.Graph(id="race-comparison-graph")
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
                                figure=graph.create_literacy_table()
                                )
                            ],
                        ),
                    dcc.Tab(
                        label="Floriano x Piauí x Brasil",
                        value="tab-2",
                        children=[
                            dcc.Graph(
                                id="comparison-literacy",
                                figure=graph.create_comparison_literacy()
                                )
                            ],
                        ),
                    ],
                )
            ],
        className="graph-card card",
        )