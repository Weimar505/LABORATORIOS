import gpiod
import time
import threading

# Configuración del GPIO
LED_PIN = 17
chip = gpiod.Chip('gpiochip0')
LED = chip.get_line(LED_PIN)
LED.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# Variable de tiempo controlada por el usuario
tiempo_encendido = 1.0  # Tiempo inicial en segundos

# Función para controlar el LED en bucle
def control_led():
    global tiempo_encendido
    while True:
        # Encender LED
        LED.set_value(1)
        time.sleep(tiempo_encendido)  # Mantener encendido el tiempo dado
        # Apagar LED
        LED.set_value(0)
        time.sleep(tiempo_encendido)  # Mantener apagado el tiempo dado

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

# Iniciar el bucle de control del LED
try:
    control_led()
except KeyboardInterrupt:
    print("\nPrograma terminado.")
    LED.set_value(0)
    LED.release()
