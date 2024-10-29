import cv2
import os
from abc import ABC, abstractmethod

# Crear la carpeta "Capturas" si no existe (sin errores si ya está creada)
os.makedirs("Capturas", exist_ok=True)

# Clase abstracta base para definir métodos requeridos en VideoCapture
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
        self.image_counter = 1  # Contador para el nombre de las imágenes

    def display_camera(self):
        # Activa el estado de visualización y llama a la función para visualizar
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        # Desactiva la visualización
        self.displayed = False

    def camera_visualization(self):
        # Bucle que muestra la cámara mientras display_camera esté activado
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro.")
                break

            # Mostrar el cuadro en la ventana de la cámara
            cv2.imshow('camera', frame)
            key = cv2.waitKey(1)
            
            # Si se presiona la tecla 's', guarda la imagen
            if key == ord('c'):
                self.save_frame(frame)
            elif key != -1:  # Cualquier otra tecla termina la visualización
                self.stop_display()

        # Liberar la cámara y cerrar todas las ventanas cuando se detiene la visualización
        self.camera.release()
        cv2.destroyAllWindows()

    def save_frame(self, frame):
        """Guardar la imagen capturada en la carpeta 'Capturas'."""
        image_path = f"Capturas/imagen{self.image_counter}.jpg"
        cv2.imwrite(image_path, frame)  # Guarda el fotograma actual, reemplazando si ya existe
        print(f"Imagen guardada en: {image_path}")
        self.image_counter += 1
        ImageProcessor.process_image(image_path)  # Procesar la imagen guardada

# Clase para procesar la imagen capturada
class ImageProcessor:
    @staticmethod
    def process_image(image_path):
        """Aplica filtro de escala de grises y divide la imagen en cuadrantes."""
        # Leer la imagen en color
        image = cv2.imread(image_path)

        # Convertir la imagen a escala de grises
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Guardar la imagen en escala de grises, reemplazando si ya existe
        gray_image_path = image_path.replace(".jpg", "_gray.jpg")
        cv2.imwrite(gray_image_path, gray_image)
        print(f"Imagen en escala de grises guardada en: {gray_image_path}")

        # Dividir la imagen en cuadrantes
        height, width = gray_image.shape
        mitad_altura, mitad_ancho = height // 2, width // 2

        # Extraer cada cuadrante
        cuadrante_1 = gray_image[:mitad_altura, :mitad_ancho]  # Superior izquierda
        cuadrante_2 = gray_image[:mitad_altura, mitad_ancho:]  # Superior derecha
        cuadrante_3 = gray_image[mitad_altura:, :mitad_ancho]  # Inferior izquierda
        cuadrante_4 = gray_image[mitad_altura:, mitad_ancho:]  # Inferior derecha

        # Guardar cada cuadrante, reemplazando si ya existen
        cv2.imwrite(image_path.replace(".jpg", "_cuadrante1.jpg"), cuadrante_1)
        cv2.imwrite(image_path.replace(".jpg", "_cuadrante2.jpg"), cuadrante_2)
        cv2.imwrite(image_path.replace(".jpg", "_cuadrante3.jpg"), cuadrante_3)
        cv2.imwrite(image_path.replace(".jpg", "_cuadrante4.jpg"), cuadrante_4)
        print("Cuadrantes guardados para la imagen procesada.")

# Configuración de la cámara
camera = cv2.VideoCapture(1)  # Inicia la cámara (cambia el índice si es necesario)
camera_object = VideoCapture(camera)  # Crea una instancia de VideoCapture con la cámara
camera_object.display_camera()  # Muestra la cámara con la funcionalidad de captura