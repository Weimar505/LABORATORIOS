import serial
from time import sleep
import threading
import gpiod

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 9600)
tiva.reset_input_buffer()

# Configuración del GPIO para el motor
chip = gpiod.Chip('gpiochip0')  # Cambia 'gpiochip0' según tu dispositivo
motor_pin = 18  # Cambia este pin según tu configuración
motor_line = chip.get_line(motor_pin)
motor_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)

# Función para ajustar la velocidad del motor (simulación de PWM)
def ajustar_velocidad(velocidad):
    # Simula PWM usando ciclos de encendido y apagado en función del porcentaje de velocidad
    tiempo_activo = velocidad / 100.0 * 0.1  # Tiempo encendido en el ciclo de 0.1s
    tiempo_inactivo = 0.1 - tiempo_activo    # Tiempo apagado en el ciclo de 0.1s
    
    if velocidad > 0:
        motor_line.set_value(1)  # Enciende el motor
        sleep(tiempo_activo)     # Mantén encendido según la proporción
        motor_line.set_value(0)  # Apaga el motor
        sleep(tiempo_inactivo)   # Mantén apagado el resto del ciclo
    else:
        motor_line.set_value(0)  # Apaga el motor completamente
    print(f"Velocidad del motor ajustada al {velocidad}%")

# Función para recibir datos en un hilo separado
def recibir_datos():
    while True:
        if tiva.in_waiting > 0:  # Verifica si hay datos en el buffer
            valor = tiva.readline().decode("utf-8").rstrip()
            if valor:
                print(f"Recibido: {valor}")
                
                # Control del motor basado en la palabra recibida
                if valor == "verde":
                    ajustar_velocidad(100)  # 100% de velocidad
                elif valor == "amarillo":
                    ajustar_velocidad(25)   # 25% de velocidad
                elif valor == "rojo":
                    ajustar_velocidad(0)    # Apaga el motor
        sleep(0.1)

# Función para introducir datos manualmente desde la terminal
def introducir_datos_terminal():
    while True:
        try:
            datos = input("Introduce datos: ")  # Captura la entrada del usuario desde la terminal
            tiva.write(datos.encode('utf-8'))  # Envía los datos al puerto serial
            print(f"Enviado: {datos}")
        except EOFError:
            print("Error de lectura")
        sleep(0.1)

# Crear hilos para la recepción de datos y entrada de terminal
hilo_recepcion = threading.Thread(target=recibir_datos)
hilo_terminal = threading.Thread(target=introducir_datos_terminal)

# Iniciar los hilos
hilo_recepcion.start()
hilo_terminal.start()

# Asegurarse de liberar el recurso GPIO al salir
try:
    hilo_recepcion.join()
    hilo_terminal.join()
finally:
    motor_line.set_value(0)
    motor_line.release()
    chip.close()
