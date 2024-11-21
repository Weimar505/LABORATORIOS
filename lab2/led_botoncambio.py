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
        # Leer el estado del botón
        button_state = button.get_value()
        button_state2 = button2.get_value()

        if button_state == 1:
            counter += 1
            print(f"Contador: {counter}")

            # Espera activa hasta que el botón se libere
            while button.get_value() == 1:
                pass
            # Esperar un pequeño tiempo para evitar rebotes del botón
            time.sleep(0.2)
                
        if button_state2 == 1:
            counter -= 1
            print(f"Contador: {counter}")

            # Espera activa hasta que el botón se libere
            while button.get_value() == 1:
                pass
            # Esperar un pequeño tiempo para evitar rebotes del botón
            time.sleep(0.2)
        
        # Controlar los LEDs basado en el contador
        
        if counter == 0:
            handle_counter_0()
        elif counter == 1:
            handle_counter_1()
        elif counter == 2:
            handle_counter_2()
        elif counter == 3:
            handle_counter_3()
        elif counter == 4:
            handle_counter_4()
        elif counter == 5:
            handle_counter_5()
        elif counter == 6:
            handle_counter_6()
        elif counter == 7:
            handle_counter_7()
        elif counter == 8:
            handle_counter_8()
        elif counter == 9:
            handle_counter_9()
        elif counter == 10:
            handle_counter_10()
        elif counter == 11:
            handle_counter_11()
        elif counter == 12:
            handle_counter_12()
        elif counter == 13:
            handle_counter_13()
        elif counter == 14:
            handle_counter_14()
        elif counter == 15:
            handle_counter_15()
        elif counter == 16:
            counter=0
        elif counter == -1:
            counter=15
        
        
except KeyboardInterrupt:
    print("Programa interrumpido")
finally:
    for led in leds:
        led.release()  # Liberar los recursos GPIO
    button_select.release()
    button_time.release()

