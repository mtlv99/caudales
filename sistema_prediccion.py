import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Solo muestra errores (oculta advertencias y mensajes informativos)

import threading
from telebot import TeleBot

import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# BOT: 
# Name: Sistema Prevención Inundaciones
# Username BOT: sys_innundacion_bot
# URL: t.me/sys_innundacion_bot
API_TOKEN = "7697819440:AAFOOP6RdwQxZjJUBXvcU-LdOOJ-7rF16lM"
chatbot = TeleBot(API_TOKEN)

# Cargar el modelo y el scalar
model = load_model("modelo/modelo_inundaciones.h5", compile=False)
scalar = np.load("modelo/scaler.npy", allow_pickle=True).item()

descripcion_eventos = {
    "V": "Evento probable - leve",
    "A": "Evento probable - dimensiones medianas",
    "R": "Evento inminente - Evacuar",
    "-": "No hay peligro"
}

###########################################################################
# Functión para predecir un evento
def predecir_evento(estacion_id, medicion):
    try:
        # Transformar la entrada en un input valido
        entrada = scalar.transform([[estacion_id, medicion]])

        # Realizar la predicción
        prediccion = model.predict(entrada)

        clase = np.argmax(prediccion)
        if (clase == 0): clase = "V"
        elif (clase == 1): clase = "A"
        elif (clase == 2): clase = "R"
        elif (clase == 3): clase = "-"
        
        return clase
    except Exception as e:
        return "-"

###########################################################################
def enviar_mensaje_masivo(mensajeEnviar):
    with open("telegram/suscripcion.json", "r") as file:
        for line in file:
            chatbot.send_message(line, mensajeEnviar)
    print ("Mensaje enviado.")

###########################################################################
def loop_usuario():
    while True:
        print ("")
        print ("-------------------------")    
        print ("  Enviar: Para enviar mensajes a todos los suscriptores")
        print ("  Datos: El administrador inserta datos de una estación")
        print ("  Salir: cierra la aplicación")
        comando = input("comando:").strip().lower()
        print ("")

        if comando == "enviar":
            mensaje = input("Mensaje: ")
            enviar_mensaje_masivo(mensaje)
        elif comando == "datos":
            estacion = input("Codigo estacion: ") # 15202
            medicion = input("Medicion: ") # 3
            resultado = predecir_evento(estacion, medicion)
            if (resultado != "-"):
                prediccion = descripcion_eventos.get(resultado, "Evento desconocido")
                mensaje = f"Alerta: estación {estacion}, {prediccion}"
                enviar_mensaje_masivo(mensaje)
        elif comando == "salir":
            print ("Saliendo del programa...")
            #Termina toda la ejecución
            exit(0)
        else:
            print ("Comando no reconocido")

###########################################################################
# Función para registrar una nueva persona
@chatbot.message_handler(commands=["start"])
def start_handler(message):
    with open("telegram/suscripcion.json", "a") as file:
        file.write(str(message.chat.id) + "\n")
        chatbot.reply_to(message, "Has quedado registrado en el servicio de Alertas")
        print (f"Registro exitoso para: {str(message.chat.id)}")

###########################################################################
def iniciar_chatbot():    
    print("Sistema corriendo")
    chatbot.polling(none_stop=True)

###########################################################################
# Crear los hilos de programación
hilo_chatbot = threading.Thread(target=iniciar_chatbot)
hilo_chatbot.daemon = True  # Para ser administrado por el programa principal
hilo_chatbot.start()

###########################################################################
# Iniciar el programa principal
loop_usuario()



'''
while (True):
    
    
    print ("")
    print (f"Evento: {prediccion}")
    print ("--------------------------------------")
    print ("")
'''