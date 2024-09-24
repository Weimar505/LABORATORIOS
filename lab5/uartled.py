import serial
import threading
from time import sleep
from gpiozero import PWMLED

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Configuración de PWM en los pines GPIO 18 y GPIO 12
pwm1 = PWMLED(18)  # LED controlado por PWM en el pin GPIO 18
pwm2 = PWMLED(12)  # LED controlado por PWM en el pin GPIO 12

# Función para procesar y actualizar los PWM en función del valor ADC recibido
def procesar_valor_adc(valor):
    try:
        # Convierte el valor ADC (0 a 4096) a un valor entre 0 y 1 para el PWM
        adc_value = int(valor)
        if 0 <= adc_value <= 4096:
            pwm_value = adc_value / 4096.0  # Escalar el valor ADC a un valor entre 0 y 1
            pwm1.value = pwm_value  # Ajustar el PWM del LED 1
            pwm2.value = pwm_value  # Ajustar el PWM del LED 2
            print(f"PWM ajustado a: {pwm_value * 100}% (Valor ADC: {adc_value})")
        else:
            print(f"Valor fuera de rango: {valor}")
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
                procesar_valor_adc(valor)  # Procesar el valor ADC recibido para ajustar los PWM
        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Función para enviar datos al puerto serial
def enviar_datos():
    while True:
        enviar = input("Escribe el dato a enviar: ")
        # Envía el dato por UART
        tiva.write(enviar.encode('utf-8'))
        print(f"Enviado: {enviar}\n")

# Crear hilos para la recepción y el envío de datos
recepcion = threading.Thread(target=recibir_datos)
envio = threading.Thread(target=enviar_datos)

# Iniciar ambos hilos
recepcion.start()
envio.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
recepcion.join()
envio.join()

# Cierra el puerto serial al salir del bucle
tiva.close()
