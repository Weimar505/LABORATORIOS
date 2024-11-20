import cv2
import numpy as np

# Función para detectar el color de una figura en base a una imagen en espacio de color HSV
def figColor(imagenHSV):
    color = "Desconocido"  # Valor predeterminado en caso de que no se detecte ningún color

    # Definir rangos de color en HSV para diferentes colores tono saturacion y brillo 

    # Rojo
    rojoBajo1 = np.array([0, 100, 20], np.uint8)
    rojoAlto1 = np.array([10, 255, 255], np.uint8)
    rojoBajo2 = np.array([175, 100, 20], np.uint8)
    rojoAlto2 = np.array([180, 255, 255], np.uint8)

    # Naranja
    naranjaBajo = np.array([11, 100, 20], np.uint8)
    naranjaAlto = np.array([19, 255, 255], np.uint8)

    # Amarillo
    amarilloBajo = np.array([20, 100, 20], np.uint8)
    amarilloAlto = np.array([32, 255, 255], np.uint8)

    # Verde
    verdeBajo = np.array([36, 100, 20], np.uint8)
    verdeAlto = np.array([85, 255, 255], np.uint8)  # Aumentado para incluir más tonos de verde

    # Celeste
    celesteBajo = np.array([86, 100, 20], np.uint8)
    celesteAlto = np.array([100, 255, 255], np.uint8)

    # Violeta
    violetaBajo = np.array([130, 100, 20], np.uint8)
    violetaAlto = np.array([145, 255, 255], np.uint8)

    # Rosa
    rosaBajo = np.array([146, 100, 20], np.uint8)
    rosaAlto = np.array([170, 255, 255], np.uint8)

    # Crear máscaras para cada color usando los límites definidos
    maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
    maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
    maskRojo = cv2.add(maskRojo1, maskRojo2)
    maskNaranja = cv2.inRange(imagenHSV, naranjaBajo, naranjaAlto)
    maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
    maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
    maskCeleste = cv2.inRange(imagenHSV, celesteBajo, celesteAlto)
    maskVioleta = cv2.inRange(imagenHSV, violetaBajo, violetaAlto)
    maskRosa = cv2.inRange(imagenHSV, rosaBajo, rosaAlto)

    # Verificar qué color está presente en la imagen usando los contornos en cada máscara
    cntsRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsNaranja = cv2.findContours(maskNaranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsVerde = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsCeleste = cv2.findContours(maskCeleste, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsVioleta = cv2.findContours(maskVioleta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsRosa = cv2.findContours(maskRosa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # Asignar el color detectado en base a la presencia de contornos en cada máscara
    if len(cntsRojo) > 0: 
        color = 'Rojo'
    elif len(cntsNaranja) > 0: 
        color = 'Naranja'
    elif len(cntsAmarillo) > 0: 
        color = 'Amarillo'
    elif len(cntsVerde) > 0: 
        color = 'Verde'
    elif len(cntsCeleste) > 0: 
        color = 'Celeste'
    elif len(cntsVioleta) > 0: 
        color = 'Violeta'
    elif len(cntsRosa) > 0: 
        color = 'Rosa'

    return color  # Retornar el color detectado


# Función para detectar el tipo de figura geométrica en base al número de lados
def figName(contorno, width, height):
    epsilon = 0.01 * cv2.arcLength(contorno, True)
    approx = cv2.approxPolyDP(contorno, epsilon, True)

    # Clasificar la figura en base al número de lados del contorno
    if len(approx) == 3:
        namefig = 'Triangulo'
    elif len(approx) == 4:
        aspect_ratio = float(width) / height
        if 0.95 <= aspect_ratio <= 1.05:  # Permitir tolerancia para diferenciar entre cuadrado y rectángulo
            namefig = 'Cuadrado'
        else:
            namefig = 'Rectangulo'
    elif len(approx) == 5:
        namefig = 'Pentagono'
    elif len(approx) == 6:
        namefig = 'Hexagono'
    elif len(approx) > 10:
        namefig = 'Circulo'
    else:
        namefig = 'Forma desconocida'

    return namefig  # Retornar el nombre de la figura detectada


# Cargar la imagen y convertirla a escala de grises
imagen = cv2.imread('figuras.png')
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar Canny para detectar bordes
canny = cv2.Canny(gray, 10, 150)
canny = cv2.dilate(canny, None, iterations=1)
canny = cv2.erode(canny, None, iterations=1)

# Encontrar contornos en la imagen de bordes
cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convertir la imagen a espacio de color HSV para detección de color
imageHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Procesar cada contorno detectado
for c in cnts:
    # Calcular el rectángulo delimitador y crear una máscara para el contorno
    x, y, w, h = cv2.boundingRect(c)
    imAux = np.zeros(imagen.shape[:2], dtype="uint8")
    imAux = cv2.drawContours(imAux, [c], -1, 255, -1)

    # Aplicar la máscara en el espacio HSV
    maskHSV = cv2.bitwise_and(imageHSV, imageHSV, mask=imAux)

    # Detectar el nombre de la figura y el color usando las funciones definidas
    name = figName(c, w, h)
    color = figColor(maskHSV)
    nameColor = f"{name} {color}"

    # Dibujar el nombre de la figura y el color sobre la imagen original
    cv2.putText(imagen, nameColor, (x, y - 5), 1, 0.8, (0, 255, 0), 1)

# Mostrar la imagen final con los nombres de las figuras y sus colores
cv2.imshow('Figuras y Colores', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()