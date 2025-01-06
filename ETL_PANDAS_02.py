# importar mi archivo de configuración config.py 
from config import *

##################################################################################
# Leer los datos desde un archivo CSV
dataFrame_Transform = pd.read_csv(file_datos_unificados)
print ("Carga los datos unificados...")

##################################################################################
# Eliminar columnas innecesarias
dataFrame_Transform = dataFrame_Transform.drop(columns=['institucion', 'fuente', 'latitud', 'longitud'])
dataFrame_Transform = dataFrame_Transform.drop(columns=['nombre_cuenca', 'codigo_sub_cuenca', 'nombre_sub_cuenca', 'geometry'])
dataFrame_Transform = dataFrame_Transform.drop(columns=['CUT_REG', 'CUT_PROV', 'SUPERFICIE'])
print ("Columnas innecesarias eliminadas...")

##################################################################################
# Esto es especialmente útil para reorganizar datos cuando se quiere tener siempre un bloque de columnas
# repitiendo en las columnas finales los datos que se requieren, esto para la construcción
# de un Datawarehouse

chunk_size = 10000
chunks = [dataFrame_Transform.iloc[i:i + chunk_size] for i in range(0, len(dataFrame_Transform), chunk_size)]
melted_chunks = [
    chunk.melt(
        id_vars=['codigo_estacion', 'nombre', 'altura', 'codigo_cuenca', 
            'inicio_observaciones', 'fin_observaciones', 'cantidad_observaciones', 
            'inicio_automatica', 'CUT_COM', 'REGION', 
            'PROVINCIA', 'COMUNA'],
        var_name = 'Fecha',
        value_name = 'Medicion'
    ) for chunk in chunks]

# Combina los fragmentos
df_MOD = pd.concat(melted_chunks)

#-df_MOD =  dataFrame_Transform.melt(
#-    id_vars=['codigo_estacion', 'nombre', 'altura', 'codigo_cuenca', 
#-            'inicio_observaciones', 'fin_observaciones', 'cantidad_observaciones', 
#-            'inicio_automatica', 'CUT_COM', 'REGION', 
#-            'PROVINCIA', 'COMUNA'],
#-    var_name = 'Fecha',
#-    value_name = 'Medicion'
#-)
print ("Datos reorganizados...")

##################################################################################
# SALVA LOS DATOS EN UN DATAFRAME PARA ENTRENAMIENTO
df_MOD.to_csv(datos_entrenamiento_file, index=False) # type: ignore
df_MOD = None
gc.collect()

print ("Fin del proceso de ETL 02")