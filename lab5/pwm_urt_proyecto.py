import serial
import threading
import gpiod
from time import sleep
from gpiozero import PWMLED
bot_d = 5
# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Configuración del botón usando gpiod en el pin 26
button1 = chip.get_line(BUTTON_PIN)
button1.request(consumer="derecha", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])

chip = gpiod.Chip('gpiochip0')

#izq2 = chip.get_line(motor2izq)

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

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
# Crear hilos para la recepción y el envío de datos
recepcion = threading.Thread(target=recibir_datos)
envio = threading.Thread(target=enviar_datos)
# Iniciar los hilos
recepcion.start()
envio.start()
# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
recepcion.join()
envio.join()
# Cierra el puerto serial al
