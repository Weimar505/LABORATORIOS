import gpiod
import time

# Configuración del pin LED
LED_PIN = 17
# Usa el gpiochip correcto
chip = gpiod.Chip('gpiochip0')  # Asegúrate de usar el gpiochip correcto
led = chip.get_line(LED_PIN)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        led.set_value(1)  # Encender el LED
        time.sleep(1)  # Esperar 1 segundo
        led.set_value(0)  # Apagar el LED
        time.sleep(1)  # Esperar 1 segundo
except KeyboardInterrupt:
	print("Código finalizado")
	led.release()  # Liberar el pin
	print("GPIOs liberados")
