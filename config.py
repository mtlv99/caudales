import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# pip install pandas
import pandas as pd
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

import gc
gc.collect()

###########################################################################
# Declaración de variables globales
#-file_datos = "datos/datos.txt"
file_datos = "datos/little_data.csv"

fileshape = "datos/SHP/COMUNAS_V1.shp"

file_datos_unificados = 'datos/datos_unificados.csv'

datos_entrenamiento_file = 'datos/datos_entrenamiento.csv'

#-datos_incidentes_file = 'datos/eventos_estaciones.csv'
datos_incidentes_file = 'datos/incidentes_pq.csv'

datos_union_file = 'datos/datos_union.csv'