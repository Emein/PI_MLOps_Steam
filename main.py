import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

    resultado = data_filtrada['anio'].iloc[0]
    
        
    return {f'Año de lanzamiento con más horas jugadas para Género {genero}': resultado}

@app.get('/ Recomendacion_juego/{item_id}')
def Recomendacion_juego(item_id : int):
    '''
      Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
        
    '''

    # se carga los datasets que se va a utilizar para dos dataframes distintos
    data = pd.read_csv('data/df_juegos_steam.csv')
    data_juegos_steam = pd.read_csv('data/df_juegos_id.csv')

    # crear una matriz de características de los juegos
    tfidv = TfidfVectorizer(min_df=2, max_df=0.7, token_pattern=r'\b[a-zA-Z0-9]\w+\b')
    data_vector = tfidv.fit_transform(data['features'])

    data_vector_df = pd.DataFrame(data_vector.toarray(), index=data['item_id'], columns = tfidv.get_feature_names_out())

    # calcular la similitud coseno entre los juegos en la matriz de características
    vector_similitud_coseno = cosine_similarity(data_vector_df.values)

    cos_sim_df = pd.DataFrame(vector_similitud_coseno, index=data_vector_df.index, columns=data_vector_df.index)

    juego_simil = cos_sim_df.loc[item_id]

    simil_ordenada = juego_simil.sort_values(ascending=False)
    resultado = simil_ordenada.head(6).reset_index()

    result_df = resultado.merge(data_juegos_steam, on='item_id',how='left')

    # La función devuelve una lista de los 6 juegos más similares al juego dado
    juego_title = data_juegos_steam[data_juegos_steam['item_id'] == item_id]['title'].values[0]

    # mensaje que indica el juego original y los juegos recomendados
    mensaje = f"{item_id} : {juego_title}:"

    result_dict = {
        'Juego': mensaje,
        'Juegos recomendados': result_df['title'][1:6].tolist()
    }

    return result_dict