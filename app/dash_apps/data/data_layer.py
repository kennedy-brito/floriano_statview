import sidrapy as sd
import pandas as pd
import numpy as np

# Usado como cache improvisado para os dados de culturas (crops)
# Para melhor desempenho, recomenda-se substituir por uma implementação de cache real
# Essa abordagem pode ser aplicada a outros conjuntos de dados para melhorar o desempenho após o primeiro uso
crops_dfs = {}

def verify_closest_year(year, available_years: list):
  """
  Verifica se o ano solicitado está disponível; caso não esteja, retorna o ano mais próximo disponível.

  Se a lista de anos disponíveis contiver a palavra-chave 'last', ela será ignorada para calcular o ano mais próximo.
  O cálculo é feito com base na menor diferença absoluta entre o ano solicitado e os anos disponíveis.

  Args:
      year (str or int): Ano desejado, no formato string ou inteiro.
      available_years (list): Lista de anos disponíveis (strings ou inteiros), podendo incluir 'last'.

  Returns:
      str: Ano válido mais próximo, no mesmo formato que os elementos de `available_years`.

  Example:
      >>> verify_closest_year('2023', ['last', '2020', '2022', '2024'])
      '2022'
  """
  if year not in available_years:
    years= available_years[1:] if 'last' in available_years else available_years
    closest_year = min(years, key=lambda x: abs(
    int(x) - int(year)))
  
    year = closest_year
  return year

def get_population_total(year='last') -> pd.Series:
  """
  Retorna a população total do município de Floriano (PI) para um ano específico, 
  com base em dados oficiais ou estimativas do IBGE via SIDRA.

  Por padrão, busca o dado mais recente disponível. Se o ano informado não tiver 
  dado oficial (Censo), a função retorna uma estimativa para o ano mais próximo 
  possível, garantindo sempre um valor válido.

  O resultado inclui a população total, o ano de referência e uma nota de rodapé 
  indicando se o valor é oficial ou estimado.

  Args:
      year (str or int, optional): Ano desejado no formato 'YYYY' ou 'last' (padrão)
          para buscar o dado mais recente.

  Returns:
      pd.Series: Série contendo:
          - 'total_populacao': (int) População total de Floriano.
          - 'ano': (int) Ano de referência do dado.
          - 'footnote': (str) Descrição indicando se é estimativa ou dado de Censo.

  Raises:
      ValueError: Se não houver dados disponíveis para o ano informado ou próximo.
      KeyError: Se a estrutura de dados retornada pela API for inesperada.

  Example:
      >>> get_population_total()
      total_populacao    59236
      ano                 2022
      footnote    Censo Oficial de 2022
      dtype: object
  """
  
  # Existem alguns anos para os quais não há dados disponíveis
# Uma solução é verificar se há dado oficial para o ano solicitado
# Caso não haja, escolhe-se o ano mais próximo disponível
  total_population_years = ['last'] + [str(year) for year in range(2010, 2025)]
  total_population_years.remove('2023') # Não possui dado oficial
  year = verify_closest_year(year, total_population_years)
    
  population_tb = '9605' # Censo oficial
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
  
  # Os dados oficiais de população são publicados aproximadamente a cada dez anos,
  # como em 2010 e 2022. Porém, estimativas são divulgadas quase todos os anos.
  # Caso o usuário solicite um ano sem dado oficial, retorna-se uma estimativa.
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
  Retorna a distribuição da população do município de Floriano (PI) por grupos de idade,
  com base nos dados oficiais do Censo mais recente ou de um ano especificado.

  Caso o ano informado não tenha dado oficial, a função seleciona automaticamente o ano
  mais próximo disponível (2010 ou 2022).

  O resultado é um DataFrame com a quantidade de pessoas em cada faixa etária, o ano de 
  referência e uma nota de rodapé indicando o ano do Censo.

  Args:
      year (str or int, optional): Ano desejado no formato 'YYYY' ou 'last' (padrão),
          que retorna o dado mais recente disponível.

  Returns:
      pd.DataFrame: DataFrame contendo:
          - 'valor' (int): Quantidade de pessoas em cada grupo de idade.
          - 'ano' (int): Ano de referência dos dados.
          - 'grupo_idade' (str): Descrição do grupo de idade.
          - 'footnote' (str): Nota indicando o ano do Censo correspondente.

  Example:
      >>> get_population_age_group()
          valor   ano    grupo_idade               footnote
      0   3200   2022   0 a 4 anos     Censo do ano de 2022
      1   3100   2022   5 a 9 anos     Censo do ano de 2022
      ...

  Raises:
      ValueError: Se não houver dados disponíveis para o ano especificado.
      KeyError: Se as colunas esperadas não forem encontradas na resposta da API.
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
  
