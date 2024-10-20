import cv2

# Capturar imagen desde la cámara (0 para la primera cámara conectada)
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if ret:
    cv2.imshow('Imagen Capturada', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No se pudo capturar la imagen.")

cap.release()
