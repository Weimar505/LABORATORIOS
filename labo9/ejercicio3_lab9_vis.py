import cv2
ruta_video = 'bouncing.mp4'
captura = cv2.VideoCapture(ruta_video)

sustractor_fondo = cv2.createBackgroundSubtractorKNN() # Crear el sustractor de fondo KNN

while captura.isOpened():
    ret, cuadro = captura.read()
    if not ret:
        break

    
    mascara_fg = sustractor_fondo.apply(cuadro) # Aplicar sustracción de fondo 

    
    contornos, _ = cv2.findContours(mascara_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Encontrar contornos en la máscara binaria generada

    
    for contorno in contornos: # Dibujar contornos en el marco original
        
        if cv2.contourArea(contorno) < 500: # Filtrar contornos pequeños para evitar detección de ruido
            continue
        
        cv2.drawContours(cuadro, [contorno], -1, (0, 255, 0), 2) # Dibujar el contorno en color verde

    
    cv2.imshow('Objetos en Movimiento - Contornos', cuadro) # Mostrar el marco original con los contornos dibujados

    
    if cv2.waitKey(30) == ord('q'):
        break

captura.release() # Liberar el objeto de video
cv2.destroyAllWindows() # Cerrar ventanas
