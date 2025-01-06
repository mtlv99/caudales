# pip install scikit-learn
# pip install tensorflow

unionDatosFile = 'datos/datos_union.csv'

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Solo muestra errores (oculta advertencias y mensajes informativos)

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input

import logging
tf.get_logger().setLevel(logging.ERROR)  # Solo muestra errores críticos

##################################################################################
# carga el arhivo
union_datos = pd.read_csv(unionDatosFile)

##################################################################################
# Seleccionar características (X) y etiquetas (y)
X = union_datos[["codigo_estacion", "Medicion"]]
Y = union_datos["Tipo_evento"]  # Etiqueta

##################################################################################
# Escalar los datos
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

##################################################################################
# Codificar las etiquetas
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(Y)

##################################################################################
# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

##################################################################################
# Crear la red neuronal
model = Sequential([
    Input(shape=(X_train.shape[1],)),  # Definir la forma de entrada explícitamente
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(4, activation='softmax')  # Cuatro clases de salida: "V", "A", "R", "-"
])

# Compilar el modelo
model.compile(
    optimizer='adam', 
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy']
)

##################################################################################
# Entrenar el modelo
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=5,
    batch_size=16,
    verbose=1
)

##################################################################################
# Evaluar el modelo
evaluation = model.evaluate(X_test, y_test)
print ("")
print ("##################################################################################")
print(f"\nPerdida: {evaluation[0]}, Exactitud: {evaluation[1]}")

##################################################################################
# Guardar el modelo
model.save('modelo/modelo_inundaciones.h5')
np.save('modelo/scaler.npy', scaler)

##################################################################################
# Función para predecir una nueva medición y estación
def predecir_evento(estacion_id, medicion):
    entrada = scaler.transform([[estacion_id, medicion]])
    prediccion = model.predict(entrada)
    clase = label_encoder.inverse_transform([np.argmax(prediccion)])[0]
    # Mapear la clase a un mensaje descriptivo
    descripcion_eventos = {
        "V": "Evento probable - leve",
        "A": "Evento probable - dimensiones medianas",
        "R": "Evento inminente - Evacuar",
        "-": "No hay peligro"
    }
    return descripcion_eventos.get(clase, "Evento desconocido")

# Ejemplo de predicción
estacion_ejemplo = 1
medicion_ejemplo = 200
print(f"Estación: {estacion_ejemplo}, Medición: {medicion_ejemplo}, Evento predicho: {predecir_evento(estacion_ejemplo, medicion_ejemplo)}")