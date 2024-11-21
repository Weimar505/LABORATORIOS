import cv2
import numpy as np
import os

# Definir la carpeta "colores"
carpeta_colores = "colores"

# Definir los colores en formato BGR
colors = {
    "rojo": (0, 0, 255),
    "verde": (0, 255, 0),
    "azul": (255, 0, 0)
}

# Función para convertir BGR a escala de grises
def rgb_a_grises(bgr_color):
    # Convertir de BGR a RGB
    rgb_color = (bgr_color[2], bgr_color[1], bgr_color[0])
    # Calcular el valor de gris usando la fórmula de luminancia
    gris = 0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2]
    return gris

# Imprimir los valores en escala de grises
def imprimir_grises():
    for color_name in colors.keys():
        img = cv2.imread(f"{carpeta_colores}/{color_name}.png")
        if img is not None:  # Verificar si la imagen se ha cargado correctamente
            color_value = img[0, 0]  # Obtener el valor del primer píxel (color sólido)
            gris_value = rgb_a_grises(color_value)
            print(f"Valor en escala de grises para {color_name}: {gris_value:.2f}")
        else:
            print(f"No se pudo cargar la imagen para el color '{color_name}'.")

# Llamar a la función para imprimir los valores en escala de grises
imprimir_grises()
