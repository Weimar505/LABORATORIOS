import cv2
import serial
import numpy as np
import gpiod
from abc import ABC, abstractmethod

# Configuración del pin LED
LED_PIN = 17  # Cambia este valor al pin que estés usando
chip = gpiod.Chip('gpiochip0')  # Cambia a gpiochip1 si es necesario
led = chip.get_line(LED_PIN)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

class VideoCaptureAbs(ABC):
    @abstractmethod
    def display_camera(self):
        pass

    @abstractmethod
    def stop_display(self):
        pass

    @abstractmethod
    def camera_visualization(self):
        pass

class VideoCapture(VideoCaptureAbs):
    def __init__(self, camera, uart_port) -> None:
        self.camera = camera
        self.displayed = False
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.uart = serial.Serial(uart_port, 9600)  # Configura el puerto UART
        self.no_motion_counter = 0  # Contador para no detectar movimiento
        self.no_motion_threshold = 10  # Para imprimir si no se detecta movimiento

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False
        self.uart.close()  # Cierra el puerto UART
        led.set_value(0)  # Asegúrate de apagar el LED al detener

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro. Verifica la cámara.")
                self.stop_display()
                break
            
            # Aplicar la sustracción de fondo
            fg_mask = self.background_subtractor.apply(frame)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))

            # Comprobar si hay movimiento
            if np.sum(fg_mask) > 0:  # Verifica si hay movimiento
                led.set_value(1)  # Enciende el LED
                self.uart.write(b'Movimiento detectado\n')  # Envía por UART
                print("Movimiento detectado")  # Imprime en consola
            else:
                led.set_value(0)  # Apaga el LED
                self.uart.write(b'Sin movimiento\n')  # Envía por UART
                print("Sin movimiento")  # Imprime en consola

            # Mostrar el marco original y la máscara de primer plano
            #cv2.imshow('Original Camera', frame)
            cv2.imshow('Foreground Mask', fg_mask)

            key = cv2.waitKey(1)
            if key != -1:  # Cualquier tecla fue presionada
                self.stop_display()

# Configurar la cámara
camera = cv2.VideoCapture(0)  # Prueba con diferentes índices si es necesario
if not camera.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    uart_port = '/dev/ttyACM0'  # Cambia esto al puerto correcto donde está conectado tu dispositivo UART
    camera_object = VideoCapture(camera, uart_port)
    camera_object.display_camera()
