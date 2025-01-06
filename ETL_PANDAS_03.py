# importar mi archivo de configuración config.py 
from config import *

##################################################################################
# Cargar el archivo de incidentes
datos_incidentes = pd.read_csv(datos_incidentes_file) # type: ignore
##################################################################################
# Filtrar datos y eventos válidos
datos_incidentes = datos_incidentes[datos_incidentes['Tipo_evento'].isin(['V', 'A', 'R', '-'])]

for df in [datos_incidentes]:
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# Abrir archivo CSV para ir escribien los datos
with open(datos_union_file, 'w') as f:
    f.write("")

chunk_num = 0
ckSize = 50000
for datos_entrenamiento in pd.read_csv(datos_entrenamiento_file, chunksize=ckSize): # type: ignore
    chunk_num += ckSize
    for df in [datos_entrenamiento]:
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    ##################################################################################
    # Agregar datos de caudales a los incentes usando la fecha y el identificado CUT_COM

    caudales = datos_entrenamiento[['Fecha', 'codigo_estacion', 'Medicion', 'CUT_COM']]

    # Combinar incidentes y datos de caudales
    union_datos = pd.merge(caudales, datos_incidentes, on=['CUT_COM', 'Fecha'], how='left')
    union_datos["Tipo_evento"] = union_datos["Tipo_evento"].fillna('-')

    # Mapear los eventos por tipo de evento por un valor numérico
    mapeo = {'V': 1, 'A': 2, 'R': 3, '-': 0}
    union_datos['Tipo_evento'] = union_datos['Tipo_evento'].map(mapeo)

    # eliminar todo lo quedo fuera de los valores indicados
    union_datos = union_datos[union_datos['Tipo_evento'].isin([0, 1, 2, 3])]

    # Eliminar las filas con datos nulos
    union_datos.dropna(inplace=True)

    ##################################################################################
    # Escribir el pedacito chunk en datos_union_file
    with open(datos_union_file, 'a') as f: # type: ignore
        union_datos.to_csv(f, header=f.tell()==0, index=False)
    
    print("Procesando datos de entrenamiento: ", chunk_num)    
    union_datos = None
    
    gc.collect()

print ("Fin del proceso de ETL - Listo para entrenamiento")