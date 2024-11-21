import evdev
from evdev import InputDevice, categorize, ecodes
import select

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
            print(f'Botón: {key_event.keycode}, Estado: {"Presionado" if key_event.keystate == 1 else "Liberado"}')
