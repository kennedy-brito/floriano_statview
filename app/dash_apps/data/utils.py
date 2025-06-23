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
