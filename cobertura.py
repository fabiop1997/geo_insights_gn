#%%

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import streamlit as st
from shapely import wkt
from spatial_join import spatial_join
from load_data import carregar_dados


@st.cache_data
def rev_bairro_geometry() -> gpd.GeoDataFrame:

    _,populacao_bairros = carregar_dados()


    rev_com_bairro = spatial_join()



    rev_com_bairro["Receita VD Últimos 6 ciclos"] = rev_com_bairro["Receita VD Últimos 6 ciclos"].astype(float)
    rev_com_bairro["Crédito Disponível"] =  rev_com_bairro["Crédito Disponível"].astype(float)
    rev_com_bairro["Receita Média VD 6 ciclos"] = rev_com_bairro["Receita Média VD 6 ciclos"].astype(float)

    rev_com_bairro["Termômetro Prox. Papel"] = (
        rev_com_bairro["Termômetro Prox. Papel"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )




    """
    Agrega informações de revendedores por bairro, realizando:
    - Tratamento de dados financeiros
    - Conversão para GeoDataFrame
    - Spatial join com bairros
    - Agregações por bairro
    - Merge com população e geometria dos bairros

    Parâmetros
    ----------
    df_rev : pd.DataFrame
        Base de revendedores com latitude e longitude

    Retorno
    -------
    gpd.GeoDataFrame
        Base agregada por bairro com métricas de receita, perfil e geometria
    """


    # ------------------------------------------------------------------
    # 5. Agregações por bairro
    # ------------------------------------------------------------------
    rev_bairro_agrupado = (
        rev_com_bairro
        .groupby(["CD_BAIRRO", "NM_BAIRRO"], as_index=False)
        .agg(
            receita_total=("Receita VD Últimos 6 ciclos", "sum"),
            credito_disponivel=("Crédito Disponível", "mean"),
            media_idade=("Idade", "mean"),
            termometro_proximo_papel=("Termômetro Prox. Papel", "mean"),
            receita_media_ultimos_6_ciclos=("Receita Média VD 6 ciclos", "mean"),
            qtd_rev=("Cod Revendedor", "count"),

            # Contagem por papel
            qtd_Bronze=("Papel", lambda x: (x == "Bronze").sum()),
            qtd_Prata=("Papel", lambda x: (x == "Prata").sum()),
            qtd_Ouro=("Papel", lambda x: (x == "Ouro").sum()),
            qtd_Platina=("Papel", lambda x: (x == "Platina").sum()),
            qtd_Diamante=("Papel", lambda x: (x == "Diamante GB").sum()),
            qtd_Esmeralda=("Papel", lambda x: (x == "Esmeralda GB").sum()),
            qtd_Rubi=("Papel", lambda x: (x == "Rubi").sum()),
        )
    )

    # ------------------------------------------------------------------
    # 6. Métricas derivadas
    # ------------------------------------------------------------------
    rev_bairro_agrupado["produtividade_bairro"] = (
        (rev_bairro_agrupado["receita_total"] / 6)
        / rev_bairro_agrupado["qtd_rev"]
    )

    rev_bairro_agrupado["rev_vips"] = (
        rev_bairro_agrupado["qtd_Diamante"]
        + rev_bairro_agrupado["qtd_Esmeralda"]
        + rev_bairro_agrupado["qtd_Rubi"]
    )

    rev_bairro_agrupado["base_ampla"] = (
        rev_bairro_agrupado["qtd_Bronze"]
        + rev_bairro_agrupado["qtd_Prata"]
        + rev_bairro_agrupado["qtd_Ouro"]
        + rev_bairro_agrupado["qtd_Platina"]
    )

    # ------------------------------------------------------------------
    # 7. Merge com população dos bairros
    # ------------------------------------------------------------------

    dicionario_rename = {
        "v0001": "Total de pessoas",
        "v0002": "Total de Domicílios",
        "v0003": "Total de Domicílios Particulares",
        "v0004": "Total de Domicílios Coletivos",
        "v0005": "Média de moradores em Domicílios Particulares Ocupados",
        "v0006": "Percentual de Domicílios Particulares Ocupados Imputados",
        "v0007": "Total de Domicílios Particulares Ocupados"
    }

    populacao_bairros.columns = populacao_bairros.columns.str.strip()

    lista_colunas = ["CD_BAIRRO"] + list(dicionario_rename.values()) + ["geometry"]

    populacao_bairros.rename(columns=dicionario_rename,inplace=True)




    base_geral = rev_bairro_agrupado.merge(
        populacao_bairros[lista_colunas],
        on="CD_BAIRRO",
        how="left"


    )


    base_geral['Cobertura'] = ((base_geral['qtd_rev']*1000)/base_geral['Total de pessoas']).round(2)
    base_geral['produtividade_bairro'] = base_geral['produtividade_bairro'].round(2)



   

    base_gera1_gdf = gpd.GeoDataFrame(
        base_geral,
        geometry="geometry",
        crs="EPSG:4326"
    )


  





    return base_gera1_gdf








    












