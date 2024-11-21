import cv2
from abc import ABC, abstractmethod

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
    def __init__(self, camera) -> None:
        self.camera = camera
        self.displayed = False
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro. Verifica la cámara.")
                self.stop_display()
                break
            
            # Aplicar la sustracción de fondo
            fg_mask = self.background_subtractor.apply(frame)

            # Mostrar el marco original y la máscara de primer plano
            cv2.imshow('Original Camera', frame)
            cv2.imshow('Foreground Mask', fg_mask)

            key = cv2.waitKey(1)
            if key != -1:  # Cualquier tecla fue presionada
                self.stop_display()

camera = cv2.VideoCapture(0)  # Prueba con diferentes índices si es necesario
if not camera.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    camera_object = VideoCapture(camera)
    camera_object.display_camera()
