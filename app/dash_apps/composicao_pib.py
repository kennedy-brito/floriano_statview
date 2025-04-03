from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import sidrapy as sd

def load_data():
    """Carrega e processa os dados do PIB."""
    data = sd.get_table(
        table_code='5938',
        period='all',
        territorial_level="6",
        ibge_territorial_code="2203909",
        variable='498,517,513,6575,525,37,543'
    )

    data.columns = data.iloc[0]
    data = data.iloc[1:].reset_index(drop=True)
    
    data = data.loc[:, ["Unidade de Medida", "Valor", "Ano", "Variável", ]]
    
    data.columns = ["medida", "valor", "ano", "setor"]

    # Limpeza e transformação dos dados
    data["valor"] = data["valor"].replace(["-", "..", "...", "X"], "0").astype(float) * 1000
    data["ano"] = pd.to_numeric(data["ano"], errors="coerce").fillna(0).astype(int)

    # Limpeza dos nomes dos setores
    data["setor"] = data["setor"].replace(
        {
            "Valor adicionado bruto a preços correntes da ": "",
            "Valor adicionado bruto a preços correntes dos ": "",
            "serviços, exclusive administração, defesa, educação e saúde públicas e seguridade social": "serviços",
            "Valor adicionado bruto a preços correntes total": "Total agregado dos setores"
        },
        regex=True
    )

    return data

df = load_data()

year_range_slider = dcc.RangeSlider(
    value=[2002, 2022],
    min=df["ano"].min(),
    max=df["ano"].max(),
    step=1,
    marks={i: str(i) for i in range(df["ano"].min(), df["ano"].max() + 1, 2)},
    id="year-slider"
)

def create_layout():
    """Cria o layout do aplicativo Dash."""
    return html.Div(
        style={"backgroundColor": "#f8f9fa", "padding": "20px"},
        children=[
            html.H1("Composição do PIB de Floriano ao longo do tempo", style={"textAlign": "center"}),
            dcc.Graph(id="composicao-pib"),
            html.Div(
                children=[year_range_slider],
                style={"textAlign": "center", "paddingTop": "20px", "width": "80%", "margin": "auto"}
            )
        ]
    )

def get_pib_df(init_year, final_year):
    """Filtra os dados com base no intervalo de anos selecionado."""
    return df.query(f"ano >= {init_year} and ano <= {final_year}")

def update_graph(year_range):
    """Atualiza o gráfico com base no intervalo de anos selecionado."""
    filtered_df = get_pib_df(year_range[0], year_range[1])

    fig = px.line(
        data_frame=filtered_df,
        x="ano",
        y="valor",
        color="setor",
        labels={"valor": "PIB (R$)", "ano": "Ano", "setor": "Setor"},
        title="Evolução do PIB de Floriano",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.2),
        margin=dict(l=40, r=40, t=40, b=80),
        xaxis=dict(
          dtick=1,
          showgrid=False,
          zeroline=False
        ),
        yaxis=dict(
          showgrid=False,
          zeroline=False
        )
    )

    return fig

def create_app(url_path, server=None):
    """Cria e retorna o servidor Flask para o app Dash."""
    app = Dash(requests_pathname_prefix=url_path)
    app.title = "Composição do PIB de Floriano"
    app.layout = create_layout()

    app.callback(
        Output("composicao-pib", "figure"),
        Input("year-slider", "value")
    )(update_graph)

    return app.server
