import sidrapy as sd
import pandas as pd
import numpy as np

def get_population_total() -> pd.Series:
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
      period='last'
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

def get_total_pib()-> pd.Series:
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
          period='last',
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
  with open('./piaui_city_codes', 'r') as file:
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
  population_by_race = '9605'
  city='6'
  race='86'
  floriano_code='2203909'
  population_perc = '1000093'
  distribuicao = sd.get_table(
      table_code=population_by_race,
      territorial_level=city,
      classification=race,
      # Branca, Preta, Amarela, Parda, Indígena
      categories='2776,2777,2778,2779,2780', 
      variable=population_perc,
      ibge_territorial_code=floriano_code,
      period='last'
      )

  distribuicao = distribuicao.loc[:, ['V','D2N', 'D4N']]
  distribuicao.columns = ['porcentagem', 'ano', 'raca']
  distribuicao = distribuicao.iloc[1:].reset_index(drop=True)


  distribuicao.loc[:,"porcentagem"] = pd.to_numeric( distribuicao.loc[:,"porcentagem"], errors="coerce").fillna(0).astype(np.float32)

  distribuicao.loc[:,"ano"] = pd.to_numeric( distribuicao.loc[:,"ano"], errors="coerce").fillna(0).astype(np.int32)

  return distribuicao