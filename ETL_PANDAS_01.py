from config import *

##################################################################################
# CARGAR UN CSV EN DATAFRAME
def cargar_datos(file_datos):
    # Cargar un CSV en un DataFrame
    df = pd.read_csv(file_datos, sep=',', header=None, low_memory=False)
    return df

##################################################################################
# DE LOS DATOS DEL ARCHIVO QUE LEIMOS COMPLETO VAMOS A OBTENER LOS DATOS DE LAS ESTACIONS
def get_estaciones(df):
    # Toma el dato de los encabedos
    estaciones = df.columns
    # Eliminar la primer fila para que queden solo los datos
    estaciones = estaciones[1:]
    return estaciones

##################################################################################
# SE OBTIENEN LOS DOS INDICES DE DATOS QUE DEBEN SGUIR, LOS DATOS DE LA INFORMACIÓN DE LAS ESTACIONES
# Y LOS DATOS DE LA MEDICIÓN
def divide_datos(dfDatos):
    # Toma el dato de la primer columna y lo convierte en una Serie
    indices = dfDatos.iloc[:,0]
    # Ahora de esta serie la divide en 2 series una con las primeras 14 filas y el otro con el resto
    indice_descripcion = indices[:15]
    indice_datos = indices[15:]

    descripciones = dfDatos[:15]
    datos = dfDatos[15:]
    
    return [indice_descripcion, indice_datos, descripciones, datos]
    
##################################################################################
# CARGA DE DATOS
dfDatos = cargar_datos(file_datos)
listaEstaciones = get_estaciones(dfDatos)
indices = divide_datos(dfDatos)

indice_descripcion = indices[0]
indice_datos = indices[1]
DATA_descripciones = indices[2]
DATA_datos = indices[3]

print("Cantidad de datos en DATA_datos: ", len(DATA_datos))

# CONVERTIR LOS DATOS EN DATA_datos EN NUMÉRICOS A TIPO FLOAT TODO A PARTIR DE LA COLUMNA 1
DATA_datos.iloc[:, 1:] = DATA_datos.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# DE TODOS LOS DATOS EN DATA_datos, SE MODIFICAN LOS VALORES DE -9999 POR CERO
DATA_datos = DATA_datos.replace(-9999, 0)
print ("Datos erroneos modificados a 0")

##################################################################################
# pip install geopandas
import geopandas as gpd
crs = {'init': 'epsg:4326'}

# CARGAR EL ARCHIVO GEOREFERENCIADO SHP
def cargar_shapefile(filepath):
    try:
        shapefile = gpd.read_file(filepath)
        return shapefile
    except FileNotFoundError:
        print ("No encuentro el SHP")
        exit()
    except Exception as e:
        print (f"Error: problema al cargar archivo SHP: {e}")
        exit()

shapefile_data = cargar_shapefile(fileshape)
shapefile_data.crs = "epsg:4326"
print("El archivo SHP ha sido cargado...")

##################################################################################
# pip install matplotlib
#-import matplotlib.pyplot as plt 
# Dibujar un SHP en un archivo png
#-shapefile_data.plot()
#-plt.savefig('mapa.png')
#-print("El mapa se ha guardado en mapa.png")

# INVERTIR FILAS Y COLUMNAS DE DATA_descripciones PARA QUE LA COLUMNA 1 SEA EL INDICE 
# HACER QUE LA PRIMERA FILA SEAN LOS ENCABEZADOS
DATA_descripciones = DATA_descripciones.T
DATA_descripciones.columns = DATA_descripciones.iloc[0]
DATA_descripciones = DATA_descripciones[1:]

##################################################################################
# CONVERTIR LA LATIUD Y LONGITUD A FLOAT
DATA_descripciones['latitud'] = DATA_descripciones['latitud'].astype(float)
DATA_descripciones['longitud'] = DATA_descripciones['longitud'].astype(float)

# AGREGAR UNA NUEVA COLUMNA TIPO geometry CON EL PUNTO DE LA LATITUD Y LONGITUD
DATA_descripciones['geometry'] = gpd.points_from_xy(DATA_descripciones['longitud'], DATA_descripciones['latitud'], crs="EPSG:4326")
print("Se ha creado la columna geometry en descripciones para lat/lon")

