from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd

def load_data() -> pd.DataFrame:
    """Carrega e processa os dados das Lavouras."""
    data = sd.get_table(
      table_code='5457',
      classifications={'782':"allxt"},
      period='all',
      territorial_level="6",
      ibge_territorial_code="2203909",
      variable='214')
    
    data.columns = data.iloc[0]
    data = data.iloc[1:].reset_index(drop=True)
    
    data = data[
      (data["Valor"] != '...') &
      (data["Unidade de Medida"] == 'Toneladas') &
      (data["Valor"] != 'X')
    ]
    
    data.loc[:,"Valor"] = data.loc[:,"Valor"].replace(['-', '..'], value='0')
    data.loc[:,"Valor"] = data.loc[:,"Valor"].str.strip()
    data.loc[:,"Valor"] = pd.to_numeric( data.loc[:,"Valor"], errors="coerce").fillna(0).astype(np.int32)
    data.loc[:,"Ano"] = pd.to_numeric( data.loc[:,"Ano"], errors="coerce").fillna(0).astype(np.int32)
    
    data = data[data["Ano"] >= 2002]
    data = data.iloc[:, [3,4,8,12]]
    data.columns = ["medida", "unidade", "ano", "produto"]
    
    data = data.query("unidade != 0")
    
    
    return data
    

df = load_data()

year_range_slider = dcc.RangeSlider(
    value=[2002, df.ano.astype(int).max()],
    min=df["ano"].min(),
    max=df["ano"].max(),
    step=1,
    marks={i: str(i) for i in range(df["ano"].min(), df["ano"].max() + 1, 2)},
    id="year-slider"
)

top_productions_slider = dcc.Slider(
  id="top-productions",
  min=1,
  max=10,
  step=1,
  value=3,
  marks={i: str(i) for i in range(1, 11)}
  )

def create_layout():
    """Cria o layout do aplicativo Dash."""
    return html.Div(
        style={"backgroundColor": "#f8f9fa", "padding": "20px"},
        children=[
            html.H1("Maiores Lavouras de Floriano por Ano", style={"textAlign": "center"}),

            dcc.Graph(id="maiores-lavouras"),

            html.Div(
                children=[
                    html.Div(
                        [
                            html.P("Ano:", style={"marginBottom": "5px"}),
                            year_range_slider
                            ], 
                        style={"width": "70%", "display": "inline-block"}
                        ),
                    html.Div(
                        [
                            html.P("Maiores Produções:", style={"marginBottom": "5px"}),
                            top_productions_slider
                            ], 
                        style={"width": "25%", "display": "inline-block", "marginLeft": "5%"}
                        )
                    ],
                style={"display": "flex", "justify-content": "center", "align-items": "center", "width": "80%", "margin": "auto"}
                )
            ]
        )
    

def get_lavouras_df(init_year, final_year, top_productions):
    """Filtra os dados com base no intervalo de anos selecionado e na quantidade de produções selecionada."""
    
    filtered_df = df.query(f"ano >= {init_year} and ano <= {final_year}")
    
    return (
        filtered_df
          .sort_values(["ano", "unidade"], ascending=[True, False])
          .groupby("ano", group_keys=False)
          .head(top_productions)
    )

def update_graph(year_range, top_productions):
    """Atualiza o gráfico com base no intervalo de anos selecionado e na quantidade de lavouras selecionada."""
    filtered_df = get_lavouras_df(year_range[0], year_range[1], top_productions)

    fig = px.bar(
      data_frame=filtered_df,
      y="unidade",
      x="ano",
      text="unidade",
      orientation="v",
      color="produto",
      color_discrete_sequence=px.colors.qualitative.Set2,
      custom_data=["produto"]
    )

    fig.update_layout(
        title_text=f"Maiores Lavouras de Floriano ({year_range[0]} - {year_range[1]})",
        xaxis=dict(
            
            tickmode='linear',
            dtick=1
        )
    )   
    fig.update_yaxes(title_text="Produção em Toneladas")
    fig.update_traces(
        hovertemplate="<b>Produto:</b> %{customdata[0]}<br><b>Produção:</b> %{y:,.0f} toneladas"
    )
    return fig 

def create_app(url_path, server=None):
    """Cria e retorna o servidor Flask para o app Dash."""
    app = Dash(requests_pathname_prefix=url_path)
    app.title = "Maiores Produções Agrícoloas de Floriano"
    app.layout = create_layout()

    app.callback(
        Output("maiores-lavouras", "figure"),
        Input("year-slider", "value"),
        Input("top-productions", "value")
    )(update_graph)

    return app.server
    
