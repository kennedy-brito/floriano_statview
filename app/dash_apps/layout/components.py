
from dash import html, dcc, callback, Output, Input
from app.dash_apps.graphs.education import *
from app.dash_apps.graphs.demographics import *
from app.dash_apps.graphs.economy import *

city_code_options = {
    'Rio Branco - AC': {'level': 6, 'code': '1200401'},
    'Macapá - AP': {'level': 6, 'code': '1600303'},
    'Manaus - AM': {'level': 6, 'code': '1302603'},
    'Belém - PA': {'level': 6, 'code': '1501402'},
    'Porto Velho - RO': {'level': 6, 'code': '1100205'},
    'Boa Vista - RR': {'level': 6, 'code': '1400100'},
    'Palmas - TO': {'level': 6, 'code': '1721000'},
    'Maceió - AL': {'level': 6, 'code': '2704302'},
    'Salvador - BA': {'level': 6, 'code': '2927408'},
    'Fortaleza - CE': {'level': 6, 'code': '2304400'},
    'São Luís - MA': {'level': 6, 'code': '2111300'},
    'João Pessoa - PB': {'level': 6, 'code': '2507507'},
    'Recife - PE': {'level': 6, 'code': '2611606'},
    'Teresina - PI': {'level': 6, 'code': '2211001'},
    'Natal - RN': {'level': 6, 'code': '2408102'},
    'Aracaju - SE': {'level': 6, 'code': '2800308'},
    'Goiânia - GO': {'level': 6, 'code': '5208707'},
    'Cuiabá - MT': {'level': 6, 'code': '5103403'},
    'Campo Grande - MS': {'level': 6, 'code': '5002704'},
    'Brasília - DF': {'level': 6, 'code': '5300108'},
    'Vitória - ES': {'level': 6, 'code': '3205309'},
    'Belo Horizonte - MG': {'level': 6, 'code': '3106200'},
    'Rio de Janeiro - RJ': {'level': 6, 'code': '3304557'},
    'São Paulo - SP': {'level': 6, 'code': '3550308'},
    'Curitiba - PR': {'level': 6, 'code': '4106902'},
    'Porto Alegre - RS': {'level': 6, 'code': '4314902'},
    'Florianópolis - SC': {'level': 6, 'code': '4205407'}
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
    'Acre': {'level': '3', 'code': '12'},
    'Alagoas': {'level': '3', 'code': '27'},
    'Amapá': {'level': '3', 'code': '16'},
    'Amazonas': {'level': '3', 'code': '13'},
    'Bahia': {'level': '3', 'code': '29'},
    'Ceará': {'level': '3', 'code': '23'},
    'Distrito Federal': {'level': '3', 'code': '53'},
    'Espírito Santo': {'level': '3', 'code': '32'},
    'Goiás': {'level': '3', 'code': '52'},
    'Maranhão': {'level': '3', 'code': '21'},
    'Mato Grosso': {'level': '3', 'code': '51'},
    'Mato Grosso do Sul': {'level': '3', 'code': '50'},
    'Minas Gerais': {'level': '3', 'code': '31'},
    'Pará': {'level': '3', 'code': '15'},
    'Paraíba': {'level': '3', 'code': '25'},
    'Paraná': {'level': '3', 'code': '41'},
    'Pernambuco': {'level': '3', 'code': '26'},
    'Piauí': {'level': '3', 'code': '22'},
    'Rio de Janeiro': {'level': '3', 'code': '33'},
    'Rio Grande do Norte': {'level': '3', 'code': '24'},
    'Rio Grande do Sul': {'level': '3', 'code': '43'},
    'Rondônia': {'level': '3', 'code': '11'},
    'Roraima': {'level': '3', 'code': '14'},
    'Santa Catarina': {'level': '3', 'code': '42'},
    'São Paulo': {'level': '3', 'code': '35'},
    'Sergipe': {'level': '3', 'code': '28'},
    'Tocantins': {'level': '3', 'code': '17'}
}

years = ['Mais Recente'] + [str(i) for i in range(2010,2026)] 

outputs_mapping_graphs = {
    "total_population_metric": get_metric_total_population,
    "total_pib_metric": get_metric_total_pib,
    "pib_per_capita_metric": get_metric_pib_per_capita,
    'location-distribution-graph': create_location_distribution,
    'age-pyramid-graph': create_age_pyramid,
    'race-distribution-graph': create_race_distribution,
    'most-populated-cities-graph': create_most_populated_cities
}

outputs_mapping_infos = {
    "total_population_footnote": get_metric_total_population_info,
    "total_pib_footnote": get_metric_total_pib_info,
    "pib_per_capita_footnote": get_metric_pib_per_capita_info,
    'location-distribution-footnote': get_location_distribution_info,
    'age-pyramid-footnote': get_age_pyramid_info,
    'race-distribution-footnote': get_race_distribution_info,
    'most-populated-cities-footnote': get_most_populated_cities_info
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
        create_location_distribution(level=location['level'], local_code=location['code']),
        get_location_distribution_info(level=location['level'], local_code=location['code'])]
  
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

@callback(
    Output('state-comparison-graph', 'figure'),
    Output('state-comparison-footnote', 'children'),
    Input('state-code-filter', 'value'),
)
def update_state_location_interactive(location_key)-> dict:
    """Atualiza o gráfico de distribuição urbana/rural baseado na localização selecionada."""
    location= state_code_options[location_key]
    return [
        create_location_distribution(level=location['level'], local_code=location['code']),
        get_location_distribution_info(level=location['level'], local_code=location['code'])]
  
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
        create_race_distribution(level=location['level'], local_code=location['code'], year=year),
        get_race_distribution_info(level=location['level'], local_code=location['code'], year=year)]

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
        create_race_distribution(level=location['level'], local_code=location['code'], year=year),
        get_race_distribution_info(level=location['level'], local_code=location['code'], year=year)]

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
    
    top_crops_graph = create_top_crops(start_year=start_year, end_year= end_year, top_crops=top_crops)
    
    return [top_crops_graph, footnote]

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