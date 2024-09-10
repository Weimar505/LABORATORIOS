import gpiod
import time

# Declaramos los pines GPIO
LED_PIN = 20
LED2_PIN = 6
BUTTON_PIN = 27

# Creamos una instancia del chip GPIO
chip = gpiod.Chip('gpiochip0')

# Configuramos las líneas GPIO
led = chip.get_line(LED_PIN)
led2 = chip.get_line(LED2_PIN)
button = chip.get_line(BUTTON_PIN)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
led2.request(consumer="LED2", type=gpiod.LINE_REQ_DIR_OUT)
button.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])

# Inicializamos el contador y el estado del botón
counter = 0
button_pressed = False

def handle_counter_1():
    led.set_value(1)
    time.sleep(1)
    led.set_value(0)
    led2.set_value(1)
    time.sleep(1)
    led2.set_value(0)

def handle_counter_2():
    led.set_value(1)
    led2.set_value(1)
    time.sleep(2)
    led.set_value(0)
    led2.set_value(0)
    time.sleep(2)

def handle_counter_3():
    led.set_value(1)
    led2.set_value(1)

def handle_counter_4():
    led.set_value(0)
    led2.set_value(0)

def execute_sequence():
    global counter
    if counter == 1:
        handle_counter_1()
    elif counter == 2:
        handle_counter_2()
    elif counter == 3:
        handle_counter_3()
    elif counter == 4:
        handle_counter_4()
        counter = 0  # Reiniciar el contador

try:
    while True:
        # Leer el estado del botón
        button_state = button.get_value()

        # Verificar si el botón ha sido presionado
        if button_state == 1:
            if not button_pressed:
                button_pressed = True
                counter += 1
                print(f"Contador: {counter}")
                # Reiniciar la secuencia actual
                execute_sequence()
                # Esperar un pequeño tiempo para evitar rebotes del botón
                time.sleep(0.2)
        else:
            button_pressed = False

except KeyboardInterrupt:
    # Liberar los recursos
    led.release()
    led2.release()
    button.release()
