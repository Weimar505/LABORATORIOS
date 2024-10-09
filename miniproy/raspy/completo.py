import serial
import threading
import gpiod
from time import sleep
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Inicializar el chip GPIO
chip = gpiod.Chip('gpiochip0')

# Pines GPIO para los botones
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

# Configuración del correo electrónico
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_usuario = "embebidos9@gmail.com"
email_contrasena = "mzds cuaz kewt hkom"  # Reemplaza con tu contraseña o token
destinatario = "rufo.huallpara@ucb.edu.bo"

# Función para enviar correos
def enviar_correo(asunto, mensaje):
    msg = MIMEMultipart()
    msg['From'] = email_usuario
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()  # Iniciar conexión segura
        servidor.login(email_usuario, email_contrasena)
        servidor.send_message(msg)
        print("Correo enviado con éxito")
        servidor.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

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
    distancia_anterior = None  # Variable para almacenar la distancia anterior
    estado_anterior = None  # Variable para almacenar el estado anterior
    correo_enviado_detenido = False  # Bandera para controlar envío de correo "detenido"
    correo_enviado_funcionando = False  # Bandera para controlar envío de correo "funcionando"

    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            # Lee la línea, decodifica y elimina caracteres de salto de línea
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                try:
                    distancia = float(valor)  # Asume que el valor recibido es un número
                    print(f"Distancia: {distancia} cm")

                    # Determina el estado actual basado en la distancia
                    if distancia <= 5:
                        estado_actual = "detenido"
                    else:
                        estado_actual = "funcionando"

                    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Verifica si hay un cambio de estado
                    if estado_actual == "detenido" and estado_anterior != "detenido":
                        if not correo_enviado_detenido:  # Envía correo solo si no se ha enviado antes
                            mensaje = f"Carro detenido a {distancia} cm\nFecha y hora: {fecha_hora_actual}"
                            enviar_correo("Estado del carro", mensaje)
                            correo_enviado_detenido = True  # Marca que se ha enviado el correo
                        correo_enviado_funcionando = False  # Reinicia el correo de funcionando

                    elif estado_actual == "funcionando" and estado_anterior != "funcionando":
                        if not correo_enviado_funcionando:  # Envía correo solo si no se ha enviado antes
                            mensaje = f"Carro en funcionamiento a {distancia} cm\nFecha y hora: {fecha_hora_actual}"
                            enviar_correo("Estado del carro", mensaje)
                            correo_enviado_funcionando = True  # Marca que se ha enviado el correo
                        correo_enviado_detenido = False  # Reinicia el correo de detenido

                    # Actualiza el estado anterior y la distancia
                    estado_anterior = estado_actual
                    distancia_anterior = distancia  # Actualiza la distancia anterior
                except ValueError:
                    print("Error: Valor recibido no es un número")

        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Función para introducir datos manualmente desde la terminal
def introducir_datos_terminal():
    while True:
        try:
            datos = input("Introduce datos: ")  # Captura la entrada del usuario desde la terminal
            tiva.write(datos.encode('utf-8'))  # Envía los datos al puerto serial
            print(f"Enviado: {datos}")
        except EOFError:
            print("Error de lectura")
        sleep(0.1)

# Crear hilos para la recepción de datos, verificación de botones y entrada de terminal
hilo_recepcion = threading.Thread(target=recibir_datos)
hilo_verificar_botones = threading.Thread(target=verificar_botones)
hilo_terminal = threading.Thread(target=introducir_datos_terminal)

# Iniciar los hilos
hilo_recepcion.start()
hilo_ver
