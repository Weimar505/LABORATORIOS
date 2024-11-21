import gpiod
import time
import threading

# Configuración de los pines GPIO para los LEDs
LED_PIN = 20
LED_PIN1 = 6
LED_PIN2 = 13
LED_PIN3 = 19

chip = gpiod.Chip('gpiochip0')
LED = chip.get_line(LED_PIN)
LED1 = chip.get_line(LED_PIN1)
LED2 = chip.get_line(LED_PIN2)
LED3 = chip.get_line(LED_PIN3)

LED.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
LED1.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
LED2.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
LED3.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# Variable de tiempo controlada por el usuario
tiempo_encendido = 1.0  # Tiempo inicial en segundos

# Función para controlar la secuencia de LEDs en bucle
def control_leds():
    global tiempo_encendido
    while True:
        # Secuencia de encendido y apagado de los LEDs
        LED.set_value(1)
        time.sleep(tiempo_encendido)
        LED.set_value(0)

        LED1.set_value(1)
        time.sleep(tiempo_encendido)
        LED1.set_value(0)

        LED2.set_value(1)
        time.sleep(tiempo_encendido)
        LED2.set_value(0)

        LED3.set_value(1)
        time.sleep(tiempo_encendido)
        LED3.set_value(0)

# Función para recibir el tiempo desde la terminal sin detener el bucle
def recibir_tiempo():
    global tiempo_encendido
    while True:
        try:
            nuevo_tiempo = float(input("Introduce el nuevo tiempo de encendido/apagado en segundos: "))
            if nuevo_tiempo > 0:
                tiempo_encendido = nuevo_tiempo
                print(f"Tiempo actualizado a {tiempo_encendido} segundos")
            else:
                print("Por favor introduce un valor mayor que 0.")
        except ValueError:
            print("Por favor introduce un número válido.")

# Crear un hilo para recibir el tiempo
hilo_entrada = threading.Thread(target=recibir_tiempo)
hilo_entrada.daemon = True  # Esto asegura que el hilo se cierre cuando el programa termine
hilo_entrada.start()

# Iniciar el bucle de control de la secuencia de LEDs
try:
    control_leds()
except KeyboardInterrupt:
    print("\nPrograma terminado.")
    LED.set_value(0)
    LED1.set_value(0)
    LED2.set_value(0)
    LED3.set_value(0)
    LED.release()
    LED1.release()
    LED2.release()
    LED3.release()

