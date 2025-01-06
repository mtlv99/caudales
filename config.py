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
###########################################################################

## dataset pequeño, para probar si ambiente funciona correctamente.
file_datos = "datos/little_data.csv"
datos_incidentes_file = 'datos/incidentes_pq.csv'

## Una vez se probó que todo funciona correctamente, se puede probar con el dataset entero
# file_datos = "datos/datos.txt"
# datos_incidentes_file = 'datos/eventos_estaciones.csv'

fileshape = "datos/SHP/COMUNAS_V1.shp"

file_datos_unificados = 'datos/datos_unificados.csv'

datos_entrenamiento_file = 'datos/datos_entrenamiento.csv'

datos_union_file = 'datos/datos_union.csv'