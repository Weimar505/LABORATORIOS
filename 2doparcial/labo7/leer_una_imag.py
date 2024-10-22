import cv2
#import matplotlib.pyplot as plt

# Leemos la imagen
# Utiliza OpenCV (cv2) para leer la imagen llamada "wall-e.jpg"
image = cv2.imread("wall-e.jpg")

# Verificar si la imagen se ha cargado correctamente
if image is None:
    print("Error: No se pudo cargar la imagen.")
else:
    # Convertir la imagen a escala de grises
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Mostrar la imagen en escala de grises usando OpenCV
    cv2.imshow("Imagen en Escala de Grises", image_gray)

    # Esperar a que se cierre la ventana
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Si deseas mostrar la imagen con matplotlib, descomenta lo siguiente:
# plt.imshow(image_gray, cmap="gray")
# plt.axis('off')  # Opcional: Oculta los ejes
# plt.show()
