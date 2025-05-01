
from dash import html, dcc, callback, Output, Input
from app.dash_apps.graphs import graph_layer as graph

city_code_options = {
    'São Paulo': {'level': 6, 'code': '3550308'},
    'Teresina': {'level': 6, 'code': '2211001'}
}

top_productions_slider = dcc.Slider(
    id="top-productions",
    min=1,
    max=10,
    step=1,
    value=3,
    marks={i: str(i) for i in range(1, 11)}
)

year_range_slider = dcc.RangeSlider(
    value=[2010, 2025],
    min=2010,
    max=2025,
    step=1,
    marks={i: str(i) for i in range(2010, 2026, 2)},
    id="year-slider"
)

state_code_options = {
    'Piauí':{'level': '3', 'code':'22'},
    'São Paulo':{'level': '3', 'code': '35'}
}

years = ['Mais Recente'] + [str(i) for i in range(2010,2026)] 

outputs_mapping_graphs = {
    "total_population_metric": graph.get_metric_total_population,
    "total_pib_metric": graph.get_metric_total_pib,
    "pib_per_capita_metric": graph.get_metric_pib_per_capita,
    'location-distribution-graph': graph.create_location_distribution,
    'age-pyramid-graph': graph.create_age_pyramid,
    'race-distribution-graph': graph.create_race_distribution,
    'most-populated-cities-graph': graph.create_most_populated_cities
}

outputs_mapping_infos = {
    "total_population_footnote": graph.get_metric_total_population_info,
    "total_pib_footnote": graph.get_metric_total_pib_info,
    "pib_per_capita_footnote": graph.get_metric_pib_per_capita_info,
    'location-distribution-footnote': graph.get_location_distribution_info,
    'age-pyramid-footnote': graph.get_age_pyramid_info,
    'race-distribution-footnote': graph.get_race_distribution_info,
    'most-populated-cities-footnote': graph.get_most_populated_cities_info
}

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

@callback(
    [Output(component_id, 'figure' if 'graph' in component_id else 'children') for component_id in outputs_mapping_graphs.keys()],
    Input("year-filter", 'value')
)
def update_all_graphs(year):
    year = 'last' if year=='Mais Recente' else year
    return [func(year=year) for func in outputs_mapping_graphs.values()]


@callback(
    [Output(component_id, 'children') for component_id in outputs_mapping_infos.keys()],
    Input("year-filter", 'value')
)
def update_all_footnotes(year):
    year = 'last' if year=='Mais Recente' else year
    return [func(year=year) for func in outputs_mapping_infos.values()]


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

@callback(
    Output('city-comparison-graph', 'figure'),
    Output('city-comparison-footnote', 'children'),
    Input('city-code-filter', 'value'),
)
def update_city_location_interactive(location_key)-> dict:
    """Atualiza o gráfico de distribuição urbana/rural baseado na localização selecionada."""
    location= city_code_options[location_key]
    return [
        graph.create_location_distribution(level=location['level'], local_code=location['code']),
        graph.get_location_distribution_info(level=location['level'], local_code=location['code'])]
  
def create_city_location_graph_card()-> html.Div:
    """Retorna o card de comparação de zona urbana/rural com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Zona Urbana/Rural - Capitais", id="city-comparison-title"),
            dcc.Dropdown(
                list(city_code_options.keys()), 
                'Teresina', 
                id='city-code-filter',
                className="dropdown"),
            dcc.Graph(id="city-comparison-graph"),
            html.P(id='city-comparison-footnote', className='footnote')
        ]
    )

@callback(
    Output('state-comparison-graph', 'figure'),
    Output('state-comparison-footnote', 'children'),
    Input('state-code-filter', 'value'),
)
def update_state_location_interactive(location_key)-> dict:
    """Atualiza o gráfico de distribuição urbana/rural baseado na localização selecionada."""
    location= state_code_options[location_key]
    return [
        graph.create_location_distribution(level=location['level'], local_code=location['code']),
        graph.get_location_distribution_info(level=location['level'], local_code=location['code'])]
  
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
    

@callback(
    Output('city-race-comparison-graph', 'figure'),
    Output('city-race-comparison-footnote', 'children'),
    Input('race-city-code-filter', 'value'),
    Input('year-filter', 'value')
)
def update_race_city_interactive(location_key, year):
    """Atualiza o gráfico de distribuição racial baseado na localização selecionada."""
    
    year = 'last' if year == 'Mais Recente' else year
    
    location= city_code_options[location_key]
    return [
        graph.create_race_distribution(level=location['level'], local_code=location['code'], year=year),
        graph.get_race_distribution_info(level=location['level'], local_code=location['code'], year=year)]

def create_race_city_graph_card()-> html.Div:
    """Retorna o card de comparação de raça com dropdown interativo."""
    return html.Div(
        className="graph-card card",
        children=[
            html.P("Distribuição da População por Raça - Capitais", id="city-race-comparison-title"),
            dcc.Dropdown(list(city_code_options.keys()), 'Teresina', id='race-city-code-filter', className="dropdown"),
            dcc.Graph(id="city-race-comparison-graph"),
            html.P(id='city-race-comparison-footnote', className='footnote')
        ]
    )


@callback(
    Output('state-race-comparison-graph', 'figure'),
    Output('state-race-comparison-footnote', 'children'),
    Input('race-state-code-filter', 'value'),
    Input('year-filter', 'value')
)
def update_race_state_interactive(location_key, year):
    """Atualiza o gráfico de distribuição racial baseado na localização selecionada."""
    
    year = 'last' if year == 'Mais Recente' else year
    
    location= state_code_options[location_key]
    return [
        graph.create_race_distribution(level=location['level'], local_code=location['code'], year=year),
        graph.get_race_distribution_info(level=location['level'], local_code=location['code'], year=year)]

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
            ,html.P(graph.get_literacy_rate_info() ,id="literacy-rate-footnote", className='footnote')
            ],
        className="graph-card card",
        )

@callback(
    Output('top_crops_productions_graph', 'figure'),
    Output('crops_footnote', 'children'),
    Input('start-year', 'value'),
    Input('end-year', 'value'),
    Input('top-n-producoes', 'value')
)
def update_top_crops_graph(start_year, end_year, top_crops):
    footnote = ''
    
    if start_year > end_year:
        start_year, end_year = end_year, start_year
        footnote = f"O intervalo foi ajustado automaticamente para {start_year}–{end_year}."
    
    top_crops_graph = graph.create_top_crops(start_year=start_year, end_year= end_year, top_crops=top_crops)
    
    return [top_crops_graph, footnote]

def create_production_graph_card() -> html.Div:
    """Retorna o card de Maiores Produções com filtros de ano e quantidade de maiores produções."""
    return html.Div(
        className="full-width-card graph-card card",
        children=[
            html.P("Maiores Produções", id="production-title"),

            html.Div(
                className="production-controls-container",
                children=[
                    html.Div(
                        className="year-selectors",
                        children=[
                            html.Label("Ano Inicial", htmlFor="ano-inicial"),
                            dcc.Dropdown(
                                id='start-year',
                                options=[{'label': str(ano), 'value': ano} for ano in range(2010, 2026)],
                                value=2010,
                                className="dropdown"
                            ),
                            html.Label("Ano Final", htmlFor="ano-final"),
                            dcc.Dropdown(
                                id='end-year',
                                options=[{'label': str(ano), 'value': ano} for ano in range(2010, 2026)],
                                value=2025,
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