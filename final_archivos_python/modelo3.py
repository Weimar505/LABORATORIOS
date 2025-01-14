import os
import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
import cv2
import numpy as np
from helper_functions import run_odt_and_draw_results

# Configuraci�n directa
cwd = os.getcwd()
MODEL_PATH = "/home/pi/vision_artificial/inteligencia_artificial/embebidosII"  # Cambia esto a la ubicaci�n real del modelo
MODEL_NAME = "model.tflite"       # Cambia esto si el nombre del modelo es diferente
DETECTION_THRESHOLD = 0.55

# Verifica que el modelo exista
model_path = f'{MODEL_PATH}/{MODEL_NAME}'
if not os.path.exists(model_path):
    print(f"Error: No se encontr� el modelo en la ruta especificada: {model_path}")
    exit()

# Inicializa el int�rprete de TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Obtiene detalles del modelo
input_details = interpreter.get_input_details()
input_shape = input_details[0]['shape'][1:3]  # Altura y ancho esperados
input_dtype = input_details[0]['dtype']  # Tipo de datos esperado

# Configura la c�mara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo acceder a la c�mara.")
    exit()

# Configura la ventana para que sea redimensionable
cv2.namedWindow("Detecci�n en tiempo real", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detecci�n en tiempo real", 1280, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    # Guarda el cuadro como imagen temporal para procesar
    temp_image_path = os.path.join(cwd, 'temp_frame.jpg')
    cv2.imwrite(temp_image_path, frame)

    # Corre la inferencia usando la funci�n de ayuda
    detection_result_image = run_odt_and_draw_results(
        temp_image_path,  # Pasa el archivo temporal
        interpreter,
        threshold=DETECTION_THRESHOLD
    )

    # Convierte el resultado a formato OpenCV si es necesario
    detection_result_image = cv2.cvtColor(np.array(detection_result_image), cv2.COLOR_RGB2BGR)

    # Muestra la imagen con los resultados
    cv2.imshow("Detecci�n en tiempo real", detection_result_image)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()

print('Detecci�n finalizada.')

