import sidrapy as sd
import pandas as pd
import numpy as np

def get_population_total():
  
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

def get_age_group():
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
  age_group.columns = age_group.iloc[0]
  age_group = age_group.iloc[1:].reset_index(drop=True)

  age_group.loc[:,"Valor"] = pd.to_numeric( age_group.loc[:,"Valor"], errors="coerce").fillna(0).astype(np.int32)
  
  return age_group

def get_total_pib():
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
  total_pib
  
  