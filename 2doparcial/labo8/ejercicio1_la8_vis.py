import cv2  # Importar la librería OpenCV

# Cargar el video
video = cv2.VideoCapture('prueba.mp4')  # Reemplaza 'video.mp4' con la ruta de tu archivo de video

# Verificar si el video se ha cargado correctamente
if not video.isOpened():
    print("Error al cargar el video.")
    exit()

# Bucle para procesar cada cuadro del video
while True:
    # Leer cada cuadro del video
    ret, frame = video.read()
    
    # Si no hay más cuadros, salir del bucle sin cerrar las ventanas
    if not ret:
        print("Fin del video. Presiona cualquier tecla para cerrar.")
        break

    # Redimensionar el cuadro a 400x600 (ancho, alto)
    resized_frame = cv2.resize(frame, (400, 600))

    # Crear un detector de bordes con Canny y mostrar el resultado
    edges = cv2.Canny(resized_frame, 100, 200)

    # Dividir el cuadro en dos mitades y mostrarlas en ventanas separadas
    mitad_izquierda = resized_frame[:, :300]  # Mitad izquierda
    mitad_derecha = resized_frame[:, 300:]    # Mitad derecha

    # Dividir el cuadro en cuatro cuadrantes y mostrarlos en ventanas separadas
    altura, ancho, _ = resized_frame.shape  # Obtener dimensiones del cuadro redimensionado
    mitad_ancho, mitad_altura = ancho // 2, altura // 2  # Calcular la mitad del ancho y altura

    # Crear cada cuadrante
    cuadrante_1 = resized_frame[:mitad_altura, :mitad_ancho]  # Superior izquierda
    cuadrante_2 = resized_frame[:mitad_altura, mitad_ancho:]  # Superior derecha
    cuadrante_3 = resized_frame[mitad_altura:, :mitad_ancho]  # Inferior izquierda
    cuadrante_4 = resized_frame[mitad_altura:, mitad_ancho:]  # Inferior derecha

    # Mostrar las distintas ventanas con resultados
    cv2.imshow('Video Original', resized_frame)  # Cuadro redimensionado original
    cv2.imshow('Bordes', edges)  # Cuadro con detector de bordes aplicado
    cv2.imshow('Mitad Izquierda', mitad_izquierda)  # Mitad izquierda
    cv2.imshow('Mitad Derecha', mitad_derecha)  # Mitad derecha
    cv2.imshow('Cuadrante 1 - Superior Izquierda', cuadrante_1)  # Cuadrante superior izquierda
    cv2.imshow('Cuadrante 2 - Superior Derecha', cuadrante_2)  # Cuadrante superior derecha
    cv2.imshow('Cuadrante 3 - Inferior Izquierda', cuadrante_3)  # Cuadrante inferior izquierda
    cv2.imshow('Cuadrante 4 - Inferior Derecha', cuadrante_4)  # Cuadrante inferior derecha

    # Presionar 'q' para salir del bucle durante la reproducción
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


# Esperar a que el usuario presione una tecla para cerrar las ventanas
cv2.waitKey(0)  # Espera indefinidamente hasta que se presione una tecla
video.release()  # Libera el video capturado
cv2.destroyAllWindows()  # Cierra todas las ventanas de OpenCV