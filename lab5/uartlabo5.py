import serial
import threading
import gpiod
from time import sleep
from gpiozero import PWMLED

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Configuración del botón usando gpiod en el pin 26
BUTTON_PIN = 26
chip = gpiod.Chip('gpiochip0')
button = chip.get_line(BUTTON_PIN)
button.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)

# Configuración de PWM en los pines GPIO 18 y GPIO 12
pwm1 = PWMLED(18)  # LED controlado por PWM en el pin GPIO 18 (motor 1)
pwm2 = PWMLED(12)  # LED controlado por PWM en el pin GPIO 12 (motor 2)

# Función para procesar y actualizar los PWM en función del valor ADC recibido
def opcion_boton(valor):
    try:
        if valor == "motor1":
            pwm1.value = 0.5  # Motor 1 al 50%
            pwm2.value = 0  # Apagar Motor 2
            print("Motor 1 encendido al 50%")
        elif valor == "motor2":
            pwm2.value = 0.5  # Motor 2 al 50%
            pwm1.value = 0  # Apagar Motor 1
            print("Motor 2 encendido al 50%")
        elif valor == "apagado":
            pwm1.value = 0  # Apagar ambos motores
            pwm2.value = 0
            print("Ambos motores apagados")
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

# Función para enviar datos al puerto serial
def enviar_datos():
    while True:
        enviar = input("")  # Captura el texto de entrada del usuario
        tiva.write(enviar.encode('utf-8'))  # Convierte la cadena a bytes con UTF-8
        print(f"Enviado: {enviar}\n")  # Imprime la cadena que fue enviada

# Función para verificar el estado del botón y enviar la palabra "buzzer" cuando se presiona
def verificar_boton():
    boton_presionado = False  # Variable para evitar envíos múltiples por una misma pulsación

    while True:
        button_state = button.get_value()  # Lee el estado del botón (0 = no presionado, 1 = presionado)

        if button_state == 1 and not boton_presionado:  # Si el botón se presiona
            tiva.write(b"buzzer\n")  # Envía "buzzer" por UART
            print("Enviado: buzzer")
            boton_presionado = True  # Marca que el botón ha sido presionado
        elif button_state == 0 and boton_presionado:  # Si el botón se libera
            tiva.write(b"apagado\n")  # Envía "apagado" por UART
            print("Enviado: apagado")
            boton_presionado = False  # Marca que el botón ha sido liberado

        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Crear hilos para la recepción y el envío de datos
recepcion = threading.Thread(target=recibir_datos)
envio = threading.Thread(target=enviar_datos)
envio_boton = threading.Thread(target=verificar_boton)

# Iniciar los hilos
recepcion.start()
envio.start()
envio_boton.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
recepcion.join()
envio.join()
envio_boton.join()

# Cierra el puerto serial al
