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

            # Enviar frase al puerto serial si el botón está presionado
            if key_event.keystate == 1:  # Solo si se presiona
                if 'BTN_NORTH' in key_event.keycode or 'BTN_X' in key_event.keycode:  # Botón X
                    phrase = "adelante"
                elif 'BTN_EAST' in key_event.keycode or 'BTN_B' in key_event.keycode:  # Botón Círculo
                    phrase = "derecha"
                elif 'BTN_WEST' in key_event.keycode or 'BTN_Y' in key_event.keycode:  # Botón Cuadrado
                    phrase = "izquierda"
                elif 'BTN_SOUTH' in key_event.keycode or 'BTN_A' in key_event.keycode:  # Botón Triángulo
                    phrase = "atras"
                elif 'BTN_TR' in key_event.keycode:  # Botón R1
                    phrase = "onluces"
                elif 'BTN_TL' in key_event.keycode:  # Botón R1
                    phrase = "offluces"
                else:
                    phrase = "desconocido"
                
                # Enviar la frase por el puerto serial
                serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar la frase
                print(f'Enviando: {phrase}')  # Imprimir la frase que se está enviando
            
            elif key_event.keystate == 0:  # Si el botón está liberado
                phrase = "apagado"
                serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar "apagado"
                print(f'Enviando: {phrase}')  # Imprimir "apagado"
