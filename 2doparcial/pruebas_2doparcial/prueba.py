import cv2
import numpy as np
import tensorflow as tf
from abc import ABC, abstractmethod

# Cargar el modelo entrenado
modelo = tf.keras.models.load_model("/home/pi/vision_artificial/inteligencia_artificial/modelo_gatos.h5")

# Diccionario para mapear las etiquetas con los nombres de las clases
etiquetas = {
    0: "Aika",
    1: "Simba",
    2: "Suzuka",
    3: "Tsuki"
}

# Umbral para clasificar un gato (probabilidad mínima requerida)
umbral = 0.6  # 50%

# Definir la clase abstracta para la captura de video
class VideoCaptureAbs(ABC):
    @abstractmethod
    def display_camera(self):
        pass

    @abstractmethod
    def stop_display(self):
        pass

    @abstractmethod
    def camera_visualization(self):
        pass

# Definir la clase que maneja la captura de video
class VideoCapture(VideoCaptureAbs):
    def __init__(self, camera) -> None:
        self.camera = camera
        self.displayed = False

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("No se pudo capturar el cuadro. Verifica la cámara.")
                self.stop_display()
                break

            # Redimensionar la imagen al tamaño que espera el modelo (por ejemplo, 100x100)
            imagen = cv2.resize(frame, (100, 100))

            # Normalizar la imagen
            imagen = imagen / 255.0

            # Expandir las dimensiones para que coincida con el formato de entrada del modelo (1, 100, 100, 3)
            imagen = np.expand_dims(imagen, axis=0)

            # Realizar la predicción para el frame capturado
            prediccion = modelo.predict(imagen)

            # Obtener la probabilidad más alta y su índice
            probabilidad_max = np.max(prediccion)
            etiqueta_predicha = np.argmax(prediccion)

            # Determinar la etiqueta basada en el umbral
            if probabilidad_max >= umbral:
                nombre_etiqueta = etiquetas.get(etiqueta_predicha, "Desconocido")
            else:
                nombre_etiqueta = "Gato no identificado"

            # Mostrar la etiqueta predicha en la imagen
            cv2.putText(frame, nombre_etiqueta, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Mostrar el frame con la predicción en tiempo real
            cv2.imshow('camera', frame)

            # Presionar 'q' para salir
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.stop_display()

# Inicializar la cámara
camera = cv2.VideoCapture(0)  # Cambiar el índice si no detecta la cámara correcta
if not camera.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    camera_object = VideoCapture(camera)
    camera_object.display_camera()

# Liberar la cámara y cerrar ventanas al finalizar
camera.release()
cv2.destroyAllWindows()
