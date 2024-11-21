import cv2
import numpy as np
import os

# Definir la carpeta "colores"
carpeta_colores = "colores"

# Verificar si la carpeta "colores" existe
if not os.path.exists(carpeta_colores):
    # Crear la carpeta "colores"
    os.makedirs(carpeta_colores)
    print(f"Carpeta '{carpeta_colores}' creada.")
else:
    print(f"La carpeta '{carpeta_colores}' ya existe.")

# Definir los colores en formato BGR
colors = {
    "rojo": (0, 0, 255),
    "verde": (0, 255, 0),
    "azul": (255, 0, 0)
}

# Crear y guardar las imágenes solo si no existen
for color_name, color_value in colors.items():
    ruta_imagen = f"{carpeta_colores}/{color_name}.png"
    if not os.path.exists(ruta_imagen):
        # Crear una imagen de 100x100 píxeles de un color sólido
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:] = color_value
        # Guardar la imagen
        cv2.imwrite(ruta_imagen, img)
        print(f"Imagen '{ruta_imagen}' creada.")
    else:
        print(f"La imagen '{ruta_imagen}' ya existe.")
