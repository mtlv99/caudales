# RNN Caudales
RNN para predicción de inundaciones.

Clase Razonamiento Artificial - UCreativa. Profesor Leonardo Correa.


Mas información del dataset en [datos/descripcion.txt](datos/descripcion.txt)

## Requisitos

- Python 3.10+

## Instalación

1. Clona este repositorio.
2. Asegúrate de tener Python instalado en tu sistema.
3. Instala dependencias adicionales:

```bash
pip install pandas geopandas matplotlib scikit-learn tensorflow
```

Se puede verificar la version en [requirements.txt](requirements.txt).

## 1. Manejador de Archivos Grandes para Git

Este script permite manejar archivos que exceden el límite de tamaño de GitHub (100MB) dividiéndolos en partes más pequeñas para su almacenamiento y posterior reconstrucción. Esto es necesario debido a que el dataset es muy grande para subirlo en un solo archivo, y hay que reconstruirlo.

Nota: por defecto se utiliza un sample muy pequeño del dataset para verificar si el ambiente se configuró correctamente. Para utilizar el dataset completo, descomentar las variables globales en [config.py](config.py).

### Uso

El script se puede usar de dos maneras:

1. Para dividir archivos antes de subirlos a Git:
```bash
python git_large_files.py -s
```

2. Para reconstruir los archivos después de clonar el repositorio:
```bash
python git_large_files.py -m
```

### ¿Cómo funciona?

#### Al subir cambios
1. Ejecuta el script con `-s` para dividir los archivos grandes
2. Los archivos originales se dividirán en chunks en el directorio `git_chunks/`
3. Añade y sube los chunks a Git
4. Asegúrate de que los archivos originales estén en `.gitignore`

#### Al clonar o actualizar
1. Clona o actualiza el repositorio
2. Ejecuta el script con `-m` para reconstruir los archivos
3. Los archivos se reconstruirán en sus ubicaciones originales

### Configuración

Los archivos que se manejarán están definidos en el script:
```python
self.large_files = [
    'datos/SHP/COMUNAS_v1.shp',
    'datos/datos.txt'
]
```

### Notas importantes

- Asegúrate de añadir los archivos originales a `.gitignore`
- Los chunks generados serán menores a 100MB para cumplir con las restricciones de GitHub
- Mantén una copia de seguridad de los archivos originales

## 2. Ejecutar ETL

Ejecutar las distintas partes del ETL en orden.


```bash
python .\ETL_PANDAS_01.py
```

```bash
python .\ETL_PANDAS_02.py
```

```bash
python .\ETL_PANDAS_03.py
```


## 3. Ejecutar Entrenamiento RNN

Ejecutar entrenamiento del modelo.

```bash
python .\RNN_entrenamiento.py
```

## 4. Predecir evento

Ejecutar las distintas partes de la RNN en orden.

```bash
python .\RNN_prediccion.py
```
