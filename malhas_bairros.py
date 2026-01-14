#%%

import geopandas as gp
import pandas as pd





#%%

def merge_malha_agregados(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:


    


    df1['CD_BAIRRO'] = df1['CD_BAIRRO'].astype(str)
    df2['CD_BAIRRO'] = df2['CD_BAIRRO'].astype(str)




    df =  df1.join(df2.set_index('CD_BAIRRO')[['AREA_KM2', 'v0001',
       'v0002', 'v0003', 'v0004', 'v0005', 'v0006', 'v0007']],
       on='CD_BAIRRO')
    

    df.rename( columns=
            {
        "v0001": "Total de pessoas",
        "v0002": "Total de Domicílios",
        "v0003": "Total de Domicílios Particulares",
        "v0004": "Total de Domicílios Coletivos",
        "v0005": "Média de moradores em Domicílios Particulares Ocupados",
        "v0006": "Percentual de Domicílios Particulares Ocupados Imputados",
        "v0007": "Total de Domicílios Particulares Ocupados"
    } , inplace= True

    ) 
    
    return df
    

#%%


#%%



    

