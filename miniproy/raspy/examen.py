import serial
import threading
import gpiod
from time import sleep
from gpiozero import PWMLED
from datetime import datetime

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Crear o sobreescribir el archivo con la ruta completa
ruta_archivo = "/home/pi/Desktop/labo1/miniproy/raspy/lecturas_ultrasonico.txt"

# Abrir el archivo en modo escritura ('w' para sobreescribir)
with open(ruta_archivo, "w") as archivo:
    archivo.write(f"Inicio de mediciones: {datetime.now()}\n")

# Función para procesar y actualizar el archivo cuando el valor "adelante" es recibido
def opcion_boton(valor):
    try:
        if valor == "adelante":
            print("Vehículo pausado")
            with open(ruta_archivo, "a") as archivo:
                archivo.write(f"Vehículo pausado: {datetime.now()}\n")
            sleep(2)
            print("Vehículo en funcionamiento")
            with open(ruta_archivo, "a") as archivo:
                archivo.write(f"Vehículo en funcionamiento: {datetime.now()}\n")
        else:
            print(f"Recibido: {valor}")
    except ValueError:
        print(f"Valor no válido: {valor}")

# Función para recibir datos en un hilo separado
def recibir_datos():
    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            # Lee la línea, decodifica y elimina caracteres de salto de línea
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                opcion_boton(valor)  # Procesar el valor recibido
        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Crear hilos para la recepción de datos
recepcion = threading.Thread(target=recibir_datos)
# Iniciar los hilos
recepcion.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
recepcion.join()
