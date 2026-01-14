
#%%
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from load_data import carregar_dados
import streamlit as st


@st.cache_data
def spatial_join() -> pd.DataFrame:


    df_rev,gdf_bairros = carregar_dados()


    geometry = [
        Point(lon, lat)
        for lon, lat in zip(df_rev["Longitude"], df_rev["Latitude"])
    ]

    gdf_rev = gpd.GeoDataFrame(
        df_rev,
        geometry=geometry,
        crs="EPSG:4326"  # Sistema de coordenadas geográficas
    )

    # ------------------------------------------------------------------
    # 4. Spatial join: associa cada revendedor ao bairro correspondente
    # ------------------------------------------------------------------
    clientes_com_bairro = gpd.sjoin(
        gdf_rev,
        gdf_bairros[['CD_BAIRRO','NM_BAIRRO','geometry']],
        how="inner",
        predicate="within"
    )

    



    return clientes_com_bairro

#%%


