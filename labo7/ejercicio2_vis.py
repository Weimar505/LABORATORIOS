import cv2

def resize_img(img, width, height):
    new_size = (width, height)
    resized_img = cv2.resize(img, new_size)
    return resized_img

def get_size_option():
    print("Selecciona un tamaño para redimensionar la imagen:")
    print("1. Original")
    print("2. Pequeño (300x300)")
    print("3. Mediano (500x500)")
    print("4. Grande (1000x1000)")

    while True:
        option = input("Ingresa el número de la opción deseada: ")
        if option in ['1', '2', '3', '4']:
            return option
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Cargar la imagen
img = cv2.imread("wall-e.jpg")

# Obtener la opción del usuario
size_option = get_size_option()

# Redimensionar según la opción seleccionada
if size_option == '1':
    # Tamaño original (no se redimensiona)
    resized_img = img
elif size_option == '2':
    resized_img = resize_img(img, 300, 300)
elif size_option == '3':
    resized_img = resize_img(img, 500, 500)
elif size_option == '4':
    resized_img = resize_img(img, 1000, 1000)

# Mostrar la imagen redimensionada
cv2.imshow("Resized Image", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
