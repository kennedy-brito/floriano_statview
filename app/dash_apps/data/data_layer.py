import sidrapy as sd
import pandas as pd
import numpy as np

crops_dfs = {}

def verify_closest_year(year, available_years: list):
    if year not in available_years:
      years= available_years[1:] if 'last' in available_years else available_years
      closest_year = min(years, key=lambda x: abs(
      int(x) - int(year)))
    
      year = closest_year
    return year

def get_population_total(year='last') -> pd.Series:
  """
  Retorna a população total de Floriano para um ano específico, com base nos dados do SIDRA (IBGE).

  A função consulta a tabela de população por sexo e cor/raça (código 9605), no nível territorial municipal,
  para o município de Floriano (código 2203909). O resultado é uma série do pandas contendo o ano e a
  população total estimada ou recenseada, dependendo do período informado.

  Args:
      year (str or int, optional): O ano desejado no formato 'YYYY' ou 'last' (padrão),
          que retorna o dado mais recente disponível.

  Returns:
      pd.Series: Uma série contendo:
          - 'total_populacao': (int) A população total do município de Floriano.
          - 'ano': (int) O ano de referência do dado retornado.

  Raises:
      ValueError: Se a resposta da API estiver vazia ou mal formatada.
      KeyError: Se as colunas esperadas não estiverem presentes na resposta.

  Example:
      >>> get_population_total()
      total_populacao    59236
      ano                 2022
      dtype: object
  """
  #TODO: UPDATE DOCSTRINGS
  
  # There are some years that the data is not available
  # A solution is to verify if the data is available in the year
  # if not, we chose the closest data available
  total_population_years = ['last'] + [str(year) for year in range(2010, 2025)]
  total_population_years.remove('2023')
  year = verify_closest_year(year, total_population_years)
    
  population_tb = '9605'
  city='6'
  population='93'
  floriano_code='2203909'
  total = sd.get_table(
    table_code=population_tb,   
    territorial_level=city,
    categories=9521,
    variable=population,
    ibge_territorial_code=floriano_code,
    period=year
  )
  
  total = total[1:]
  
  # the official population data is published in roughly ten years time, so
  # in 2010, 2022, etc. But an estimative is published nearly every year
  # in case a user selects a year that has no official data we present an estimative
  if total.empty:
    city='6'
    floriano_code='2203909'
    estimated_population_tb='6579'
    estimated_population_v='9324'

    total = sd.get_table(
        table_code=estimated_population_tb,
        territorial_level=city,
        variable=estimated_population_v,
        ibge_territorial_code=floriano_code,
        period=year
    )
  
    total = total.loc[:,['V','D2N']]
    total.columns = ['total_populacao', 'ano']
    total = total.iloc[1:].reset_index(drop=True)

    total.loc[:,"total_populacao"] = pd.to_numeric( total.loc[:,"total_populacao"], errors="coerce").fillna(0).astype(np.int32)
    total.loc[:,"ano"] = pd.to_numeric( total.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)
   
    total = total.iloc[0]

    total['footnote'] = f"Estimativa do Censo de {total['ano']}"

  else:
    total = total.loc[:, ['V','D2N']]
    total.columns = ['total_populacao', 'ano']

    total['ano'] = int(total.iloc[0]['ano'])
    total['total_populacao'] = int(total.iloc[0]['total_populacao'])

    total = total.iloc[0]

    total['footnote'] = f"Censo Oficial de {total['ano']}"
  
  return total

def get_population_age_group(year='last') -> pd.DataFrame:
  """
  Recupera a distribuição da população de Floriano por grupo de idade com base no último Censo disponível.

  Args:
      year (str, optional): Ano da consulta. Por padrão, busca o dado mais recente ('last').

  Returns:
      pd.DataFrame: DataFrame com as colunas:
          - 'valor' (int): Quantidade de pessoas em cada grupo etário.
          - 'ano' (int): Ano de referência.
          - 'grupo_idade' (str): Descrição do grupo de idade.
  """
  age_group_years = ['last', '2010', '2022']
  year = verify_closest_year(year, age_group_years)
  
  population_age_group = '9606'
  city='6'
  population='93'
  floriano_code='2203909'
  age='287'
  age_group = sd.get_table(
      table_code=population_age_group,
      territorial_level=city,
      classification=age,
      categories="93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098,49108,49109,60040,60041,6653",
      variable=population,
      ibge_territorial_code=floriano_code,
      period=year
      )

  age_group = age_group.loc[:,['V','D2N','D4N']]
  age_group.columns = ["valor", "ano", "grupo_idade"]
  age_group = age_group.iloc[1:].reset_index(drop=True)

  age_group.loc[:,"valor"] = pd.to_numeric( age_group.loc[:,"valor"], errors="coerce").fillna(0).astype(np.int32)
  
  age_group['footnote'] = f'Censo do ano de {age_group.iloc[0]['ano']}'
  
  return age_group

