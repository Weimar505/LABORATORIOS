import serial
import threading
import gpiod
from time import sleep
from gpiozero import PWMLED
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from abc import ABC, abstractmethod

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Crear o sobreescribir el archivo con la ruta completa
ruta_archivo = "/home/pi/Desktop/labo1/miniproy/raspy/lecturas_ultrasonico.txt"

# Configuración del correo
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_usuario = "embebidos9@gmail.com"
email_contrasena = "mzds cuaz kewt hkom"
destinatario = "rufo.huallpara@ucb.edu.bo"

# Clase abstracta para la comunicación UART
class ComunicacionUART(ABC):
    @abstractmethod
    def enviar_mensaje(self, mensaje):
        pass

# Clase concreta que implementa la comunicación UART
class ComunicacionUARTConcreta(ComunicacionUART):
    def __init__(self, uart):
        self.uart = uart
        self.enviando_girar = True  # Bandera para controlar el envío continuo

    def enviar_mensaje(self, mensaje):
        self.uart.write(f"{mensaje}\n".encode("utf-8"))
        print(f"Enviado a la Tiva: {mensaje}")

    # Método para iniciar o detener el envío continuo de "girar"
    def enviar_girar_continuo(self):
        while self.enviando_girar:
            self.enviar_mensaje("girar")
            sleep(1)  # Envía "girar" cada segundo

    # Método para detener el envío de "girar"
    def detener_envio_girar(self):
        self.enviando_girar = False
        print("Envio de 'girar' detenido.")

    # Método para reanudar el envío de "girar"
    def reanudar_envio_girar(self):
        if not self.enviando_girar:
            self.enviando_girar = True
            threading.Thread(target=self.enviar_girar_continuo).start()

# Instancia de la clase concreta para enviar datos por UART
comunicacion_uart = ComunicacionUARTConcreta(tiva)

# Función para enviar correo electrónico
def enviar_correo(asunto, mensaje):
    try:
        # Crear el objeto de mensaje
        msg = MIMEMultipart()
        msg['From'] = email_usuario
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'plain'))

        # Conexión al servidor SMTP y envío del correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Asegurar la conexión
        server.login(email_usuario, email_contrasena)  # Iniciar sesión
        server.sendmail(email_usuario, destinatario, msg.as_string())  # Enviar correo
        server.quit()
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Función para recibir datos en un hilo separado
def recibir_datos():
    medicion_inicial = False
    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                print(f"Recibido: {valor}")
                
                # Solo registrar la primera medición al inicio
                if not medicion_inicial:
                    fecha_hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(ruta_archivo, 'w') as archivo:
                        archivo.write(f"Inicio de medición: {fecha_hora_inicio}, Medida inicial: {valor}\n")
                    enviar_correo("Inicio de medición", f"Fecha: {fecha_hora_inicio}, Medida inicial: {valor}")
                    medicion_inicial = True

                # Cuando se recibe la palabra "adelante"
                if valor == "adelante":
                    fecha_hora_adelante = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(ruta_archivo, 'a') as archivo:
                        archivo.write(f"Recogiendo basura: {fecha_hora_adelante}\n")
                    enviar_correo("Recogiendo basura", f"Vehículo pausado y recogiendo basura. Fecha: {fecha_hora_adelante}")
                    print("Recogiendo basura")

                    # Detener el envío de "girar" al recibir "adelante"
                    comunicacion_uart.detener_envio_girar()

                else:
                    # Reanudar el envío de "girar" al recibir lecturas normales
                    comunicacion_uart.reanudar_envio_girar()

        sleep(0.1)  # Pausa para evitar consumir demasiados recursos de CPU

# Crear hilos para la recepción y el envío de datos
recepcion = threading.Thread(target=recibir_datos)
# Hilo para enviar "girar" de manera continua
envio_girar = threading.Thread(target=comunicacion_uart.enviar_girar_continuo)

# Iniciar los hilos
recepcion.start()
envio_girar.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
recepcion.join()
envio_girar.join()
