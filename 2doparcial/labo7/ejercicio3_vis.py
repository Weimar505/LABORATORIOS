import cv2

# Función para rotar la imagen 90 grados
def rotate_image(img):
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# Cargar la imagen
img = cv2.imread("wall-e.jpg")

# Verificar si la imagen se cargó correctamente
if img is None:
    print("Error al cargar la imagen.")
    exit()

while True:
    # Mostrar la imagen
    cv2.imshow("Image", img)

    # Esperar a que se presione una tecla
    key = cv2.waitKey(0)

    # Rotar la imagen si se presiona cualquier tecla
    img = rotate_image(img)

    # Si se presiona 'q', salir del bucle
    if key == ord('q'):
        break

# Cerrar todas las ventanas
cv2.destroyAllWindows()
