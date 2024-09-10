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

# Inicializamos el contador
counter = 0

def handle_counter_0():
    led.set_value(0)
    led2.set_value(0)
    led3.set_value(0)
    led4.set_value(0)
    
def handle_counter_1():
    led.set_value(1)
    led2.set_value(0)
    led3.set_value(0)
    led4.set_value(0)

def handle_counter_2():
    led.set_value(0)
    led2.set_value(1)
    led3.set_value(0)
    led4.set_value(0)

def handle_counter_3():
    led.set_value(1)
    led2.set_value(1)
    led3.set_value(0)
    led4.set_value(0)
    
def handle_counter_4():
    led.set_value(0)
    led2.set_value(0)
    led3.set_value(1)
    led4.set_value(0)
    
def handle_counter_5():
    led.set_value(1)
    led2.set_value(0)
    led3.set_value(1)
    led4.set_value(0)
    
def handle_counter_6():
    led.set_value(0)
    led2.set_value(1)
    led3.set_value(1)
    led4.set_value(0)
    
def handle_counter_7():
    led.set_value(1)
    led2.set_value(1)
    led3.set_value(1)
    led4.set_value(0)
    
def handle_counter_8():
    led.set_value(0)
    led2.set_value(0)
    led3.set_value(0)
    led4.set_value(1)
    
def handle_counter_9():
    led.set_value(1)
    led2.set_value(0)
    led3.set_value(0)
    led4.set_value(1)

def handle_counter_10():
    led.set_value(0)
    led2.set_value(1)
    led3.set_value(0)
    led4.set_value(1)
    
def handle_counter_11():
    led.set_value(1)
    led2.set_value(1)
    led3.set_value(0)
    led4.set_value(1)
    
def handle_counter_12():
    led.set_value(0)
    led2.set_value(0)
    led3.set_value(1)
    led4.set_value(1)

def handle_counter_13():
    led.set_value(1)
    led2.set_value(0)
    led3.set_value(1)
    led4.set_value(1)
    
def handle_counter_14():
    led.set_value(0)
    led2.set_value(1)
    led3.set_value(1)
    led4.set_value(1)
    
def handle_counter_15():
    led.set_value(1)
    led2.set_value(1)
    led3.set_value(1)
    led4.set_value(1)
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
    # Liberar los recursos
    led.release()
    led2.release()
    led3.release()
    led4.release()
    button.release()
    button2.release()
