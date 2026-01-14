
#%%
import geopandas as gpd
import pandas as pd
import os
from malhas_bairros import merge_malha_agregados
import streamlit as st



@st.cache_data
def carregar_dados() -> tuple[pd.DataFrame,pd.DataFrame]:

    """
    Carregaga dados de Revendedores, Polígonos e Agragados de bairro,
    faz o merge entre poligonos de bairro e agragados. Retorna o dataframme
    de dados de revendedores e um Dataframe com os polígonos e os agregados por bairro.
    """

    path_malhas = st.secrets["PATH_MALHA_BAIRROS"]

    path_rev = st.secrets["PATH_BASE_REV"]

    path_agregados_bairro = st.secrets["PATH_AGREGADOS_BAIRROS"]


    dados_rev = pd.read_excel(path_rev)

    dados_bairros = gpd.read_file(path_malhas)

    dados_bairros_agregados = pd.read_excel(path_agregados_bairro)

    base_bairros = merge_malha_agregados(dados_bairros,dados_bairros_agregados)

    base_bairros = base_bairros[base_bairros['NM_MUN'] == "Mossoró"]

    base_bairros.drop(columns=['CD_REGIAO','NM_REGIAO','CD_UF',
                                'CD_DIST', 'NM_DIST', 'CD_SUBDIST',
                                'NM_SUBDIST','CD_RGINT', 'NM_RGINT', 'CD_RGI', 'NM_RGI', 'CD_CONCURB',
       'NM_CONCURB'], inplace= True)
    

    
    dados_rev.columns = dados_rev.columns.str.strip()
    base_bairros.columns = base_bairros.columns.str.strip()

    dados_rev["Termômetro Prox. Papel"] = (
        dados_rev["Termômetro Prox. Papel"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    

    base_bairros["CD_BAIRRO"] = base_bairros["CD_BAIRRO"].astype(str)





    return dados_rev,base_bairros


#%%





