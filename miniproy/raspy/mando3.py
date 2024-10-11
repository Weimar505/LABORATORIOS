import evdev
from evdev import InputDevice, categorize, ecodes
import select
import serial
import time

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
            
            else:
                # Enviar frase si solo un botón está presionado
                if key_event.keystate == 1:  # Solo si se presiona
                    phrase = button_phrases.get(key_event.keycode, "desconocido")
                    serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar la frase
                    print(f'Enviando: {phrase}')  # Imprimir la frase que se está enviando
            
            # Verificar si el botón está liberado
            if key_event.keystate == 0:  # Si el botón está liberado
                phrase = "apagado"
                serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar "apagado"
                print(f'Enviando: {phrase}')  # Imprimir "apagado"