import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

# pip install pandas
import pandas as pd
import numpy as np

import gc
gc.collect()

###########################################################################
# Declaración de variables globales
file_datos = "datos/datos.txt"
#-file_datos = "datos/little_data.csv"

fileshape = "datos/SHP/COMUNAS_V1.shp"

file_datos_unificados = 'datos/datos_unificados.csv'