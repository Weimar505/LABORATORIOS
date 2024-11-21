import cv2
from abc import ABC, abstractmethod

# Clase abstracta base
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

# Clase principal de captura de video
class VideoCapture(VideoCaptureAbs):
    def __init__(self, camera) -> None:
        self.camera = camera
        self.displayed = False
        self.filter = None  # Atributo para el filtro actual

    def set_filter(self, filter_name):
        """Define el filtro a aplicar en la visualización"""
        self.filter = filter_name

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro.")
                break

            # Aplicar el filtro seleccionado al frame
            if self.filter == 'grayscale':
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif self.filter == 'canny':
                frame = cv2.Canny(frame, 100, 200)
            elif self.filter == 'invert':
                frame = cv2.bitwise_not(frame)

            # Mostrar la cámara con el filtro aplicado
            cv2.imshow('camera', frame)
            key = cv2.waitKey(1)
            if key != -1:  # Cualquier tecla fue presionada
                self.stop_display()

        self.camera.release()
        cv2.destroyAllWindows()

# Clase para la selección de filtros
class FilterSelection:
    def __init__(self, camera_object):
        self.camera_object = camera_object

    def select_filter(self):
        """Muestra el menú para seleccionar el filtro"""
        print("Selecciona un filtro:")
        print("1: Escala de grises")
        print("2: Bordes (Canny)")
        print("3: Invertir colores")
        print("0: Sin filtro")

        choice = input("Elige una opción (1-3 o 0 para ninguno): ")
        if choice == '1':
            self.camera_object.set_filter('grayscale')
        elif choice == '2':
            self.camera_object.set_filter('canny')
        elif choice == '3':
            self.camera_object.set_filter('invert')
        else:
            self.camera_object.set_filter(None)

# Configuración de la cámara y selección de filtro
camera = cv2.VideoCapture(1)  # Cambia el índice si es necesario
camera_object = VideoCapture(camera)

# Crear el objeto para seleccionar filtros y activar la cámara
filter_selection = FilterSelection(camera_object)
filter_selection.select_filter()  # Permite al usuario elegir el filtro
camera_object.display_camera()  # Muestra la cámara con el filtro seleccionado