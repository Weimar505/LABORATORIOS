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
    def __init__(self, camera) -> None:  # Corregido el nombre del constructor
        self.camera = camera
        self.displayed = False
        self.gray_scale = False  # Bandera para cambiar entre escala de grises y RGB

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                break

            # Mostrar en escala de grises o RGB según el estado de la bandera
            if self.gray_scale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('Camera - Grayscale', frame)
            else:
                cv2.imshow('Camera - RGB', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):  # Presionar 'q' para salir
                self.stop_display()
            elif key == ord('g'):  # Presionar 'g' para cambiar a escala de grises
                self.gray_scale = True
            elif key == ord('r'):  # Presionar 'r' para cambiar a RGB
                self.gray_scale = False

        # Liberar la cámara y cerrar ventanas
        self.camera.release()
        cv2.destroyAllWindows()

# Inicializar la captura de la cámara y ejecutar el programa
camera = cv2.VideoCapture(0)
camera_object = VideoCapture(camera)  # Aquí ahora debería funcionar correctamente
camera_object.display_camera()
