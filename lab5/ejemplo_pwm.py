from gpiozero import PWMLED
from time import sleep

led = PWMLED(18)  # Usa el pin GPIO 18

while True:
    # LED al 50% de brillo durante 2 segundos
    led.value = 0.5
    sleep(2)

    # LED al 35% de brillo durante 3 segundos
    led.value = 0.35
    sleep(3)

    # LED al 100% de brillo durante 2 segundos
    led.value = 1.0
    sleep(2)
