#Importação Bibliotecas
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_folium import st_folium
from mapas import realizar_mapa, choropleth_map
from load_data import carregar_dados
from cobertura import rev_bairro_geometry
from spatial_join import spatial_join
import streamlit.components.v1 as components

import geopandas as gp


st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1450px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


data_load_state = st.text("Carreando dados...")

dados, _ = carregar_dados()


st.title("APP VD MOSSORÓ")


data_load_state.text("Dados carregados!")

opcao_atividade = {
    "ATIVOS": "BASE ATIVA",
    "CESSADOS": "CESSADOS",
    "TODOS": "TODOS"
}


# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "SITUAÇÃO DA BASE",
        options=list(opcao_atividade.keys())
    )

with st.sidebar:
    add_inadinplecia = st.selectbox(
        "INADIMPLENTES?",
        ("Sim", "Não", "TODOS")
    )


filtro = opcao_atividade[add_radio]


if filtro != "TODOS":
    dados_1 = dados[dados["Agrupamento_Atividade"] == filtro]
    dados = dados_1[dados_1['Inadimplente?'] == add_inadinplecia]
else:
    dados = dados


st.dataframe(dados)

st.subheader("ANÁLISES DA BASE 2026C1")


with st.expander("Análise da Base", icon="👤", expanded=True):

    df_agrupado = (dados.groupby("Cidade", as_index=False)['Cod Revendedor']
                   .count()).sort_values(by='Cod Revendedor', ascending=False)

    df_agrupado_ativa = (dados.groupby("Agrupamento_Atividade", as_index=False)['Cod Revendedor']
                         .count()).sort_values(by='Cod Revendedor', ascending=False)

    valor_base_ativa = (
        dados['Agrupamento_Atividade']
        .eq('BASE ATIVA')
        .sum()
    )

    valor_base_inatiVa = (
        dados['Agrupamento_Atividade']
        .eq('CESSADOS')
        .sum()
    )

    VALOR_DELTA = ((valor_base_ativa / valor_base_inatiVa) - 1) * 100

    st.dataframe(df_agrupado)
    st.dataframe(df_agrupado_ativa)

    fig = px.bar(
        df_agrupado,
        x="Cidade",
        y="Cod Revendedor",
        title="Revendedores por Cidade"
    )
    st.plotly_chart(fig, use_container_width=True)

    a, b, c = st.columns(3)

    a.metric(label="BASE TOTAL", value=df_agrupado['Cod Revendedor'].sum(), delta="-322 Rev", border=True)

    b.metric(label="BASE ATIVA", value=valor_base_ativa, delta=f"{VALOR_DELTA:.2f}%", border=True)

    c.metric(label="VALOR FILTRO", value=opcao_atividade[add_radio], delta="35%", border=True)


with st.expander("MAPA ER", icon="🗺", expanded=True):

    mapa = realizar_mapa(dados)

    components.html(
        mapa._repr_html_(),
        height=800,
        width=1450,
        scrolling=True
    )


with st.expander("Cobertura", icon="🗺️", expanded=True):

    dict_options = {
        "Cobertura por Bairro": "Cobertura",
        "População": "Total de pessoas",
        "Média termômetro próximo papel": "termometro_proximo_papel",
        "Produtividade Bairro": 'produtividade_bairro',
        "Idade": "media_idade"
    }

    metrica_selecao = st.selectbox(
        "Selecione a visão desejada:",
        list(dict_options.keys()),
        index=False,
        placeholder="Seleciona a visão...",
    )

    coluna = dict_options[metrica_selecao]

    base_geral = rev_bairro_geometry()

    mapa_chro = choropleth_map(base_geral, coluna)

    components.html(
        mapa_chro._repr_html_(),
        height=800,
        width=1450,
        scrolling=True
    )
