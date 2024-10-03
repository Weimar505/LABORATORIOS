import serial
import threading
import gpiod
from time import sleep

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Inicializar el chip GPIO
chip = gpiod.Chip('gpiochip0')

# Pines GPIO para los 4 botones
boton_atras_pin = 21
boton_adelante_pin = 19
boton_izquierda_pin = 13
boton_derecha_pin = 26
swi_ch_pin = 20
# Configuración de los botones usando gpiod
boton_adelante = chip.get_line(boton_adelante_pin)
boton_atras = chip.get_line(boton_atras_pin)
boton_izquierda = chip.get_line(boton_izquierda_pin)
boton_derecha = chip.get_line(boton_derecha_pin)
swi_ch_luces = chip.get_line(swi_ch_pin)

boton_adelante.request(consumer="adelante", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
boton_atras.request(consumer="atras", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
boton_izquierda.request(consumer="izquierda", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
boton_derecha.request(consumer="derecha", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
swi_ch_luces.request(consumer="lluzes", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
# Función para verificar el estado de los botones y enviar el comando correspondiente
def verificar_botones():
    estado_botones = {"adelante": False, "atras": False, "izquierda": False, "derecha": False}
    estado_luces = {"luces": False}

    while True:
        # Verificar estado de cada botón
        if boton_adelante.get_value() == 1 and not estado_botones["adelante"]:
            tiva.write(b"adelante\n")
            print("Enviado: adelante")
            estado_botones["adelante"] = True
        elif boton_adelante.get_value() == 0 and estado_botones["adelante"]:
            tiva.write(b"apagado\n")  # Envía "apagado" por UART
            print("Enviado: apagado")
            estado_botones["adelante"] = False

        if boton_atras.get_value() == 1 and not estado_botones["atras"]:
            tiva.write(b"atras\n")
            print("Enviado: atras")
            estado_botones["atras"] = True
        elif boton_atras.get_value() == 0 and estado_botones["atras"]:
            tiva.write(b"apagado\n")  # Envía "apagado" por UART
            print("Enviado: apagado")
            estado_botones["atras"] = False

        if boton_izquierda.get_value() == 1 and not estado_botones["izquierda"]:
            tiva.write(b"izquierda\n")
            print("Enviado: izquierda")
            estado_botones["izquierda"] = True
        elif boton_izquierda.get_value() == 0 and estado_botones["izquierda"]:
            tiva.write(b"apagado\n")  # Envía "apagado" por UART
            print("Enviado: apagado")
            estado_botones["izquierda"] = False

        if boton_derecha.get_value() == 1 and not estado_botones["derecha"]:
            tiva.write(b"derecha\n")
            print("Enviado: derecha")
            estado_botones["derecha"] = True
        elif boton_derecha.get_value() == 0 and estado_botones["derecha"]:
            tiva.write(b"apagado\n")  # Envía "apagado" por UART
            print("Enviado: apagado")
            estado_botones["derecha"] = False
        if swi_ch_luces.get_value() == 1 and not estado_luces["luces"]:
            tiva.write(b"luces\n")
            print("Enviado: luces")
            estado_luces["luces"] = True
        elif swi_ch_luces.get_value() == 0 and estado_luces["luces"]:
            tiva.write(b"apagadolu\n")
            print("Enviado: apagado")
            estado_luces["luces"] = False
        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Función para recibir datos en un hilo separado
def recibir_datos():
    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            # Lee la línea, decodifica y elimina caracteres de salto de línea
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                print(f"Recibido: {valor}")
        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Función para enviar datos al puerto serial
def enviar_datos():
    while True:
        enviar = input("")  # Captura el texto de entrada del usuario
        tiva.write(enviar.encode('utf-8'))  # Convierte la cadena a bytes con UTF-8
        print(f"Enviado: {enviar}\n")  # Imprime la cadena que fue enviada

# Crear hilos para la recepción de datos y para verificar el estado de los botones
hilo_recepcion = threading.Thread(target=recibir_datos)
hilo_verificar_botones = threading.Thread(target=verificar_botones)

# Iniciar los hilos
hilo_recepcion.start()
hilo_verificar_botones.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
hilo_recepcion.join()
hilo_verificar_botones.join()
