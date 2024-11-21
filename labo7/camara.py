#Para que funcione dembemos ejecutarlo en el entorno virtual en el s=caso de la direccion de vision artificail 
# y luego habilitar antes de hacerlo correr el programa el entorno virtual con : source env/bin/activate

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

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            cv2.imshow('camera', frame)
            key = cv2.waitKey(1)
            if key != -1:  # Cualquier tecla fue presionada
                self.stop_display()

camera = cv2.VideoCapture(0)
camera_object = VideoCapture(camera)
camera_object.display_camera()
