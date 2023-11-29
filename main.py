import pandas as pd
from fastapi import FastAPI


app = FastAPI()

df_funcion1 = pd.read_csv('data/df_funcion1.csv')
df_funcion2 = pd.read_csv('data/df_funcion2.csv')


@app.get("/ PlayTimeGenre")
def  PlayTimeGenre(genero: str):
    '''
      Debe devolver año con mas horas jugadas para dicho género.
        
    '''
    # Filtra el dataframe por desarrollador de interés
    data_filtrada = df_funcion1[df_funcion1['genero'] == genero]

    resultado = data_filtrada['anio'].to_dict()
    
        
    return {f'Año de lanzamiento con más horas jugadas para Género {genero}': resultado}