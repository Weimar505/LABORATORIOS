import cv2


video_path = 'bouncing.mp4'  
cap = cv2.VideoCapture(video_path)

# Crear el sustractor de fondo MOG2 (Objeto)
sin_fondo = cv2.createBackgroundSubtractorMOG2()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar el sustractor de fondo MOG2 (metodo apply del objeto)
    mascara = sin_fondo.apply(frame)

    #cv2.imshow('Original Frame', frame)
    cv2.imshow('MOG2', mascara)

    # Esperar 30 ms y salir con la tecla 'q'
    if cv2.waitKey(30) == ord('q'):
        break

cap.release() #libera el objeto de video
cv2.destroyAllWindows()# Cerrar ventanas