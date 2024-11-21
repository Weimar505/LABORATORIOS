import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('monedas_2.jpg')
original = imagen.copy()

# Convertir a escala de grises
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro Gaussiano para reducir el ruido
gauss = cv2.GaussianBlur(grises, (5, 5), 0)

# Hough Circle Transform (Ajustar parámetros)
circles = cv2.HoughCircles(gauss, cv2.HOUGH_GRADIENT, 1.2, 80,  # dp and minDist ajustados
                            param1=150, param2=40,  # param2 incrementado
                            minRadius=180, maxRadius=200)  # minRadius ajustado

# Asegúrate de que se encontraron círculos
if circles is not None:
    circles = np.uint16(np.around(circles))
    
    # Dibujar círculos y numerar las monedas
    for i, (x, y, r) in enumerate(circles[0, :]):
        cv2.circle(original, (x, y), r, (0, 255, 0), 2)
        cv2.putText(original, f"Moneda {i + 1}", (x - 40, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Mostrar la imagen con las monedas detectadas
cv2.imshow('Monedas Detectadas', original)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Imprimir el número de monedas detectadas
print(f"Se detectaron {len(circles[0]) if circles is not None else 0} monedas.")
