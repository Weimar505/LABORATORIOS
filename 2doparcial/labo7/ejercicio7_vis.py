import cv2
import numpy as np

class ColorDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("No se pudo cargar la imagen.")

    def detect_color(self, color_name, lower_bound, upper_bound):
        # Convertir la imagen a HSV
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # Crear una máscara para el color
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # Encontrar los contornos del color detectado
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Calcular el área de los contornos detectados
        total_area = sum(cv2.contourArea(c) for c in contours)
        if total_area > 0:
            print(f"Color detectado: {color_name}, Área: {total_area:.2f}")
        else:
            print(f"Color {color_name} no detectado.")

# Usar la clase ColorDetector
image_path = "colores/rojo.png"  # Cambiar por la ruta de la imagen que desees usar
detector = ColorDetector(image_path)

# Definir los rangos HSV para los colores
hsv_ranges = {
    "rojo": ((0, 100, 100), (10, 255, 255)),  # Rango de rojo
    "verde": ((40, 100, 100), (80, 255, 255)),  # Rango de verde
    "azul": ((100, 100, 100), (140, 255, 255))   # Rango de azul
}

# Detectar colores
for color_name, (lower_bound, upper_bound) in hsv_ranges.items():
    detector.detect_color(color_name, np.array(lower_bound), np.array(upper_bound))
