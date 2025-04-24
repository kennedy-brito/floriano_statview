import sidrapy as sd
import pandas as pd
import numpy as np

def get_population_total(year='last') -> pd.Series:
  """
  Retrieves the total population of Floriano,
  the result is of the latest Census.
  Return:
    total: a pandas Series with a 'total_populacao' and a 'ano' row
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

def get_age_group() -> pd.DataFrame:
  """
  Retrieves the age group of the population of Floriano,
  the result is of the latest Census.
  Return:
    total: a pandas DataFrame with columns being 'valor', 'ano' and 'grupo_idade'
  """
  population_age_group = '9606'
  city='6'
  population='93'
  floriano_code='2203909'
  age='287'
  age_group = sd.get_table(
      table_code=population_age_group,
      territorial_level=city,
      classification="287",
      categories="93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098,49108,49109,60040,60041,6653",
      variable=population,
      ibge_territorial_code=floriano_code,
      period='last'
      )

  age_group = age_group.loc[:,['V','D2N','D4N']]
  age_group.columns = ["valor", "ano", "grupo_idade"]
  age_group = age_group.iloc[1:].reset_index(drop=True)

  age_group.loc[:,"valor"] = pd.to_numeric( age_group.loc[:,"valor"], errors="coerce").fillna(0).astype(np.int32)
  
  return age_group

def get_total_pib(year='last')-> pd.Series:
  """
  Retrieves the total pib of Floriano,
  the result is of the latest Census.
  Return:
    total_pib: a pandas Series with a 'total' and a 'ano' row
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
  Retrieves the most populated cities of Piauí,
  the result is of the latest Census.
  Return:
    total: a pandas DataFrame with columns being
      'populacao'
      'municipio'
      'ano'
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

def get_population_by_race() -> pd.DataFrame:
  """
  Retrieves the race distribution of the population of Floriano,
  the result is of the latest Census.
  Return:
    distribuition: a pandas DataFrame with columns being 'porcentagem', 'ano' and 'raca'
  """
  population_by_race = '9605'
  city='6'
  race='86'
  floriano_code='2203909'
  population_perc = '1000093'
  distribuition = sd.get_table(
      table_code=population_by_race,
      territorial_level=city,
      classification=race,
      # Branca, Preta, Amarela, Parda, Indígena
      categories='2776,2777,2778,2779,2780', 
      variable=population_perc,
      ibge_territorial_code=floriano_code,
      period='last'
      )

  distribuition = distribuition.loc[:, ['V','D2N', 'D4N']]
  distribuition.columns = ['porcentagem', 'ano', 'raca']
  distribuition = distribuition.iloc[1:].reset_index(drop=True)


  distribuition.loc[:,"porcentagem"] = pd.to_numeric( distribuition.loc[:,"porcentagem"], errors="coerce").fillna(0).astype(np.float32)

  distribuition.loc[:,"ano"] = pd.to_numeric( distribuition.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

  return distribuition

def get_population_by_local() -> pd.DataFrame:
  """
  Retrieves the local distribution of the population of Floriano,
  the result is of the latest Census.
  Return:
    distribuition: a pandas DataFrame with columns being 'porcentagem', 'ano' and 'local'
  """
  population_by_local = '9923'
  city='6'
  local='1'
  floriano_code='2203909'
  population_perc = '1000093'
  distribuition = sd.get_table(
      table_code=population_by_local,
      territorial_level=city,
      classification=local,
      categories='1,2', # Urbana, Rural
      variable=population_perc,
      ibge_territorial_code=floriano_code,
      period='last'
      )


  distribuition = distribuition.loc[:, ['V','D2N', 'D4N']]
  distribuition.columns = ['porcentagem', 'ano', 'local']
  distribuition = distribuition.iloc[1:].reset_index(drop=True)


  distribuition.loc[:,"porcentagem"] = pd.to_numeric( distribuition.loc[:,"porcentagem"], errors="coerce").fillna(0).astype(np.float32)

  distribuition.loc[:,"ano"] = pd.to_numeric( distribuition.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

  return distribuition

def get_pib_per_capita(year='last'):
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

  """
  Consegui o pib per capita mas tem um porém,
  não existem fontes oficiais que informem essa métrica e que possuam API
  Como eu fiz?
    Eu pego o pib mais recente e procuro informações da população daquele ano
    Isso é feito usando a tabela de população oficial e a de população estimada
      Caso uma não tenha, a busca é feita na outra
    Com esse resultado eu cálculo o pib per capita
      Pelas minhas pesquisas o resultado é bem próximo ao de fontes oficiais
      Meu resultado (2021):     24441.017451
      De outras fontes (2021):  24441.02
      Aparentemente basta aproximar
  """
  return pib_per_capita

if __name__ == '__main__':
  print(get_pib_per_capita())