import sidrapy as sd
import pandas as pd
import numpy as np

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
  population_by_gender_and_race = '9605'
  city='6'
  population='93'
  floriano_code='2203909'
  total = sd.get_table(
    table_code=population_by_gender_and_race,
    territorial_level=city,
    categories=9521,
    variable=population,
    ibge_territorial_code=floriano_code,
    period=year
  )

  total = total.loc[:, ['V','D2N']]
  total.columns = ['total_populacao', 'ano']
  total = total.iloc[1]

  total['ano'] = int(total['ano'])
  total['total_populacao'] = int(total['total_populacao'])

  return total

def get_age_group(year='last') -> pd.DataFrame:
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
  total_pib['total'] = int(total_pib['total'])*1000
  total_pib['ano'] = int(total_pib['ano']) 
  
  return total_pib
  
def get_top_population_city()-> pd.DataFrame:
  """
  Recupera os 10 municípios mais populosos do estado do Piauí com base no último Censo disponível.

  Returns:
      pd.DataFrame: DataFrame com as colunas:
          - 'populacao' (int): Quantidade de habitantes.
          - 'municipio' (str): Nome do município.
          - 'ano' (int): Ano de referência.
  """
  with open('app/dash_apps/piaui_city_codes.txt', 'r') as file:
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
      period='last'
      )

  cities_population = cities_population.loc[:, ['V', 'D1N', 'D2N']]

  cities_population.columns = ['populacao', 'municipio', 'ano']

  cities_population = cities_population.iloc[1:].reset_index(drop=True)

  cities_population['municipio'] = cities_population['municipio'].str.replace(' (PI)', '', regex=False)

  cities_population.loc[:,"populacao"] = pd.to_numeric( cities_population.loc[:,"populacao"], errors="coerce").fillna(0).astype(np.int32)

  cities_population.loc[:,"ano"] = pd.to_numeric( cities_population.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

  cities_population = cities_population.sort_values('populacao',ascending=False)

  top_population = cities_population.head(10)

  top_population = top_population.reset_index(drop=True)

  return top_population

def get_population_by_race(level='6', local_code='2203909') -> pd.DataFrame:
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
      period='last'
      )

  distribuition = distribuition.loc[:, ['V','D2N', 'D4N']]
  distribuition.columns = ['porcentagem', 'ano', 'raca']
  distribuition = distribuition.iloc[1:].reset_index(drop=True)


  distribuition.loc[:,"porcentagem"] = pd.to_numeric( distribuition.loc[:,"porcentagem"], errors="coerce").fillna(0).astype(np.float32)

  distribuition.loc[:,"ano"] = pd.to_numeric( distribuition.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

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
  pib = get_total_pib(year)

  city='6'
  floriano_code='2203909'
  estimated_population_tb='6579'
  estimated_population_v='9324'

  estimated_population = sd.get_table(
      table_code=estimated_population_tb,
      territorial_level=city,
      variable=estimated_population_v,
      ibge_territorial_code=floriano_code,
      period='last5'
      )

  estimated_population = estimated_population.loc[:,['V','D2N']]
  estimated_population.columns = ['estimativa', 'ano']
  estimated_population = estimated_population.iloc[1:].reset_index(drop=True)

  estimated_population.loc[:,"estimativa"] = pd.to_numeric( estimated_population.loc[:,"estimativa"], errors="coerce").fillna(0).astype(np.int32)
  estimated_population.loc[:,"ano"] = pd.to_numeric( estimated_population.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)


  if(pib['ano'] in estimated_population['ano'].values):
    pop = estimated_population[estimated_population['ano'] == pib['ano']]['estimativa']
  else:
    pop = get_population_total(year=pib['ano'])

  pib_per_capita = pib['total']/pop

  return pd.Series({'pib_per_capita':pib_per_capita, 'ano': pib['ano']})

if __name__ == '__main__':
  print("🔍 Testando funções de coleta de dados do SIDRA (Floriano - PI)\n")

  try:
    print("✅ População Total:")
    total_pop = get_population_total()
    print(total_pop, end="\n\n")

    print("✅ População por Faixa Etária:")
    age_group = get_age_group()
    print(age_group.head(), end="\n\n")

    print("✅ PIB Total:")
    pib_total = get_total_pib()
    print(pib_total, end="\n\n")

    print("✅ Cidades mais Populosas do Piauí:")
    top_pop = get_top_population_city()
    print(top_pop, end="\n\n")

    print("✅ População por Raça:")
    race_dist = get_population_by_race()
    print(race_dist, end="\n\n")

    print("✅ População por Local (Urbano/Rural):")
    local_dist = get_population_by_local()
    print(local_dist, end="\n\n")

    print("✅ PIB per capita:")
    pib_pc = get_pib_per_capita()
    print(pib_pc, end="\n\n")

    print("🚀 Todos os testes foram executados com sucesso!")

  except Exception as e:
    print("❌ Erro durante a execução das funções:")
    print(repr(e))
