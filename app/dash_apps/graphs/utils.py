
def format_pib_value(value) -> str:
  """
  Formata um valor numérico em reais com notação apropriada
  para bilhões, milhões ou unidades simples.

  Args:
    value (int or float): Valor numérico em reais.

  Returns:
    str: Valor formatado como string, com vírgulas e unidade (R$, mi, bi).
  """
  if value >= 1_000_000_000:
    return f"R$ {value / 1_000_000_000:.2f} bilhões".replace(".", ",")
  elif value >= 1_000_000:
    return f"R$ {value / 1_000_000:.2f} milhões".replace(".", ",")
  else:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
