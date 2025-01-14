import os
import warnings
import tensorflow as tf
import cv2
import numpy as np
import serial  # Biblioteca para comunicaci�n UART

# Configuraci�n UART
UART_PORT = '/dev/ttyACM0'  # Cambia esto al puerto correcto de tu Raspberry Pi
UART_BAUDRATE = 9600
ser = serial.Serial(UART_PORT, UART_BAUDRATE)

# Configuraci�n directa
cwd = os.getcwd()
MODEL_PATH = "/home/pi/vision_artificial/inteligencia_artificial/embebidosII"
MODEL_NAME = "model.tflite"
DETECTION_THRESHOLD = 0.55
CLASSES = ['pelusa']

model_path = f'{MODEL_PATH}/{MODEL_NAME}'
if not os.path.exists(model_path):
    print(f"Error: No se encontr� el modelo en la ruta especificada: {model_path}")
    exit()

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
input_shape = input_details[0]['shape'][1:3]
input_dtype = input_details[0]['dtype']

COLORS = np.random.randint(0, 255, size=(len(CLASSES), 3), dtype=np.uint8)

def preprocess_image(image, input_size):
    img = tf.image.resize(image, input_size)
    img = tf.cast(img, dtype=tf.uint8)
    return img[tf.newaxis, :]

def detect_objects(interpreter, image, threshold):
    signature_fn = interpreter.get_signature_runner()
    output = signature_fn(images=image)
    count = int(np.squeeze(output['output_0']))
    scores = np.squeeze(output['output_1'])
    classes = np.squeeze(output['output_2'])
    boxes = np.squeeze(output['output_3'])

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)
    return results

def control_movement(center_x, frame_center_x, tolerance=50):
    if abs(center_x - frame_center_x) <= tolerance:
        ser.write(b'centro\n')  # Enviar comando para centrar
    elif center_x < frame_center_x:
        ser.write(b'izquierda\n')  # Enviar comando para girar izquierda
    elif center_x > frame_center_x:
        ser.write(b'derecha\n')  # Enviar comando para girar derecha

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo acceder a la c�mara.")
    exit()

cv2.namedWindow("Detecci�n en tiempo real", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detecci�n en tiempo real", 1280, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    frame_height, frame_width, _ = frame.shape
    frame_center_x = frame_width // 2

    input_tensor = preprocess_image(tf.convert_to_tensor(frame), input_shape)
    results = detect_objects(interpreter, input_tensor, threshold=DETECTION_THRESHOLD)

    for obj in results:
        ymin, xmin, ymax, xmax = obj['bounding_box']
        xmin = int(xmin * frame_width)
        xmax = int(xmax * frame_width)
        ymin = int(ymin * frame_height)
        ymax = int(ymax * frame_height)

        center_x = (xmin + xmax) // 2
        center_y = (ymin + ymax) // 2

        control_movement(center_x, frame_center_x)

        color = [int(c) for c in COLORS[int(obj['class_id'])]]
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.circle(frame, (center_x, center_y), 5, color, -1)
        label = "{}: {:.0f}%".format(CLASSES[int(obj['class_id'])], obj['score'] * 100)
        cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Detecci�n en tiempo real", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
print('Detecci�n finalizada.')

