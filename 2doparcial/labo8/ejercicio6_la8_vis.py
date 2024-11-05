import cv2
from abc import ABC, abstractmethod

# Clase abstracta base para definir los métodos requeridos en VideoCapture
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

# Clase principal de captura de video que implementa VideoCaptureAbs
class VideoCapture(VideoCaptureAbs):
    def __init__(self, camera) -> None:
        # Constructor para inicializar la cámara y el estado de visualización
        self.camera = camera
        self.displayed = False

    def display_camera(self):
        # Activa el estado de visualización y llama a la función para visualizar
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        # Desactiva la visualización
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            # Leer el fotograma de la cámara
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro.")
                break
            
            # Convertir el fotograma a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Aplicar un umbral para binarizar la imagen
            _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            # Detectar los contornos
            contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Dibujar los contornos sobre el fotograma original
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            # Mostrar el fotograma con los contornos
            cv2.imshow('camera', frame)

            # Revisar si se presiona una tecla para detener la visualización
            key = cv2.waitKey(1)
            if key != -1:  # Cualquier tecla fue presionada
                self.stop_display()

        # Liberar la cámara y cerrar todas las ventanas al detener la visualización
        self.camera.release()
        cv2.destroyAllWindows()

# Configuración de la cámara
camera = cv2.VideoCapture(0)  # Cambia el índice de la cámara si es necesario
camera_object = VideoCapture(camera)  # Crear instancia de VideoCapture
camera_object.display_camera()  # Iniciar la visualización con detección de contornos