import serial
import threading
from time import sleep
import gpiod
import time

# Configuración del puerto serial
tiva = serial.Serial("/dev/ttyACM0", 115200)
tiva.reset_input_buffer()

# Definir los números de línea GPIO correspondientes a TRIG y ECHO
TRIG_LINE = 23  # GPIO 23 para TRIG
ECHO_LINE = 24  # GPIO 24 para ECHO

# Crear un chip GPIO con el número del chip (normalmente "gpiochip0")
chip = gpiod.Chip('gpiochip0')

# Solicitar acceso a las líneas GPIO TRIG y ECHO
trig_line = chip.get_line(TRIG_LINE)
echo_line = chip.get_line(ECHO_LINE)

# Configurar TRIG como salida y ECHO como entrada
trig_line.request(consumer="Ultrasonic Trigger", type=gpiod.LINE_REQ_DIR_OUT)
echo_line.request(consumer="Ultrasonic Echo", type=gpiod.LINE_REQ_DIR_IN)

def medir_distancia():
    # Asegurarse de que el TRIG está en bajo
    trig_line.set_value(0)
    time.sleep(0.05)  # Espera mínima para estabilizar la señal TRIG

    # Enviar un pulso de 10us a TRIG
    trig_line.set_value(1)
    time.sleep(0.00001)
    trig_line.set_value(0)

    # Esperar a que ECHO pase a alto
    inicio_pulso = time.time()
    while echo_line.get_value() == 0:
        inicio_pulso = time.time()

    # Esperar a que ECHO vuelva a bajo
    fin_pulso = time.time()
    while echo_line.get_value() == 1:
        fin_pulso = time.time()

    duracion_pulso = fin_pulso - inicio_pulso

    # Calcular la distancia (velocidad del sonido es 34300 cm/s)
    distancia = duracion_pulso * 34300 / 2
    
    # Convertir la distancia a una cadena y enviarla por UART
    distancia_str = f"{distancia:.2f}\n"  # Formatear la distancia con dos decimales
    tiva.write(distancia_str.encode())  # Enviar la distancia por UART
    
    return distancia

try:
    while True:
        dist = medir_distancia()
        print(f"Distancia: {dist:.2f} cm")
        time.sleep(0.05)  # Esperar solo 50ms antes de la siguiente medición
except KeyboardInterrupt:
    print("Medición detenida por el usuario")
finally:
    trig_line.release()
    echo_line.release()
    chip.close()
