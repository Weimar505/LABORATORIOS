import gpiod
import time

# Configuraciones de los pines
LED_PINS = [13, 19, 20, 6]  # Pines GPIO para los LEDs
BUTTON_PIN_SELECT = 12       # Pin GPIO para el botón de selección de LED
BUTTON_PIN_TIME = 27         # Pin GPIO para el botón de incremento de tiempo

# Estado inicial
current_led = 0              # LED actualmente seleccionado
on_time = 1                  # Tiempo de encendido del LED (inicia en 1 segundo)

# Configuración del chip GPIO
chip = gpiod.Chip('gpiochip0')

# Configurar los LEDs como salida
leds = [chip.get_line(pin) for pin in LED_PINS]
for led in leds:
    led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# Configurar los botones como entrada
button_select = chip.get_line(BUTTON_PIN_SELECT)
button_select.request(consumer="ButtonSelect", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])

button_time = chip.get_line(BUTTON_PIN_TIME)
button_time.request(consumer="ButtonTime", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])

# Función para cambiar al siguiente LED
def change_led():
    global current_led, on_time
    current_led = (current_led + 1) % len(leds)  # Seleccionar el siguiente LED (cíclico)
    on_time = 1  # Reiniciar el tiempo a 1 segundo
    print(f"LED {current_led + 1} seleccionado, tiempo reiniciado a {on_time} segundo(s)")

# Función para incrementar el tiempo de encendido
def increase_time():
    global on_time
    on_time += 1
    print(f"Tiempo de encendido del LED {current_led + 1}: {on_time} segundo(s)")

# Función para encender el LED actual por el tiempo especificado
def turn_on_led(led_index, duration):
    leds[led_index].set_value(1)  # Encender LED
    time.sleep(duration)
    leds[led_index].set_value(0)  # Apagar LED

# Bucle principal
try:
    while True:
        # Leer estado del botón de selección
        if button_select.get_value() == 1:
            change_led()
            # Espera activa hasta que el botón se libere para evitar rebotes
            while button_select.get_value() == 1:
                time.sleep(0.1)

        # Leer estado del botón de tiempo
        if button_time.get_value() == 1:
            increase_time()
            # Espera activa hasta que el botón se libere para evitar rebotes
            while button_time.get_value() == 1:
                time.sleep(0.1)

        # Encender el LED seleccionado por el tiempo indicado
        turn_on_led(current_led, on_time)

        time.sleep(0.1)  # Pausa para evitar sobrecargar la CPU

except KeyboardInterrupt:
    print("Programa interrumpido")
finally:
    for led in leds:
        led.release()  # Liberar los recursos GPIO
    button_select.release()
    button_time.release()

