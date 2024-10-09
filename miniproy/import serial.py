import serial
import threading
from time import sleep
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Ruta del archivo de registro
ruta_archivo = "/home/pi/Desktop/labo1/miniproy/raspy/registro_estados.txt"

# Configuración del correo electrónico
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_usuario = "embebidos9@gmail.com"  # Reemplaza con tu dirección de correo
email_contrasena = "mzds cuaz kewt hkom"  # Reemplaza con tu contraseña o token
destinatario = "rufo.huallpara@ucb.edu.bo"  # Reemplaza con el correo del destinatario

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

# Función para escribir en el archivo
def registrar_cambio(mensaje):
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(ruta_archivo, 'a') as archivo:
            archivo.write(f"{mensaje} | Fecha y hora: {fecha_hora_actual}\n")
        print(f"Registrado: {mensaje}, Fecha y hora: {fecha_hora_actual}")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")

# Función para recibir datos en un hilo separado
def recibir_datos():
    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            # Lee la línea, decodifica y elimina caracteres de salto de línea
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                print(f"Valor recibido: {valor}")

                # Si recibe "adelante", enviar correo de "detenido"
                if valor.lower() == "adelante":
                    mensaje = "Estado cambiado a detenido."
                    # Enviar correo
                    threading.Thread(target=enviar_correo, args=("Cambio de Estado", mensaje)).start()
                    # Registrar en el archivo
                    registrar_cambio(mensaje)

                # Si recibe datos del sensor (asumiendo que son números)
                else:
                    try:
                        distancia = float(valor)  # Intenta convertir el valor a float
                        estado_actual = "funcionando"
                        mensaje = f"Carro funcionando. Distancia: {distancia} cm."
                        # Enviar correo
                        threading.Thread(target=enviar_correo, args=("Estado Funcionando", mensaje)).start()
                        # Registrar en el archivo
                        registrar_cambio(mensaje)

                    except ValueError:
                        print("Error: Valor recibido no es un número válido")

        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Crear hilo para la recepción de datos
hilo_recepcion = threading.Thread(target=recibir_datos)

# Iniciar el hilo
hilo_recepcion.start()

# Esperar a que el hilo termine (esto nunca sucederá a menos que el programa se cierre)
hilo_recepcion.join()
