import cv2

# Cargar la imagen
image = cv2.imread("contorno.jpg")  # Reemplaza "imagen.jpg" con la ruta de tu imagen

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un umbral para resaltar los contornos
# Puedes ajustar el umbral dependiendo de la imagen
_, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Detectar los contornos
# cv2.RETR_EXTERNAL para obtener solo los contornos externos
# cv2.CHAIN_APPROX_SIMPLE para simplificar los puntos del contorno
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos sobre la imagen original
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)  # -1 dibuja todos los contornos, color verde, grosor 2

# Mostrar la imagen con los contornos
cv2.imshow("Contornos", image)
cv2.waitKey(0)
cv2.destroyAllWindows()