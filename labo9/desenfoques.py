import cv2
import numpy as np

def custom_convolution(image, kernel):
    # Aplicar convolución 2D
    return cv2.filter2D(image, -1, kernel)

# Cargar la imagen
image = cv2.imread('M_O.jpg')  # Reemplaza con tu imagen
if image is None:
    print("Error: No se pudo cargar la imagen.")
    exit()

# Definir un kernel positivo impar (ejemplo: un kernel de suavizado)
'''
kernel = np.array([[0, 1, 0],
                   [1, 3, 1],
                   [0, 1, 0]]) / 8  # Normalizado para que la suma sea 1
'''
kernel = np.array([[1,  4,  6,  4, 1],
                   [4, 16, 24, 16, 4],
                   [6, 24, 36, 24, 6],
                   [4, 16, 24, 16, 4],
                   [1,  4,  6,  4, 1]]) / 256

# Aplicar convolución
convolved_image = custom_convolution(image, kernel)

# Aplicar desenfoque promedio
average_blurred = cv2.blur(image, (5, 5))  # Tamaño del kernel 5x5

# Aplicar desenfoque gaussiano
gaussian_blurred = cv2.GaussianBlur(image, (5, 5), 0)  # Tamaño del kernel 5x5, sigma 0

# Aplicar desenfoque mediano
median_blurred = cv2.medianBlur(image, 5)  # Tamaño del kernel 5

# Mostrar resultados
cv2.imshow('Original', image)
cv2.imshow('Convolución Personalizada', convolved_image)
cv2.imshow('Desenfoque Promedio', average_blurred)
cv2.imshow('Desenfoque Gaussiano', gaussian_blurred)
cv2.imshow('Desenfoque Mediano', median_blurred)

cv2.waitKey(0)
cv2.destroyAllWindows()
