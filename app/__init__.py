from flask import Flask
from app.dash_apps.layout import composicao_pib, maiores_lavouras, taxa_alfabetizacao_idade, general_information_dashboard as general_info
from werkzeug.middleware.dispatcher import DispatcherMiddleware

DASH_APPS = {
  '/floriano-statview': (general_info.create_app, "Floriano Statview"),
  '/pib-floriano': (composicao_pib.create_app, "Composição do PIB de Floriano"),
  '/maiores-lavouras': (maiores_lavouras.create_app, "Maiores Lavouras de Floriano"),
  '/taxa-alfabetizacao': (taxa_alfabetizacao_idade.create_app, "Taxa de Alfabetização - Floriano - Piauí - Brasil"),
}

def create_app():
  app = Flask(__name__)
  
  dash_mw_input = {}
  
  list_items = ""

  for url in DASH_APPS:
     
      dash_mw_input[url] = DASH_APPS[url][0](url + "/")

      list_items += "<li><a href=\"" + url + "/\">" + DASH_APPS[url][1] + "</a></li>\n"

  
  @app.route("/")
  def home():
    return f"""
  <u>
  {list_items}
  </u>
  """
  app = DispatcherMiddleware(app, dash_mw_input)
  
  return app