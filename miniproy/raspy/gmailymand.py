import evdev
from evdev import InputDevice, categorize, ecodes
import select
import serial
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del puerto serial
serial_port = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
time.sleep(2)  # Esperar a que se establezca la conexión serial

# Ruta correcta del dispositivo de tu mando de PS5
device = InputDevice('/dev/input/event11')

print(f'Conectado a: {device.name}')
print('Esperando datos...')

# Diccionario de botones y frases correspondientes
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

# Configuración del correo electrónico
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

# Bucle de eventos para leer datos del dispositivo
while True:
    # Usa select para esperar hasta que el dispositivo esté listo
    r, w, x = select.select([device], [], [])
    
    # Leer los eventos disponibles
    for event in device.read():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            button_state = "Presionado" if key_event.keystate == 1 else "Liberado"
            print(f'Botón: {key_event.keycode}, Estado: {button_state}')

            # Manejar si el keycode es una lista
            if isinstance(key_event.keycode, list):
                # Si hay múltiples botones presionados, procesar cada uno
                for key in key_event.keycode:
                    phrase = button_phrases.get(key, "desconocido")
                    if key_event.keystate == 1:  # Solo si se presiona
                        serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar la frase
                        print(f'Enviando: {phrase}')  # Imprimir la frase que se está enviando
                        enviar_correo("Botón presionado", f'Se presionó el botón: {phrase}')  # Enviar correo
                        
            else:
                # Enviar frase si solo un botón está presionado
                if key_event.keystate == 1:  # Solo si se presiona
                    phrase = button_phrases.get(key_event.keycode, "desconocido")
                    serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar la frase
                    print(f'Enviando: {phrase}')  # Imprimir la frase que se está enviando
                    enviar_correo("Botón presionado", f'Se presionó el botón: {phrase}')  # Enviar correo
            
            # Verificar si el botón está liberado
            if key_event.keystate == 0:  # Si el botón está liberado
                phrase = "apagado"
                serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar "apagado"
                print(f'Enviando: {phrase}')  # Imprimir "apagado"
                enviar_correo("Botón liberado", "Se liberó un botón.")  # Enviar correo
