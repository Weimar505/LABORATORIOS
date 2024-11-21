import cv2
import os
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
    def __init__(self, camera) -> None:  # Constructor con doble guión bajo
        self.camera = camera
        self.displayed = False
        self.gray_scale = False
        self.capture_count = 1  # Contador para guardar imágenes con nombres secuenciales

        # Verificar si la carpeta "Capturas" existe
        if not os.path.exists("Capturas"):
            os.makedirs("Capturas")  # Crea el directorio "Capturas" si no existe

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
                frame_display = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('Camera - Grayscale', frame_display)
            else:
                frame_display = frame
                cv2.imshow('Camera - RGB', frame_display)

            key = cv2.waitKey(1)
            if key == ord('q'):  # Presionar 'q' para salir
                self.stop_display()
            elif key == ord('g'):  # Presionar 'g' para cambiar a escala de grises
                self.gray_scale = True
            elif key == ord('r'):  # Presionar 'r' para cambiar a RGB
                self.gray_scale = False
            elif key == ord('c'):  # Presionar 'c' para capturar y guardar la imagen
                image_path = f"Capturas/imagen{self.capture_count}.jpg"
                cv2.imwrite(image_path, frame)  # Guarda la imagen original
                print(f"Imagen guardada en {image_path}")
                self.apply_grayscale_and_split(image_path)  # Aplica el filtro de escala de grises y divide en cuadrantes
                self.capture_count += 1

        # Liberar la cámara y cerrar ventanas
        self.camera.release()
        cv2.destroyAllWindows()

    def apply_grayscale_and_split(self, image_path):
        # Cargar la imagen guardada
        image = cv2.imread(image_path)
        if image is None:
            print("No se pudo cargar la imagen.")
            return

        # Convertir la imagen a escala de grises
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Guardar la imagen en escala de grises
        gray_image_path = image_path.replace(".jpg", "_grayscale.jpg")
        cv2.imwrite(gray_image_path, gray_image)
        print(f"Imagen en escala de grises guardada en {gray_image_path}")

        # Obtener el tamaño de la imagen
        height, width = gray_image.shape

        # Dividir la imagen en cuatro cuadrantes
        half_height = height // 2
        half_width = width // 2

        # Extraer cada cuadrante
        quadrants = [
            gray_image[0:half_height, 0:half_width],        # Cuadrante superior izquierdo
            gray_image[0:half_height, half_width:width],    # Cuadrante superior derecho
            gray_image[half_height:height, 0:half_width],   # Cuadrante inferior izquierdo
            gray_image[half_height:height, half_width:width] # Cuadrante inferior derecho
        ]

        # Guardar cada cuadrante
        for i, quadrant in enumerate(quadrants):
            quadrant_path = image_path.replace(".jpg", f"_quadrant{i+1}.jpg")
            cv2.imwrite(quadrant_path, quadrant)
            print(f"Cuadrante {i+1} guardado en {quadrant_path}")

# Inicializar la captura de la cámara y ejecutar el programa
camera = cv2.VideoCapture(0)
camera_object = VideoCapture(camera)
camera_object.display_camera()