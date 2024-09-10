#https://github.com/Weimar505/labo1.git
import gpiod #Esta libreria nos permite controlar los pines GPIO en las raspberry pi 5
LED_PIN = 17 #Declaramos el el pin del led en el gpio 17
BUTTON_PIN = 27 #Declaramos  el pin del boton en el gpio 27
BUTTON2_PIN = 22 #Declaramos  el pin del boton en el gpio 27
chip = gpiod.Chip('gpiochip0') # en esta linea decimos que utilizaremos el gpiochip0 que se almacena en la variable chip
# donde se encuentran los gpio mas info, ingresar en terminal el siguiente comando "gpioinfo"
led = chip.get_line(LED_PIN) # aca se define  que el "led"  utilizará el gpio 17  de las raspberry
button = chip.get_line(BUTTON_PIN) #aca se define que el "button" utilizara el pin 27 de la raspberry
button2 = chip.get_line(BUTTON2_PIN)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT) #Configuramos el led, se coloca una etiqueta (OPCIONAL) para identificar que que representa ese gpio
#despues decimos que la linea 17 gpio de la raspi sera una salida
button.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, default_vals=[0])
#Configuramos el button donde, etiquetamos el pin, declaramos que la linea 27 gpio  es entrada y que es modo pull down
try:  #
   while True:
       button_state = button.get_value()
       if button_state == 1:
           led.set_value(1)
       else:
           led.set_value(0)
except KeyboardInterrupt:#limpia los pines y detiene la ejecucion
	led.release()
	button.release()
