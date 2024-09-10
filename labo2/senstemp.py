import random
import gpiod
import time

# Configuración de pines GPIO
LED1_PIN = 13  # Pin para el LED 1
LED2_PIN = 19  # Pin para el LED 2

# Configurar el uso de los números de pines en la placa
chip = gpiod.Chip('gpiochip0')

led = chip.get_line(LED1_PIN)
led2 = chip.get_line(LED2_PIN)

led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
led2.request(consumer="LED2", type=gpiod.LINE_REQ_DIR_OUT)

def control_leds(value):
    if value < 12:
        led.set_value(1)
        led2.set_value(0)
        print(f"Valor aleatorio: {value} - LED1 encendido (menor de 20)")
    elif value > 20:
        led.set_value(0)
        led2.set_value(1)
        print(f"Valor aleatorio: {value} - LED2 encendido (mayor de 30)")
    else:
        led.set_value(0)
        led2.set_value(0)
        print(f"Valor aleatorio: {value} - Ningún LED encendido (entre 20 y 30)")

try:
    while True:
        random_value = random.randint(0, 50)  # Genera un número aleatorio entre 0 y 50
        control_leds(random_value)
        time.sleep(5)  # Espera 2 segundos antes de generar un nuevo número

except KeyboardInterrupt:
    print("Programa interrumpido")
    led.release()
    led2.release()
