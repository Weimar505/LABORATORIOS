import evdev
from evdev import InputDevice, categorize, ecodes
import select
import serial
import time

# Configuración del puerto serial
# Asegúrate de cambiar '/dev/ttyUSB0' por el puerto serial correcto
# Puedes usar 'ttyACM0' o cualquier otro que esté disponible
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
            # Verificar si el botón está presionado
            if key_event.keystate == 1:  # 1 significa que el botón está presionado
                # Comprobar los nombres de los botones
                if 'BTN_NORTH' in key_event.keycode or 'BTN_X' in key_event.keycode:  # Botón X
                    phrase = "adelante"
                elif 'BTN_EAST' in key_event.keycode or 'BTN_B' in key_event.keycode:  # Botón Círculo
                    phrase = "derecha"
                elif 'BTN_WEST' in key_event.keycode or 'BTN_Y' in key_event.keycode:  # Botón Cuadrado
                    phrase = "izquierda"
                elif 'BTN_SOUTH' in key_event.keycode or 'BTN_A' in key_event.keycode:  # Botón Triángulo
                    phrase = "atras"
                
                print(phrase)  # Imprimir la frase en la consola
                serial_port.write(phrase.encode('utf-8') + b'\n')  # Enviar la frase por el puerto serial

    