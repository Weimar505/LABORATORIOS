import os
import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
from PIL import Image
import cv2
import numpy as np
from helper_functions import run_odt_and_draw_results
import config

# Configuraci�n
cwd = os.getcwd()
MODEL_PATH = config.MODEL_PATH
MODEL_NAME = config.MODEL_NAME
DETECTION_THRESHOLD = 0.3

# Inicializa el int�rprete de TensorFlow Lite
model_path = f'{MODEL_PATH}/{MODEL_NAME}'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

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

    # Guarda el cuadro actual como imagen temporal
    temp_image_path = f'{cwd}/temp_frame.png'
    cv2.imwrite(temp_image_path, frame)

    # Redimensiona y prepara la imagen con PIL
    im = Image.open(temp_image_path)
    im.thumbnail((640, 640), Image.Resampling.LANCZOS)
    resized_image_path = f'{cwd}/resized_frame.png'
    im.save(resized_image_path, 'PNG')

    # Corre la inferencia usando la funci�n de ayuda
    detection_result_image = run_odt_and_draw_results(
        resized_image_path,
        interpreter,
        threshold=DETECTION_THRESHOLD
    )

    # Convierte el resultado a formato OpenCV
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
