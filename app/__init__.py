from flask import Flask
from .dash_apps import composicao_pib
from werkzeug.middleware.dispatcher import DispatcherMiddleware

DASH_APPS = {
  '/pib-floriano': (composicao_pib.create_app, "Composição do PIB de Floriano")
}

def create_app():
  app = Flask(__name__)
  
  dash_mw_input = {}
  
  list_items = ""

  for url in DASH_APPS:
      # Add pathname: dash_app mapping to middleware.
      dash_mw_input[url] = DASH_APPS[url][0](url + "/")

      # Add name and pathname to <li>
      list_items += "<li><a href=\"" + url + "/\">" + DASH_APPS[url][1] + "</a></li>\n"

  # Integrate Flask and Dash apps using DispatcherMiddleware
  
  @app.route("/")
  def home():
    return f"""
  <u>
  {list_items}
  </u>
  """
  app = DispatcherMiddleware(app, dash_mw_input)
  
  return app