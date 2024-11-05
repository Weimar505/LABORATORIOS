import cv2


video_path = 'bouncing.mp4'  
cap = cv2.VideoCapture(video_path)

# Crear el sustractor de fondo KNN (Objeto)
sin_fondo = cv2.createBackgroundSubtractorKNN()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar el sustractor de fondo KNN (Metodo apply del objeto)
    mascara = sin_fondo.apply(frame)

    #cv2.imshow('Original Frame', frame)
    cv2.imshow('KNN', mascara)

    # Esperar 30 ms y salir con la tecla 'q'
    if cv2.waitKey(30) == ord('q'):
        break

cap.release() #libera el objeto de video
cv2.destroyAllWindows()# Cerrar ventanas