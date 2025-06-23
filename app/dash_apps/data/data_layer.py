import sidrapy as sd
import pandas as pd
import numpy as np
import app.dash_apps.data.population as pop

from app.dash_apps.data.utils import verify_closest_year

# Usado como cache improvisado para os dados de culturas (crops)
# Recomenda-se substituir por uma implementação de cache real
# Essa abordagem pode ser aplicada a outros conjuntos de dados para melhorar o desempenho após o primeiro uso
crops_dfs = {}

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