##################################################################################
# AGREGAR COLUMNAS EXTRA A LAS DESCRIPCIONES DE LAS ESTACIONES
DATA_descripciones['CUT_REG'] = ''
DATA_descripciones['CUT_PROV'] = ''
DATA_descripciones['CUT_COM'] = ''
DATA_descripciones['REGION'] = ''
DATA_descripciones['PROVINCIA'] = ''
DATA_descripciones['COMUNA'] = ''
DATA_descripciones['SUPERFICIE'] = ''

print ("Iniciar el proceso de Georeferenciación de las estaciones...")
registro = 0
# Recorrece cada una de las estaciones
for i, row in DATA_descripciones.iterrows():
    registro += 1
    # por cada 50 registros muestra un mensaje
    if registro % 50 == 0:
        print(f"Procesando registro {registro} de {len(DATA_descripciones)}")
        # Eliminar objetos innecesarios
        gc.collect()
    
    # Hacer un QUERY de tipo GEOESPACIAL para obtener la información de la comuna
    comuna = shapefile_data[shapefile_data.contains(row['geometry'])]
    try:
        DATA_descripciones.at[i, 'CUT_REG'] = comuna['CUT_REG'].values[0]
        DATA_descripciones.at[i, 'CUT_PROV'] = comuna['CUT_PROV'].values[0]
        DATA_descripciones.at[i, 'CUT_COM'] = comuna['CUT_COM'].values[0]
        DATA_descripciones.at[i, 'REGION'] = comuna['REGION'].values[0]
        DATA_descripciones.at[i, 'PROVINCIA'] = comuna['PROVINCIA'].values[0]
        DATA_descripciones.at[i, 'COMUNA'] = comuna['COMUNA'].values[0]
        DATA_descripciones.at[i, 'SUPERFICIE'] = comuna['SUPERFICIE'].values[0]
    except:
        DATA_descripciones.at[i, 'CUT_REG'] = ''

print ("Proceso de Georeferenciación de las estaciones finalizado...")

# Limpiar data no necesaria
shapefile_data = None
comuna = None
gc.collect()

##################################################################################
# INVERTIR DATA_datos PARA QUE LA COLUMNA 1 SEA EL INDICE
# HACER QUE LA PRIMERA FILA SEA LOS ENCABEZADOS
DATA_datos = DATA_datos.T
DATA_datos.columns = DATA_datos.iloc[0]
DATA_datos = DATA_datos[1:]

# CONVERTIR LA COLUMNA codigo_estacion que funciona como indice en una columna más de datos
DATA_descripciones.reset_index(level=0, inplace=True)
DATA_datos.reset_index(level=0, inplace=True)

#RENOMBRA LA COLUMNA index A codigo_estacion
DATA_descripciones.rename(columns={'index': 'codigo_estacion'}, inplace=True)
DATA_datos.rename(columns={'index': 'codigo_estacion'}, inplace=True)

##################################################################################
# Eliminar columnas/filas duplicadas
DATA_descripciones = DATA_descripciones.loc[:,~DATA_descripciones.columns.duplicated()]
DATA_datos = DATA_datos.loc[:,~DATA_datos.columns.duplicated()]

# Eliminar espacios al rededor de los indices
DATA_descripciones.columns = DATA_descripciones.columns.str.strip()
DATA_datos.columns = DATA_datos.columns.str.strip()
print ("Datos duplicados eliminados...")

##################################################################################
# Reindexar los datos
DATA_descripciones = DATA_descripciones.reset_index(drop=True)
DATA_datos = DATA_datos.reset_index(drop=True)

DATA = pd.merge(DATA_descripciones, DATA_datos, on='codigo_estacion', suffixes=('_desc', '_datos'))
# Eliminar columnas innecesarias
DATA = DATA.loc[:, ~DATA.columns.duplicated()]

##################################################################################
DATA.to_csv(file_datos_unificados, index=False)
print("Datos se han unificado")
DATA = None
gc.collect()

print("FIN DEL ETL - PASO 01") 