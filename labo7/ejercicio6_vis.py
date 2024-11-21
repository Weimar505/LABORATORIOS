import cv2
import numpy as np
import os

class ColorModifier:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("No se pudo cargar la imagen.")

    def to_grayscale(self):
        # Convertir la imagen a escala de grises
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def to_hsv(self):
        # Convertir la imagen a espacio de color HSV
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

    def display_image(self, image, window_name):
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Usar la clase ColorModifier
carpeta_colores = "colores"
colors = ["rojo", "verde", "azul"]

for color_name in colors:
    try:
        image_path = f"{carpeta_colores}/{color_name}.png"
        color_modifier = ColorModifier(image_path)

        # Mostrar imagen original
        color_modifier.display_image(color_modifier.image, f"Original - {color_name}")

        # Convertir y mostrar imagen en escala de grises
        gray_image = color_modifier.to_grayscale()
        color_modifier.display_image(gray_image, f"Escala de Grises - {color_name}")

        # Convertir y mostrar imagen en HSV
        hsv_image = color_modifier.to_hsv()
        color_modifier.display_image(hsv_image, f"HSV - {color_name}")

    except ValueError as e:
        print(e)