def get_top_population_cities(year='last')-> pd.DataFrame:
  """
  Retorna os 10 municípios mais populosos do estado do Piauí para um ano específico
  ou para o dado mais recente disponível.

  A função utiliza os dados oficiais do Censo ou, caso não haja dado oficial para o ano
  solicitado, retorna uma estimativa com base em projeções populacionais do IBGE.

  O resultado inclui a população de cada município, o nome do município, o ano de referência
  e uma nota de rodapé indicando se o dado é oficial ou estimado.

  Args:
      year (str or int, optional): Ano desejado no formato 'YYYY' ou 'last' (padrão),
          que retorna o dado mais recente disponível.

  Returns:
      pd.DataFrame: DataFrame contendo as colunas:
          - 'populacao' (int): Quantidade de habitantes do município.
          - 'municipio' (str): Nome do município (sem sufixo " (PI)").
          - 'ano' (int): Ano de referência.
          - 'footnote' (str): Indicação de Censo oficial ou estimativa.

  Example:
      >>> get_top_population_cities()
          populacao     municipio   ano                footnote
      0     868075   Teresina      2022   Censo oficial do ano de 2022
      1     163000   Parnaíba      2022   Censo oficial do ano de 2022
      ...

  Raises:
      ValueError: Se não houver dados disponíveis para o ano especificado.
      KeyError: Se as colunas esperadas não estiverem presentes na resposta.
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
  Retorna a distribuição percentual da população de um município (ou outro nível territorial)
  por raça, com base nos dados do último Censo disponível ou de um ano especificado.

  Por padrão, consulta o município de Floriano (PI). A função organiza o resultado com o 
  percentual de cada grupo racial, o ano de referência e uma nota de rodapé indicando o ano do Censo.

  Args:
      level (str, optional): Nível territorial da consulta (padrão: '6' para município).
      local_code (str, optional): Código IBGE do local de interesse 
          (padrão: '2203909' para Floriano).
      year (str or int, optional): Ano desejado no formato 'YYYY' ou 'last' (padrão),
          que retorna o dado mais recente disponível.

  Returns:
      pd.DataFrame: DataFrame contendo:
          - 'porcentagem' (float): Percentual da população para cada raça.
          - 'ano' (int): Ano de referência.
          - 'raca' (str): Descrição da raça.
          - 'footnote' (str): Indicação do ano do Censo utilizado.

  Example:
      >>> get_population_by_race()
          porcentagem   ano      raca               footnote
      0         62.5  2022     Parda     Censo do ano de 2022
      1         28.0  2022    Branca     Censo do ano de 2022
      ...

  Raises:
      ValueError: Se não houver dados disponíveis para o ano especificado.
      KeyError: Se as colunas esperadas não estiverem presentes na resposta da API.
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
  Retorna a distribuição percentual da população de um município (ou outro nível territorial) entre áreas urbanas e rurais, com base nos dados do Censo de 2022.

  Embora aceite o parâmetro `year`, atualmente os dados estão disponíveis apenas para 2022,
  sendo este ano utilizado sempre na consulta.

  O resultado informa o percentual de população em cada localidade, o ano de referência 
  e uma nota de rodapé indicando essa limitação.

  Args:
      level (str, optional): Nível territorial da consulta (padrão: '6' para município).
      local_code (str, optional): Código IBGE do local de interesse 
          (padrão: '2203909' para Floriano).
      year (str or int, optional): Ano desejado, ignorado na prática 
          pois o dado está disponível somente em 2022.

  Returns:
      pd.DataFrame: DataFrame contendo:
          - 'porcentagem' (float): Percentual da população em cada localidade.
          - 'ano' (int): Ano de referência (sempre 2022).
          - 'local' (str): Tipo de localidade ('Urbana' ou 'Rural').
          - 'footnote' (str): Nota indicando a limitação de ano fixo.

  Example:
      >>> get_population_by_local()
          porcentagem   ano   local                       footnote
      0         87.5  2022  Urbana  Dado disponível somente no ano de 2022
      1         12.5  2022   Rural  Dado disponível somente no ano de 2022

  Raises:
      ValueError: Se houver erro na consulta à API.
      KeyError: Se as colunas esperadas não estiverem presentes na resposta.
  """
  available_years = ['last', '2022']
  year = verify_closest_year(year, available_years)
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

  Os dados correspondem à taxa de alfabetização segmentada por grupo etário e localização territorial,
  podendo ser município, estado ou Brasil, conforme os parâmetros. O DataFrame retornado está limpo,
  com os dados prontos para análise ou visualização.

  Nota:
      Os dados estão disponíveis apenas para o ano de 2022, independentemente do parâmetro `year`.

  Args:
      level (int): Nível territorial da consulta. Valores comuns:
          - 6: Município
          - 2: Unidade da Federação (Estado)
          - 1: Brasil
      code (str): Código IBGE do território consultado. Exemplo padrão: '2203909' (Floriano, PI).
      year (str or int): Ano da consulta, ignorado na prática pois os dados são fixos em 2022.

  Returns:
      pd.DataFrame: DataFrame com as seguintes colunas:
          - 'medida' (str): Tipo de medida (ex: percentual, número absoluto).
          - 'quantidade' (float): Valor numérico da medida.
          - 'grupo' (str): Grupo populacional (ex: faixa etária).
          - 'local' (str): Nome do local (ex: Floriano, Piauí, Brasil).
          - 'ano' (int): Ano de referência dos dados.
          - 'footnote' (str): Nota informando a limitação temporal dos dados.

  Raises:
      ValueError: Se a consulta à API falhar ou retornar dados inconsistentes.
      KeyError: Se as colunas esperadas não estiverem presentes na resposta.

  Example:
      >>> df = get_literacy_rate(level=6, code='2203909')
      >>> df.head()
        medida  quantidade       grupo    local   ano                       footnote
      0  %      92.5        15 a 24 anos  Floriano 2022  Dado disponível somente no ano de 2022
      ...
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