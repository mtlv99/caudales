import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Solo muestra errores (oculta advertencias y mensajes informativos)

import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Cargar el modelo y el scalar
model = load_model("modelo/modelo_inundaciones.h5", compile=False)
scalar = np.load("modelo/scaler.npy", allow_pickle=True).item()

descripcion_eventos = {
    "V": "Evento probable - leve",
    "A": "Evento probable - dimensiones medianas",
    "R": "Evento inminente - Evacuar",
    "-": "No hay peligro"
}

def predecir_evento(estacion_id, medicion):
    try:
        # Transformar la entrada en un input valido
        entrada = scalar.transform([[estacion_id, medicion]])

        # Realizar la predicción
        prediccion = model.predict(entrada)
        print ("Arreglo de predicción: ")
        print(prediccion)

        clase = np.argmax(prediccion)
        if (clase == 0): clase = "V"
        elif (clase == 1): clase = "A"
        elif (clase == 2): clase = "R"
        elif (clase == 3): clase = "-"

        print (f"Evento sería: {clase}")
        
        return clase
    except Exception as e:
        print ("Error en predicción...")
        return "-"

while (True):
    estacion = input("Codigo estacion: ") # 15202
    medicion = input("Medicion: ") # 3
    resultado = predecir_evento(estacion, medicion)
    prediccion = descripcion_eventos.get(resultado, "Evento desconocido")
    print ("")
    print (f"Evento: {prediccion}")
    print ("--------------------------------------")
    print ("")