def get_total_pib(year='last')-> pd.Series:
  """
  Recupera o valor total do PIB (Produto Interno Bruto) de Floriano no ano especificado.

  Args:
      year (str, optional): Ano da consulta. Por padrão, busca o dado mais recente ('last').

  Returns:
      pd.Series: Série com as seguintes chaves:
          - 'total' (int): Valor total do PIB em reais (convertido de milhares).
          - 'ano' (int): Ano de referência.
  """
  total_pib_years = ['last'] + [str(year) for year in range(2010, 2022)]
  year = verify_closest_year(year, total_pib_years)
  pib_composition='5938'
  city='6'
  floriano_code='2203909'
  total='37'
  total_pib = sd.get_table(
          table_code=pib_composition,
          period=year,
          territorial_level=city,
          ibge_territorial_code=floriano_code,
          variable=total
      )

  total_pib = total_pib.loc[:,['V','D2N']] 
  total_pib.columns = ['total', 'ano']
  total_pib = total_pib.iloc[1]
  total_pib['total'] = float(total_pib['total'])*1000
  total_pib['ano'] = int(total_pib['ano']) 
  
  total_pib['footnote'] = f'Censo do ano de {total_pib['ano']}'
  
  return total_pib
  
def get_top_population_cities(year='last')-> pd.DataFrame:
  """
  Recupera os 10 municípios mais populosos do estado do Piauí com base no último Censo disponível.

  Returns:
      pd.DataFrame: DataFrame com as colunas:
          - 'populacao' (int): Quantidade de habitantes.
          - 'municipio' (str): Nome do município.
          - 'ano' (int): Ano de referência.
  """
  total_population_years = ['last'] + [str(year) for year in range(2010, 2025)]
  total_population_years.remove('2023')
  year = verify_closest_year(year, total_population_years)
  
  with open('app/dash_apps/data/piaui_city_codes.txt', 'r') as file:
    city_codes = file.readline()
  
  population_of_cities = '9605'
  city='6'
  population='93'

  cities_population = sd.get_table(
      table_code=population_of_cities,
      territorial_level=city,
      categories=9521,
      variable=population,
      ibge_territorial_code=city_codes,
      period=year
      )
  cities_population = cities_population.iloc[1:].reset_index(drop=True)

  if cities_population.empty:
    estimated_population_tb='6579'
    estimated_population_v='9324'

    cities_population = sd.get_table(
        table_code=estimated_population_tb,
        territorial_level=city,
        variable=estimated_population_v,
        ibge_territorial_code=city_codes,
        period=year
    )
  
    cities_population = cities_population.loc[:,['V','D1N', 'D2N']]
    cities_population.columns = ['total_populacao', 'municipio', 'ano']
    cities_population = cities_population.iloc[1:].reset_index(drop=True)

    cities_population['municipio'] = cities_population['municipio'].str.replace(' (PI)', '', regex=False)
    
    cities_population.loc[:,"populacao"] = pd.to_numeric( cities_population.loc[:,"total_populacao"], errors="coerce").fillna(0).astype(np.int32)
    
    cities_population.loc[:,"ano"] = pd.to_numeric( cities_population.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

    cities_population['footnote'] = f"Estimativas do Censo de {cities_population.iloc[0]['ano']}"
    
  else:
    cities_population = cities_population.loc[:, ['V', 'D1N', 'D2N']]

    cities_population.columns = ['populacao', 'municipio', 'ano']


    cities_population['municipio'] = cities_population['municipio'].str.replace(' (PI)', '', regex=False)

    cities_population.loc[:,"populacao"] = pd.to_numeric( cities_population.loc[:,"populacao"], errors="coerce").fillna(0).astype(np.int32)

    cities_population.loc[:,"ano"] = pd.to_numeric( cities_population.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)
    
    cities_population['footnote'] = f"Censo oficial do ano de {cities_population.iloc[0]['ano']}"

  cities_population = cities_population.sort_values('populacao',ascending=False)

  top_population = cities_population.head(10)

  top_population = top_population.reset_index(drop=True)


  return top_population

def get_population_by_race(level='6', local_code='2203909', year='last') -> pd.DataFrame:
  """
  Recupera a distribuição percentual da população de Floriano por raça, com base no último Censo.

  Args:
      level (str, optional): Nível territorial da consulta (padrão: '6' para município).
      local_code (str, optional): Código IBGE do município (padrão: '2203909' para Floriano).

  Returns:
      pd.DataFrame: DataFrame com as colunas:
          - 'porcentagem' (float): Percentual da população por raça.
          - 'ano' (int): Ano de referência.
          - 'raca' (str): Descrição da raça.
  """
  race_group_years = ['last', '2010', '2022']
  year = verify_closest_year(year, race_group_years)
  
  population_by_race = '9605'
  race='86'
  population_perc = '1000093'
  distribuition = sd.get_table(
      table_code=population_by_race,
      territorial_level=level,
      classification=race,
      # Branca, Preta, Amarela, Parda, Indígena
      categories='2776,2777,2778,2779,2780', 
      variable=population_perc,
      ibge_territorial_code=local_code,
      period=year
      )

  distribuition = distribuition.loc[:, ['V','D2N', 'D4N']]
  distribuition.columns = ['porcentagem', 'ano', 'raca']
  distribuition = distribuition.iloc[1:].reset_index(drop=True)


  distribuition.loc[:,"porcentagem"] = pd.to_numeric( distribuition.loc[:,"porcentagem"], errors="coerce").fillna(0).astype(np.float32)

  distribuition.loc[:,"ano"] = pd.to_numeric( distribuition.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

  distribuition['footnote'] = f"Censo do ano de {distribuition.iloc[0]['ano']}"

  return distribuition

def get_population_by_local(level='6', local_code='2203909', year='last') -> pd.DataFrame:
  """
  Recupera a distribuição percentual da população de Floriano entre áreas urbanas e rurais, com base no último Censo.

  Args:
    level (str, optional): Nível territorial da consulta (padrão: '6' para município).
    local_code (str, optional): Código IBGE do município (padrão: '2203909' para Floriano).
    year (str, optional): Ano da consulta. Por padrão, busca o dado mais recente ('last').

  Returns:
    pd.DataFrame: DataFrame com as colunas:
      - 'porcentagem' (float): Percentual da população por localidade.
      - 'ano' (int): Ano de referência.
      - 'local' (str): Tipo de localidade ('Urbana' ou 'Rural').
  """
  year = '2022'
  population_by_local = '9923'
  local='1'
  population_perc = '1000093'
  distribuition = sd.get_table(
      table_code=population_by_local,
      territorial_level=level,
      classification=local,
      categories='1,2', # Urbana, Rural
      variable=population_perc,
      ibge_territorial_code=local_code,
      period=year
      )


  distribuition = distribuition.loc[:, ['V','D2N', 'D4N']]
  distribuition.columns = ['porcentagem', 'ano', 'local']
  distribuition = distribuition.iloc[1:].reset_index(drop=True)


  distribuition.loc[:,"porcentagem"] = pd.to_numeric( distribuition.loc[:,"porcentagem"], errors="coerce").fillna(0).astype(np.float32)

  distribuition.loc[:,"ano"] = pd.to_numeric( distribuition.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

  distribuition['footnote'] = 'Dado disponível somente no ano de 2022'
  
  return distribuition

def get_pib_per_capita(year='last'):
  """
  Calcula o PIB per capita de Floriano com base no PIB total e na população estimada do ano correspondente.

  O cálculo é feito utilizando a seguinte lógica:
    - Busca o PIB mais recente disponível.
    - Tenta obter a população estimada para o mesmo ano.
    - Caso não esteja disponível, busca a população oficial daquele ano.
    - Divide o valor total do PIB pelo número de habitantes.

  Nota:
    Embora o dado não esteja disponível diretamente por API em fontes oficiais, o valor calculado se aproxima bastante de dados publicados.
    Resultado calculado (2021): 24441.017451
    Resultado de outras fontes (2021): 24441.02

  Args:
    year (str, optional): Ano da consulta. Por padrão, busca o dado mais recente ('last').

  pd.Series: Uma série contendo:
    - 'pib_per_capita': (float) O PIB Per Capita de Floriano
    - 'ano': (int) O ano de referência do dado retornado.
  """
  total_population_years = ['last'] + [str(year) for year in range(2010, 2025)]
  total_population_years.remove('2023')
  
  pib = get_total_pib(year)

  if pib['ano'] not in total_population_years:
    year = verify_closest_year(pib['ano'], total_population_years)
    pib = get_total_pib(year)
  
  pop = get_population_total(year=pib['ano'])

  pib_per_capita = pib['total']/pop['total_populacao']
  
  return pd.Series(
    {
      'pib_per_capita':pib_per_capita, 
      'ano': pib['ano'], 
      'footnote': f'Calculado usando dados do ano de {pib['ano']}'
    })

def get_literacy_rate(level=6, code='2203909', year='last') -> pd.DataFrame:
  """
  Carrega e processa os dados da taxa de alfabetização a partir da tabela SIDRA (código 9543).

  Os dados retornados correspondem à taxa de alfabetismo por grupo etário e localização 
  (Município, Estado ou Brasil), conforme especificado nos parâmetros. O DataFrame retornado 
  está limpo e pronto para análise ou visualização.

  Args:
      level (int): Nível territorial da consulta. Os valores comuns são:
          - 6: Município
          - 2: Unidade da Federação (Estado)
          - 1: Brasil
      code (str): Código IBGE do território consultado. Por padrão, '2203909' representa o município de Floriano (PI).
      year (str): Ano da consulta. Pode ser um ano específico (ex: '2022') ou 'last' para pegar o dado mais recente disponível.

  Returns:
      pd.DataFrame: DataFrame com as colunas:
          - 'medida': Tipo de medida (ex: percentual ou número absoluto)
          - 'quantidade': Valor da medida
          - 'grupo': Grupo populacional (ex: faixa etária)
          - 'local': Nome do local (ex: Floriano, Piauí, Brasil)
          - 'ano': Ano do dado
  """
  
  literacy_rate = sd.get_table(
    table_code='9543',
    period=year,
    territorial_level=level,
    classification="287",
    categories="93086,93087,2999,9482,9483,9484,3000",
    ibge_territorial_code=code,
    variable='2513')
  
  literacy_rate = literacy_rate.loc[:, ["MN", "V", "D4N", "D1N", "D2N"]]
  
  literacy_rate.columns = literacy_rate.iloc[0]
  
  literacy_rate = literacy_rate.iloc[1:].reset_index(drop=True)

  literacy_rate.columns = ["medida", "quantidade", "grupo", "local", "ano"]
  
  literacy_rate.loc[:,"quantidade"] = pd.to_numeric( literacy_rate.loc[:,"quantidade"], errors="coerce").fillna(0).astype(np.float32)
  
  literacy_rate['footnote'] = 'Dado disponível somente no ano de 2022'
  
  return literacy_rate

def get_crop_production(level="6",local_code="2203909", start_year=2010, end_year=2025, top_crops=3)-> pd.DataFrame:
  """Carrega e processa os dados das Lavouras."""
  key = f"{level}_{local_code}"
  
  crops = crops_dfs.get(key)
  
  if crops is None:
    temporary_permanent_crops_production_tb='5457'
    crops = sd.get_table(
      table_code=temporary_permanent_crops_production_tb,
      classifications={'782':"allxt"},
      period='all',
      territorial_level=level,
      ibge_territorial_code=local_code,
      variable='214')
    
    crops.columns = crops.iloc[0]
    crops = crops.iloc[1:].reset_index(drop=True)
    
    crops = crops.loc[:, ["Unidade de Medida","Valor","Ano","Produto das lavouras temporárias e permanentes"]]
    
    crops.columns = ["medida", "quantidade", "ano", "produto"]
    
    crops = crops[
      (crops["quantidade"] != '...') &
      (crops["medida"] == 'Toneladas') &
      (crops["quantidade"] != 'X')
    ]
    
    crops.loc[:,"quantidade"] = crops.loc[:,"quantidade"].replace(['-', '..'], value='0')
    crops.loc[:,"quantidade"] = crops.loc[:,"quantidade"].str.strip()
    crops.loc[:,"quantidade"] = pd.to_numeric( crops.loc[:,"quantidade"], errors="coerce").fillna(0).astype(np.int32)
    crops.loc[:,"ano"] = pd.to_numeric( crops.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)
    
    crops = crops[crops["ano"] >= 2002]
    
    crops = crops.query("quantidade != 0")
    
    crops.sort_values(by='quantidade', ascending=False, inplace=True)

    crops_dfs[key] = crops
    
  crops = crops.query(f"ano >= {start_year} and ano <= {end_year}")
  
  crops = crops.groupby("ano", group_keys=False).head(top_crops).sort_values(by='quantidade', ascending=False)
  
  return crops