import sidrapy as sd
import pandas as pd
import numpy as np
import app.dash_apps.data.population as pop

from app.dash_apps.data.utils import verify_closest_year

# Usado como cache improvisado para os dados de culturas (crops)
# Recomenda-se substituir por uma implementação de cache real
# Essa abordagem pode ser aplicada a outros conjuntos de dados para melhorar o desempenho após o primeiro uso
crops_dfs = {}

def get_total_pib(year='last')-> pd.Series:
  """
  Retorna o valor total do PIB (Produto Interno Bruto) do município de Floriano (PI)
  para um ano específico ou para o dado mais recente disponível.

  O valor retornado é convertido de milhares de reais para reais e inclui uma nota
  indicando o ano de referência do dado.

  Args:
      year (str or int, optional): Ano desejado no formato 'YYYY' ou 'last' (padrão),
          que retorna o dado mais recente disponível.

  Returns:
      pd.Series: Série contendo:
          - 'total' (float): Valor total do PIB em reais.
          - 'ano' (int): Ano de referência.
          - 'footnote' (str): Nota indicando o ano do dado utilizado.

  Example:
      >>> get_total_pib()
      total        134521000.0
      ano                 2021
      footnote    Censo do ano de 2021
      dtype: object

  Raises:
      ValueError: Se não houver dados disponíveis para o ano especificado.
      KeyError: Se as colunas esperadas não forem encontradas na resposta da API.
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

def get_pib_per_capita(year='last'):
  """
  Calcula o PIB per capita de Floriano com base no PIB total e na população estimada do ano correspondente.

  O cálculo segue a lógica:
    - Obtém o PIB total mais recente disponível para o ano solicitado.
    - Busca a população estimada para o mesmo ano.
    - Se a população estimada não estiver disponível, obtém a população oficial.
    - Divide o PIB total pelo número de habitantes para calcular o PIB per capita.

  Nota:
    Embora o valor não seja disponibilizado diretamente por APIs oficiais, o cálculo se aproxima bastante dos valores publicados.
    Exemplo para 2021:
      - Resultado calculado: 24441.017451
      - Resultado de outras fontes: 24441.02

  Args:
      year (str or int, optional): Ano desejado no formato 'YYYY' ou 'last' (padrão),
          que retorna o dado mais recente disponível.

  Returns:
      pd.Series: Série pandas contendo:
          - 'pib_per_capita' (float): PIB per capita calculado para Floriano.
          - 'ano' (int): Ano de referência dos dados utilizados.
          - 'footnote' (str): Nota indicando o ano dos dados usados no cálculo.

  Raises:
      ValueError: Se não for possível obter dados de PIB ou população para o ano especificado.
  """
  total_population_years = ['last'] + [str(year) for year in range(2010, 2025)]
  total_population_years.remove('2023')
  
  pib = get_total_pib(year)

  if pib['ano'] not in total_population_years:
    year = verify_closest_year(pib['ano'], total_population_years)
    pib = get_total_pib(year)
  
  total_pop = pop.get_population_total(year=pib['ano'])

  pib_per_capita = pib['total']/total_pop['total_populacao']
  
  return pd.Series(
    {
      'pib_per_capita':pib_per_capita, 
      'ano': pib['ano'], 
      'footnote': f'Calculado usando dados do ano de {pib['ano']}'
    })

def get_crop_production(level="6",local_code="2203909", start_year=2010, end_year=2025, top_crops=3)-> pd.DataFrame:
  """
  Carrega e processa os dados de produção das lavouras temporárias e permanentes
  para um determinado nível territorial e código IBGE, retornando os principais cultivos
  por ano dentro do intervalo especificado.

  A função utiliza um cache interno para otimizar consultas repetidas no mesmo nível
  e localidade, evitando múltiplas chamadas à API para os mesmos dados.

  Args:
      level (str, optional): Nível territorial da consulta (ex: '6' para município).
          Padrão é '6' (município).
      local_code (str, optional): Código IBGE do local de interesse.
          Padrão é '2203909' (Floriano, PI).
      start_year (int, optional): Ano inicial do intervalo para filtragem dos dados.
          Padrão é 2010.
      end_year (int, optional): Ano final do intervalo para filtragem dos dados.
          Padrão é 2025.
      top_crops (int, optional): Quantidade dos principais cultivos (por produção) a retornar
          para cada ano dentro do intervalo. Padrão é 3.

  Returns:
      pd.DataFrame: DataFrame contendo as colunas:
          - 'medida' (str): Unidade de medida (ex: Toneladas).
          - 'quantidade' (int): Quantidade produzida na unidade informada.
          - 'ano' (int): Ano da produção.
          - 'produto' (str): Nome do cultivo/lavoura.

  Observações:
      - A função filtra para valores de produção maiores que zero e unidade em toneladas.
      - A cache interna `crops_dfs` armazena os dados carregados para evitar múltiplas consultas
        ao SIDRA para o mesmo nível e localidade.
  """
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
