import cv2
import serial
import numpy as np
import threading
import time
import gpiod
from abc import ABC, abstractmethod

# Configuración del pin LED
LED_PIN = 17  # Cambia esto al pin correcto para tu LED
# Usa el gpiochip correcto
chip = gpiod.Chip('gpiochip0')  # Asegúrate de usar el gpiochip correcto
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
        self.motion_detected = False  # Indica si se detectó movimiento
        self.running = True  # Controla la ejecución de hilos

    def display_camera(self):
        self.displayed = True
        threading.Thread(target=self.camera_visualization, daemon=True).start()  # Inicia el hilo de visualización
        threading.Thread(target=self.uart_sender, daemon=True).start()  # Inicia el hilo para enviar por UART
        threading.Thread(target=self.led_controller, daemon=True).start()  # Inicia el hilo para controlar el LED

    def stop_display(self):
        self.displayed = False
        self.running = False  # Detiene la ejecución
        self.uart.close()  # Cierra el puerto UART al detener la visualización
        led.set_value(0)  # Apaga el LED al detener la visualización

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro. Verifica la cámara.")
                self.stop_display()
                break
            
            # Aplicar la sustracción de fondo
            fg_mask = self.background_subtractor.apply(frame)
            # Aplicar una operación morfológica para limpiar la máscara
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))

            # Detectar movimiento
            if np.sum(fg_mask) > 0:  # Verifica si hay movimiento
                self.motion_detected = True
            else:
                self.motion_detected = False
            
            # Mostrar el marco original y la máscara de primer plano
            cv2.imshow('Foreground Mask', fg_mask)

            key = cv2.waitKey(1)
            if key != -1:  # Cualquier tecla fue presionada
                self.stop_display()

    def uart_sender(self):
        while self.running:
            if self.motion_detected:
                self.uart.write(b'Movimiento detectado\n')  # Envía el mensaje por UART
                print("Movimiento detectado")  # Imprime en consola
            else:
                print("Movimiento no detectado")  # Imprime en consola
            time.sleep(1)  # Espera 1 segundo antes de volver a verificar

    def led_controller(self):
        while self.running:
            if self.motion_detected:
                led.set_value(1)  # Enciende el LED
            else:
                led.set_value(0)  # Apaga el LED
            time.sleep(0.5)  # Espera medio segundo antes de volver a verificar

camera = cv2.VideoCapture(1)  # Prueba con diferentes índices si es necesario
if not camera.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    uart_port = '/dev/ttyACM0'  # Cambia esto al puerto correcto donde está conectado tu dispositivo UART
    camera_object = VideoCapture(camera, uart_port)
    camera_object.display_camera()
