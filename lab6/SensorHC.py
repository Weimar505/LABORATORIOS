import gpiod
import time

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
    time.sleep(2)

    # Enviar un pulso de 10us a TRIG
    trig_line.set_value(1)
    time.sleep(0.00001)
    trig_line.set_value(0)

    # Esperar a que ECHO pase a alto
    while echo_line.get_value() == 0:
        inicio_pulso = time.time()

    # Esperar a que ECHO vuelva a bajo
    while echo_line.get_value() == 1:
        fin_pulso = time.time()

    duracion_pulso = fin_pulso - inicio_pulso

    # Calcular la distancia (velocidad del sonido es 34300 cm/s)
    distancia = duracion_pulso * 34300 / 2

    return distancia

try:
    while True:
        dist = medir_distancia()
        print(f"Distancia: {dist:.2f} cm")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Medición detenida por el usuario")
finally:
    trig_line.release()
    echo_line.release()
    chip.close()
