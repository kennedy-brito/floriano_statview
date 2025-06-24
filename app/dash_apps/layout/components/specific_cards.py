from dash import html, dcc
from app.dash_apps.layout.config.options import city_code_options, state_code_options
from app.dash_apps.graphs.education import create_comparison_literacy, create_literacy_table, get_literacy_rate_info
from app.dash_apps.layout.components.callbacks import (
  update_city_location_interactive, 
  update_race_city_interactive,
  update_race_state_interactive,
  update_state_location_interactive)
from app.dash_apps.layout.components.generic_cards import create_graph_card_with_dropdown


def create_city_location_graph_card():
    return create_graph_card_with_dropdown(
        title="Distribuição da População por Zona Urbana/Rural - Capitais",
        options=list(city_code_options.keys()),
        default_value='Teresina - PI',
        dropdown_id='city-code-filter',
        graph_id='city-comparison-graph',
        footnote_id='city-comparison-footnote'
    )

def create_state_location_graph_card():
    return create_graph_card_with_dropdown(
        title="Distribuição da População por Zona Urbana/Rural - Estados",
        options=list(state_code_options.keys()),
        default_value='Piauí',
        dropdown_id='state-code-filter',
        graph_id='state-comparison-graph',
        footnote_id='state-comparison-footnote'
    )

def create_race_city_graph_card():
    return create_graph_card_with_dropdown(
        title="Distribuição da População por Raça - Capitais",
        options=list(city_code_options.keys()),
        default_value='Teresina - PI',
        dropdown_id='race-city-code-filter',
        graph_id='city-race-comparison-graph',
        footnote_id='city-race-comparison-footnote'
    )

def create_race_state_graph_card():
    return create_graph_card_with_dropdown(
        title="Distribuição da População por Raça - Estados",
        options=list(state_code_options.keys()),
        default_value='Piauí',
        dropdown_id='race-state-code-filter',
        graph_id='state-race-comparison-graph',
        footnote_id='state-race-comparison-footnote'
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
