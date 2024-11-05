import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen
ruta_imagen = 'figuras.png'
imagen = cv2.imread(ruta_imagen)

# Convertir la imagen a escala de grises y aplicar desenfoque para reducir el ruido
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
imagen_desenfocada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

# Detectar bordes usando Canny
bordes = cv2.Canny(imagen_desenfocada, 50, 150)

# Encontrar contornos en la imagen binaria
contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Colores para cada tipo de figura
colores = {
    "Triángulo": (0, 255, 255),
    "Cuadrado": (255, 0, 0),
    "Rectángulo": (0, 255, 0),
    "Pentágono": (255, 0, 255),
    "Hexágono": (0, 165, 255),
    "Círculo": (255, 255, 0)
}

# Función para detectar el tipo de figura
def detectar_figura(contorno):
    perimetro = cv2.arcLength(contorno, True)
    aproximacion = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)
    lados = len(aproximacion)

    if lados == 3:
        return "Triángulo"
    elif lados == 4:
        (x, y, w, h) = cv2.boundingRect(aproximacion)
        aspecto = w / float(h)
        if 0.95 <= aspecto <= 1.05:
            return "Cuadrado"
        else:
            return "Rectángulo"
    elif lados == 5:
        return "Pentágono"
    elif lados == 6:
        return "Hexágono"
    else:
        return "Círculo"

# Detectar y colorear cada figura directamente en la imagen original
for contorno in contornos:
    figura = detectar_figura(contorno)
    color = colores.get(figura, (0, 0, 0))  # Obtener color asignado para la figura

    # Dibujar el contorno de la figura y el nombre
    cv2.drawContours(imagen, [contorno], -1, color, -1)  # Rellenar la figura
    M = cv2.moments(contorno)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.putText(imagen, figura, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

# Mostrar la imagen con las figuras coloreadas y etiquetadas usando matplotlib
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)  # Convertir a RGB para matplotlib
plt.imshow(imagen_rgb)
plt.axis('off')  # Ocultar ejes
plt.title("Detección de Figuras y Colores")
plt.show()
