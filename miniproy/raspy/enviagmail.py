import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import gpiod
import time

# Configuración del chip GPIO y del botón
chip = gpiod.Chip('gpiochip0')  # Define el chip GPIO
boton_pin = 21  # Usa el pin GPIO 17 para el botón

boton = chip.get_line(boton_pin)

# Configurar el botón como entrada con resistencia pull-down
boton.request(consumer="boton", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0], flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)

# Función para enviar el correo
def enviar_correo():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_usuario = "embebidos9@gmail.com"
    email_contrasena = "mzds cuaz kewt hkom"  # O token si usas autenticación en dos pasos
    destinatario = "rufo.huallpara@ucb.edu.bo"
    
    msg = MIMEMultipart()
    msg['From'] = email_usuario
    msg['To'] = destinatario
    msg['Subject'] = "Hora y fecha actuales"

    # Obtener la hora y fecha actuales
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensaje = f"Hola, la fecha y hora actuales son: {fecha_hora_actual}"

    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Conectar al servidor SMTP y enviar el correo
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()  # Iniciar conexión segura
        servidor.login(email_usuario, email_contrasena)
        servidor.send_message(msg)
        print("Correo enviado con éxito")
        servidor.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para manejar la pulsación del botón
def boton_callback():
    # Verificar el estado de la línea
    estado = boton.get_value()
    if estado:  # Solo enviar el correo si el estado es HIGH
        print("Botón pulsado, enviando correo...")
        enviar_correo()

# Detectar la pulsación del botón
try:
    while True:
        # Esperar el evento de pulsación (borde de subida)
        evento = boton.event_wait(sec=5)
        if evento:
            boton_callback()  # Llamar la función cuando se detecta la pulsación del botón
except KeyboardInterrupt:
    print("Saliendo del programa")
finally:
    boton.release()  # Liberar la línea GPIO al terminar el programa
