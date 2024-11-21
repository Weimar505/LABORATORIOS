import gpiod
import time

# Declaramos los pines GPIO
LED_PIN = 17
BUTTON_PIN = 12
BUTTON_PIN2 = 27

# Creamos una instancia del chip GPIO
chip = gpiod.Chip('gpiochip0')

# Configuramos las líneas GPIO
led = chip.get_line(LED_PIN)
button = chip.get_line(BUTTON_PIN)
button2 = chip.get_line(BUTTON_PIN2)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
button.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
button2.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])

# Inicializamos el contador
counter = 0

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
            while button2.get_value() == 1:
                pass
            # Esperar un pequeño tiempo para evitar rebotes del botón
            time.sleep(0.2)
            
        # Controlar los LEDs basado en el contador
        if counter == 1:
            led.set_value(1)  # Enciende el LED principal
        elif counter == 0:
            led.set_value(0)  # Enciende el LED principal
            


except KeyboardInterrupt:
    # Liberar los recursos
    led.release()
    button2.release()
    button.release()