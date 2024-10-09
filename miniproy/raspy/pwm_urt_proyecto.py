import serial
import threading
import gpiod
from time import sleep
from gpiozero import PWMLED

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Configuración del botón usando gpiod en el pin 26
motor1der = 4
motor1izq = 5
motor2der = 6
motor2izq = 7

vel1 = PWMLED(13)
vel2 = PWMLED(19)

chip = gpiod.Chip('gpiochip0')

der1 = chip.get_line(motor1der)
der2 = chip.get_line(motor2der)
izq1 = chip.get_line(motor1izq)
#izq2 = chip.get_line(motor2izq)
der1.request(consumer="derecha M1", type=gpiod.LINE_REQ_DIR_OUT)
der2.request(consumer="derecha M2", type=gpiod.LINE_REQ_DIR_OUT)
izq1.request(consumer="izquierda M1", type=gpiod.LINE_REQ_DIR_OUT)
#izq2.request(consumer="izquierda M2", type=gpiod.LINE_REQ_DIR_OUT)
# Configuración de PWM en los pines GPIO 18 y GPIO 12

# Función para procesar y actualizar los PWM en función del valor ADC recibido
def opcion_boton(valor):
    try:
        if valor == "adelante":
            vel1.value = 1  # Motor 1 al 50%
            vel2.value = 1  # Apagar Motor 2
            der1.set_value(1)
            der2.set_value(1)
            izq1.set_value(0)
            izq2.set_value(0)
            print("ATRAS")
            
            print("ADELANTE")
        elif valor == "atras":
            vel1.value = 1  # Motor 1 al 50%
            vel2.value = 1  # Apagar Motor 2
            der1.set_value(0)
            der2.set_value(0)
            izq1.set_value(1)
            izq2.set_value(1)
            print("ATRAS")
            
    except ValueError:
        print(f"Valor no válido: {valor}")

# Función para recibir datos en un hilo separado
def recibir_datos():
    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            # Lee la línea, decodifica y elimina caracteres de salto de línea
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                print(f"Recibido: {valor}")
                opcion_boton(valor)  # Procesar el valor recibido para ajustar los PWM
        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Crear hilos para la recepción y el envío de datos
recepcion = threading.Thread(target=recibir_datos)
# Iniciar los hilos
recepcion.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
recepcion.join()

# Cierra el puerto serial al
