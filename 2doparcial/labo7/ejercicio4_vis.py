import cv2

# Cargar la imagen
img = cv2.imread("wall-e.jpg")

# Verificar si la imagen se cargó correctamente
if img is None:
    print("Error al cargar la imagen.")
    exit()

# Mostrar la imagen original
cv2.imshow("Imagen Original", img)

# Redimensionar la imagen a 400x600
resized_img = cv2.resize(img, (600, 400))
cv2.imshow("Imagen Redimensionada", resized_img)

# Cortar la imagen horizontalmente y mostrar las dos mitades
height, width, _ = img.shape
half_height = height // 2
top_half = img[:half_height, :]
bottom_half = img[half_height:, :]

cv2.imshow("Mitad Superior", top_half)
cv2.imshow("Mitad Inferior", bottom_half)

# Cortar la imagen verticalmente y mostrar las dos mitades
half_width = width // 2
left_half = img[:, :half_width]
right_half = img[:, half_width:]

cv2.imshow("Mitad Izquierda", left_half)
cv2.imshow("Mitad Derecha", right_half)

# Dividir la imagen en cuadrantes
quadrant_1 = img[:half_height, :half_width]
quadrant_2 = img[:half_height, half_width:]
quadrant_3 = img[half_height:, :half_width]
quadrant_4 = img[half_height:, half_width:]

# Mostrar los cuadrantes
cv2.imshow("Cuadrante 1", quadrant_1)
cv2.imshow("Cuadrante 2", quadrant_2)
cv2.imshow("Cuadrante 3", quadrant_3)
cv2.imshow("Cuadrante 4", quadrant_4)

# Esperar a que se cierre la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()
