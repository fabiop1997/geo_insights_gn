import folium
from folium.plugins import FastMarkerCluster
from geopy.distance import geodesic
import pandas as pd
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import streamlit as st
import geopandas as gp
from malhas_bairros import merge_malha_agregados
from cobertura import rev_bairro_geometry
from dotenv import load_dotenv
import os

load_dotenv()


def style_function(feature):
    return {
        'fillColor': "#749EE3",
        'color': 'black',
        'weight': 0.4,
        'fillOpacity': 0.4
    }



def style_function_2(feature):
    return {
        'fillColor': "#010813",
        'color': "#010813",
        'weight': 0.5,
   
    }


def highlight_function(feature):
    return {
        'fillColor': "#5f6492",
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.1
    }


@st.cache_data
def realizar_mapa(df_rev: pd.DataFrame ) -> folium.Map:

    df_rev= df_rev.dropna(subset=["Latitude", "Longitude"])
    df_rev["Latitude"] = df_rev["Latitude"].astype(float)
    df_rev["Longitude"] = df_rev["Longitude"].astype(float)

    ponto_inicial = (-5.1934804,-37.3420123)


    mapa = folium.Map(location=ponto_inicial, zoom_start=12)

    

    marker_cluster = MarkerCluster().add_to(mapa)

    




    # for i in range(len(df_rev)):
    #     folium.Marker(

    #         location=[df_rev['Latitude'].iloc[i],df_rev['Longitude'].iloc[i]],
    #         tooltip="Clique aqui",
    #         popup= folium.Popup(
    #             f"Revendedor: {df_rev['Cod Revendedor'].iloc[i]}" , max_width=200

    #         )

    #     ).add_to(marker_cluster)


    FastMarkerCluster(data=zip(df_rev['Latitude'],df_rev['Longitude'])).add_to(mapa)


     # marcador do ER
    folium.Marker(
        location=[ponto_inicial[0], ponto_inicial[1]],
        tooltip="ER",
        popup="VD MOSSORÓ",
        icon=folium.Icon(icon="store", prefix="fa", color="green")
    ).add_to(mapa)



    path_malhas = os.getenv("PATH_MALHA_BAIRROS")

    path_agregados = os.getenv("PATH_AGREGADOS_BAIRROS")

    #%%

    malha_bairros = gp.read_file(path_malhas)

    agregados_bairro = pd.read_excel(path_agregados)


    bairros_poligonos_agregados = merge_malha_agregados(malha_bairros,agregados_bairro)

    bairros_poligonos_agregados = bairros_poligonos_agregados[bairros_poligonos_agregados['NM_MUN'] == "Mossoró"]

    

    folium.GeoJson(
    data=bairros_poligonos_agregados,
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip
        (
            fields=['NM_BAIRRO', 'Total de pessoas'],
            aliases=['Bairro:', 'População:']
        ),
    name="BAIRROS"
    ).add_to(mapa)

    folium.LayerControl().add_to(mapa)

    




    return mapa









def choropleth_map(df_rev, coluna):


    



    ponto_inicial = (-5.1934804,-37.3420123)

    df_map = df_rev.dropna(subset=["geometry"])


    mapa = folium.Map(location=ponto_inicial,tiles="Cartodb Positron", zoom_start=12)

    folium.Marker(
    location=ponto_inicial,
    popup="ER MOSSORÓ",
    tooltip="Clique aqui",
    icon=folium.Icon(
        icon="shopping-cart",
        prefix="fa",        
        color="blue"
    )
    ).add_to(mapa)
    
    

    

    
    folium.Choropleth(
    geo_data=df_map[["CD_BAIRRO", "geometry"]],
    data=df_map,
    columns=["CD_BAIRRO", coluna],
    key_on="feature.properties.CD_BAIRRO",
    fill_color="YlGn",
    fill_opacity=0.9,
    line_opacity=0,   
    line_weight=0,
    nan_fill_color="lightgray",
    legend_name=f"{coluna}"
    # bins=[2,5,7,10,15,25,50]
    ).add_to(mapa)

    folium.GeoJson(
    df_map,
    name="Bairros (hover)",
    style_function=style_function_2,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["NM_BAIRRO",'Total de pessoas', coluna],
        aliases=["Bairro:","População:", coluna],
        sticky=True
    )
    ).add_to(mapa)

    return mapa









    






