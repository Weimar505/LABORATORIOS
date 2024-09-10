import gpiod
import time

# Configuración de pines GPIO
LED_PIN = 17  # Pin GPIO donde está conectado el LED

# Crea una instancia del chip GPIO
chip = gpiod.Chip('gpiochip0')

# Configura la línea del LED
led = chip.get_line(LED_PIN)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

def pwm_led(led_line, frequency, duty_cycle):
    """
    Simula PWM en un LED usando la biblioteca gpiod.
    
    :param led_line: Línea GPIO para controlar el LED.
    :param frequency: Frecuencia del PWM en Hz.
    :param duty_cycle: Ciclo de trabajo del PWM en porcentaje (0-100).
    """
    period = 1.0 / frequency  # Periodo del PWM en segundos
    on_time = period * (duty_cycle / 100.0)  # Tiempo en alto
    off_time = period - on_time  # Tiempo en bajo

    while True:
        led_line.set_value(1)  # Enciende el LED
        time.sleep(on_time)  # Espera durante el tiempo en alto
        led_line.set_value(0)  # Apaga el LED
        time.sleep(off_time)  # Espera durante el tiempo en bajo

try:
    frequency = 100  # Frecuencia de PWM en Hz
    duty_cycle = 100   # Ciclo de trabajo en porcentaje
    pwm_led(led, frequency, duty_cycle)
except KeyboardInterrupt:
    print("Interrupción del usuario")
finally:
    led.release()  # Libera la línea del GPIO cuando el script termina
