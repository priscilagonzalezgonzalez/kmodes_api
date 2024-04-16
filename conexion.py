from kmodes.kmodes import KModes
import numpy as np
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

df = pd. DataFrame()
km = None
clusters = None

def connector():
    return mysql.connector.connect(
        host= "chiva-puma.cbaskge6gh1c.us-east-2.rds.amazonaws.com",
        user= "root",
        password= "12345678",
        database = "chivapuma",
        port = "3306"
    )

def get_product(id):
    row = df.loc[id]
    selected_columns = ['equipo', 'categoria', 'sexo']
    producto_entrada = row[selected_columns].values
    return producto_entrada

def get_products():
    try:
        db = connector()
        query = "SELECT id, equipo, categoria, sexo FROM productos;"
        global df
        df = pd.read_sql(query, db)
        df = df.set_index('id')
        equipo_mapping = {'chivas': 0, 'america': 1, 'mexico': 2,'pumas': 3, 'kings': 4, 'espana': 5,'tigres': 6,'rayados': 7,'alemania':8}
        df['equipo'] = df['equipo'].map(equipo_mapping).fillna(df['equipo'])
        categoria_mapping = {'camisa': 0, 'gorra': 1, 'chanclas': 1,'espinilleras': 1,'balon': 1}
        df['categoria'] = df['categoria'].map(categoria_mapping).fillna(df['categoria'])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        db.close()

def train_model():
    get_products()
    global df
    selected_columns = ['equipo', 'categoria', 'sexo']
    data_np = df[selected_columns].values
    global km
    km = KModes(n_clusters=6, init='Huang', n_init=5, verbose=1)
    global clusters
    clusters = km.fit_predict(data_np)

def get_prediction(productId):
    global df
    global km
    global clusters
    producto_entrada = get_product(productId)
    cluster_producto_entrada = km.predict([producto_entrada])[0]
    productos_recomendados = df[clusters == cluster_producto_entrada]
    
    #data_dict = productos_recomendados.index.to_dict(orient='records')
    data_dict = productos_recomendados.index.to_frame().to_dict(orient='records')

    return data_dict