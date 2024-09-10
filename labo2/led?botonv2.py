import gpiod
import time

# Declaramos los pines GPIO
LED_PIN = 20
LED2_PIN = 6
LED3_PIN = 19
LED4_PIN = 13
BUTTON_PIN = 27
BUTTON_PIN2 = 12

# Creamos una instancia del chip GPIO
chip = gpiod.Chip('gpiochip0')

# Configuramos las líneas GPIO
led = chip.get_line(LED_PIN)
led2 = chip.get_line(LED2_PIN)
led3 = chip.get_line(LED3_PIN)
led4 = chip.get_line(LED4_PIN)

button = chip.get_line(BUTTON_PIN)
button2 = chip.get_line(BUTTON_PIN2)

led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
led2.request(consumer="LED2", type=gpiod.LINE_REQ_DIR_OUT)
led3.request(consumer="LED3", type=gpiod.LINE_REQ_DIR_OUT)
led4.request(consumer="LED4", type=gpiod.LINE_REQ_DIR_OUT)
button.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
button2.request(consumer="Button2", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
counter = 0
x = 1
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
            x -= 0.1
            print(f"tiempo: {x}")

            # Espera activa hasta que el botón se libere
            while button.get_value() == 1:
                pass
            # Esperar un pequeño tiempo para evitar rebotes del botón
            time.sleep(0.2)
        
        # Controlar los LEDs basado en el contador
        
        if counter == 1:
                led.set_value(1)
                led2.set_value(0)
                led3.set_value(0)
                led4.set_value(0)
                time.sleep(x)
                led.set_value(0)
                time.sleep(x)
        elif counter == 2:
                led.set_value(0)
                led2.set_value(1)
                led3.set_value(0)
                led4.set_value(0)
                time.sleep(x)
                led2.set_value(0)
                time.sleep(x)
        elif counter == 3:
                led.set_value(0)
                led2.set_value(0)
                led3.set_value(1)
                led4.set_value(0)
                time.sleep(x)
                led3.set_value(0)
                time.sleep(x)
            
        elif counter == 4:
                led.set_value(0)
                led2.set_value(0)
                led3.set_value(0)
                led4.set_value(1)
                time.sleep(x)
                led4.set_value(0)
                time.sleep(x)
        
        elif counter >4:
            counter = 1
        elif x <0.1:
            x = 1
except KeyboardInterrupt:
    # Liberar los recursos
    led.release()
    led2.release()
    led3.release()
    led4.release()
    button.release()
    button2.release()
