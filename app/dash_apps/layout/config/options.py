from dash import dcc

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
