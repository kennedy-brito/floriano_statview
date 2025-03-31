from flask import Flask
from .dash_apps import composicao_pib, maiores_lavouras
from werkzeug.middleware.dispatcher import DispatcherMiddleware

DASH_APPS = {
  '/pib-floriano': (composicao_pib.create_app, "Composição do PIB de Floriano"),
  '/maiores-lavouras': (maiores_lavouras.create_app, "Maiores Lavouras de Floriano"),
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