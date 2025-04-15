from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd

def data_from(level, code):
    data = sd.get_table(
      table_code='9543',
      period='last',
      territorial_level=level,
      classification="287",
      categories="93086,93087,2999,9482,9483,9484,3000",
      ibge_territorial_code=code,
      variable='2513')
    
    data = data.loc[:, ["MN", "V", "D4N", "D1N"]]
    
    data.columns = data.iloc[0]
    
    data = data.iloc[1:].reset_index(drop=True)

    data.columns = ["medida", "quantidade", "grupo", "local"]
    
    data.loc[:,"quantidade"] = pd.to_numeric( data.loc[:,"quantidade"], errors="coerce").fillna(0).astype(np.float32)
    
    return data

def load_data() -> pd.DataFrame:
    """Carrega e processa os dados de taxa de alfabetismo de Floriano, do Piauí e do Brasil."""
    
    floriano_dt = data_from(level= 6,code=2203909)
    
    piaui_dt = data_from(level= 3,code=22)
    
    brasil_dt = data_from(level= 1,code=1)
    
    data = pd.concat(
      [floriano_dt, piaui_dt, brasil_dt],
      ignore_index=True
    )
    
    return data

df = load_data()

def create_layout():
    """Cria o layout do aplicativo Dash."""
    return html.Div(
        style={"backgroundColor": "#f8f9fa", "padding": "20px"},
        children=[
            html.H1("Taxa de Alfabetização", style={"textAlign": "center"}),

            dcc.Graph(id="taxa-alfabetizacao", figure=update_graph()),

            ]
        )

def update_graph():
    """Cria o gráfico de comparação entre as taxas de alfabetismo"""
    
    fig = px.line(
      data_frame=df,
      y="quantidade",
      x="grupo",
      color="local",
      labels={"quantidade": "Taxa de Alfabetização (%)", "grupo": "Faixa Etária", "local": "Localidade"},
      markers=True,
      color_discrete_sequence=px.colors.qualitative.Set2,
    )

    fig.update_layout(
        title_text=f"Taxa de Alfabetização - Floriano x Piauí x Brasil",
        xaxis=dict(
            
            tickmode='linear',
            dtick=1
        ),
        yaxis=dict(
            range=[50, 100])
    )   
    
    return fig 

def create_app(url_path, server=None):
    """Cria e retorna o servidor Flask para o app Dash."""
    app = Dash(requests_pathname_prefix=url_path)
    app.title = "Taxa de Alfabetização - Floriano x Piauí x Brasil"

    app.layout = create_layout()

    return app.server
