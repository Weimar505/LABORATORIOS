import serial
import gpiod
from time import sleep
from gpiozero import PWMLED

# Configuración del puerto serie
user = serial.Serial("/dev/ttyACM0", 115200)
user.reset_input_buffer()

# Configuración del pin LED
LED_PIN = 16
# Usa el gpiochip correcto
chip = gpiod.Chip('gpiochip0')  # Asegúrate de usar el gpiochip correcto
led = chip.get_line(LED_PIN)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

pwm1 = PWMLED(18)  # Usa el pin GPIO 18 para PWM
pwm2 = PWMLED(12)  # Usa el pin GPIO 12 para PWM

try:
    while True:
        try:
            # Leer y enviar datos desde el teclado
            mensaje = input("")
            user.write(mensaje.encode('utf-8') + b'\n')  # Añade un salto de línea al final si es necesario

            # Leer mensajes desde el puerto UART en tiempo real
            while user.in_waiting > 0:
                value = user.read(user.in_waiting).decode('utf-8').strip()  # Strip para eliminar espacios adicionales
                print(value)
                
                # Procesar el mensaje recibido
                if value == "motor 1":
                    led.set_value(1)
                    pwm1.value = 0.25
                    pwm2.value = 1
                elif value == "motor 2":
                    led.set_value(0)
                    pwm1.value = 1
                    pwm2.value = 0.25
                elif value == "apagado":
                    led.set_value(0)
                    pwm1.value = 0
                    pwm2.value = 0

            # Pausa para evitar el uso excesivo de CPU
            sleep(0.1)
        except Exception as e:
            print("Error:", e)
except KeyboardInterrupt:
    print("Código finalizado")
    led.set_value(0)  # Asegurarse de que el LED esté apagado
    pwm1.off()  # Asegurarse de que PWMLED esté apagado
    pwm2.off()  # Asegurarse de que PWMLED esté apagado
    led.release()  # Liberar el pin
    user.close()  # Cerrar el puerto serie
    print("GPIOs liberados")
