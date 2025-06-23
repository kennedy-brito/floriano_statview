from dash import callback, Output, Input
from app.dash_apps.layout.config.options import * 

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
