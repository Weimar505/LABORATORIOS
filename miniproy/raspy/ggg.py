import serial
import threading
import gpiod
from time import sleep
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import evdev
from evdev import InputDevice, categorize, ecodes
import select

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
tiva.reset_input_buffer()
sleep(2)  # Esperar a que se establezca la conexión serial

# Ruta correcta del dispositivo de tu mando de PS5
device = InputDevice('/dev/input/event11')

print(f'Conectado a: {device.name}')
print('Esperando datos...')

# Configuración de GPIO (si es necesario)
chip = gpiod.Chip('gpiochip0')
# Aquí se pueden definir los pines GPIO que necesites

smtp_server = "smtp.gmail.com"
smtp_port = 587
email_usuario = "embebidosdosdos@gmail.com"
email_contrasena = "wsib atid isrq mrei"  # Reemplaza con tu contraseña o token
destinatario = "kakurrazo@gmail.com"  # Reemplaza con el correo del destinatario

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

# Función para recibir datos del sensor de distancia y enviar correos según el estado
def recibir_datos():
    distancia_anterior = None
    estado_anterior = None
    correo_enviado_detenido = False
    correo_enviado_funcionando = False

    while True:
        if tiva.in_waiting > 0:
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                try:
                    distancia = float(valor)
                    print(f"Distancia: {distancia} cm")

                    estado_actual = "detenido" if distancia <= 5 else "funcionando"
                    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    if estado_actual == "detenido" and estado_anterior != "detenido":
                        if not correo_enviado_detenido:
                            mensaje = f"Carro detenido a {distancia} cm\nFecha y hora: {fecha_hora_actual}"
                            enviar_correo("Estado del carro", mensaje)
                            correo_enviado_detenido = True
                        correo_enviado_funcionando = False

                    elif estado_actual == "funcionando" and estado_anterior != "funcionando":
                        if not correo_enviado_funcionando:
                            mensaje = f"Carro en funcionamiento a {distancia} cm\nFecha y hora: {fecha_hora_actual}"
                            enviar_correo("Estado del carro", mensaje)
                            correo_enviado_funcionando = True
                        correo_enviado_detenido = False

                    estado_anterior = estado_actual
                    distancia_anterior = distancia
                except ValueError:
                    print("Error: Valor recibido no es un número")
        sleep(0.1)

# Diccionario de botones y frases correspondientes para el mando
button_phrases = {
    'BTN_NORTH': "adelante",
    'BTN_X': "adelante",
    'BTN_EAST': "derecha",
    'BTN_B': "derecha",
    'BTN_WEST': "izquierda",
    'BTN_Y': "izquierda",
    'BTN_SOUTH': "atras",
    'BTN_A': "atras",
    'BTN_TR': "onluces",
    'BTN_TL': "offluces"
}

# Función para manejar eventos del mando
def manejar_mando():
    print('Esperando datos del mando...')
    while True:
        r, w, x = select.select([device], [], [])
        for event in device.read():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == 1:  # Solo si se presiona
                    phrase = button_phrases.get(key_event.keycode, "desconocido")
                    if phrase != "desconocido":
                        tiva.write(phrase.encode('utf-8') + b'\n')
                        print(f'Enviando: {phrase}')  # Imprimir la frase que se está enviando

                if key_event.keystate == 0:  # Si el botón está liberado
                    phrase = "apagado"
                    tiva.write(phrase.encode('utf-8') + b'\n')
                    print(f'Enviando: {phrase}')  # Imprimir "apagado"

# Crear hilos para la recepción de datos y para manejar el mando
hilo_recepcion = threading.Thread(target=recibir_datos)
hilo_mando = threading.Thread(target=manejar_mando)

# Iniciar los hilos
hilo_recepcion.start()
hilo_mando.start()

# Esperar a que los hilos terminen (esto nunca sucederá a menos que el programa se cierre)
hilo_recepcion.join()
hilo_mando.join()
