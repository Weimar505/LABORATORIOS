import os
import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
import cv2
import numpy as np

# Configuración directa
cwd = os.getcwd()
MODEL_PATH = "/home/pi/vision_artificial/inteligencia_artificial/embebidosII"  # Cambia esto a la ubicación real del modelo
MODEL_NAME = "model.tflite"       # Cambia esto si el nombre del modelo es diferente
DETECTION_THRESHOLD = 0.55

# Verifica que el modelo exista
model_path = f'{MODEL_PATH}/{MODEL_NAME}'
if not os.path.exists(model_path):
    print(f"Error: No se encontró el modelo en la ruta especificada: {model_path}")
    exit()

# Inicializa el intérprete de TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Obtén detalles de entrada y salida del modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Configura la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

cv2.namedWindow("Detección en tiempo real", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detección en tiempo real", 1280, 720)

def determinar_cuadrante(x, y, frame_width, frame_height):
    tercio_ancho = frame_width // 3
    if x < tercio_ancho:
        return 1  # Izquierdo
    elif x < 2 * tercio_ancho:
        return 2  # Central
    else:
        return 3  # Derecho

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    frame_height, frame_width, _ = frame.shape

    # Preprocesar la imagen para el modelo
    input_shape = input_details[0]['shape']
    input_data = cv2.resize(frame, (input_shape[2], input_shape[1]))

    if input_details[0]['dtype'] == np.uint8:
        input_data = np.expand_dims(input_data, axis=0)
    else:
        input_data = (np.expand_dims(input_data, axis=0) / 255.0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obtiene las detecciones del modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Verifica la forma del tensor de salida
    if len(output_data.shape) == 2:  # Varias detecciones esperadas
        detections = output_data
    else:
        print("Formato inesperado de salida del modelo. Verifica el modelo.")
        break

    detection_result_image = frame.copy()

    # Dibuja los cuadrantes
    tercio_ancho = frame_width // 3
    cv2.line(detection_result_image, (tercio_ancho, 0), (tercio_ancho, frame_height), (0, 255, 0), 2)
    cv2.line(detection_result_image, (2 * tercio_ancho, 0), (2 * tercio_ancho, frame_height), (0, 255, 0), 2)

    # Procesa las detecciones
    for detection in detections:
        if len(detection) >= 4:  # Verifica que la detección contenga los valores necesarios
            ymin, xmin, ymax, xmax = detection[0:4]
            score = detection[4] if len(detection) > 4 else 0.0

            if score > DETECTION_THRESHOLD:
                # Convierte las coordenadas normalizadas a píxeles
                xmin = int(xmin * frame_width)
                ymin = int(ymin * frame_height)
                xmax = int(xmax * frame_width)
                ymax = int(ymax * frame_height)

                # Calcula el centro del bounding box
                x_center = (xmin + xmax) // 2
                y_center = (ymin + ymax) // 2

                cuadrante = determinar_cuadrante(x_center, y_center, frame_width, frame_height)

                # Dibuja el bounding box y el cuadrante
                cv2.rectangle(detection_result_image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                label = f"Cuadrante: {cuadrante}"
                cv2.putText(detection_result_image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Imprime el cuadrante en la consola
                print(f"Objeto detectado en el cuadrante: {cuadrante}")

    # Mostrar imagen procesada
    cv2.imshow("Detección en tiempo real", detection_result_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()