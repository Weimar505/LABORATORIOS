import os
import tensorflow as tf
import cv2
import numpy as np
import serial

# Configuración directa
cwd = os.getcwd()
MODEL_PATH = "/home/pi/vision_artificial/inteligencia_artificial/embebidosII"
MODEL_NAME = "model.tflite"
CLASSES = ['pelusa']

# Configura el puerto UART
UART_PORT = '/dev/ttyACM0'  # Cambiar al puerto de la Tiva
UART_BAUDRATE = 9600
try:
    uart = serial.Serial(UART_PORT, UART_BAUDRATE)
except Exception as e:
    print(f"Error al configurar el puerto UART: {e}")
    exit()

# Verifica que el modelo exista
model_path = f'{MODEL_PATH}/{MODEL_NAME}'
if not os.path.exists(model_path):
    print(f"Error: No se encontró el modelo en la ruta especificada: {model_path}")
    exit()

# Inicializa el intérprete de TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Obtiene detalles del modelo
input_details = interpreter.get_input_details()
input_shape = input_details[0]['shape'][1:3]  # Altura y ancho esperados
input_dtype = input_details[0]['dtype']  # Tipo de datos esperado

# Funciones Helper
COLORS = np.random.randint(0, 255, size=(len(CLASSES), 3), dtype=np.uint8)

def preprocess_image(image_path, input_size):
    img = tf.io.read_file(image_path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.uint8)
    original_image = img
    resized_img = tf.image.resize(img, input_size)
    resized_img = resized_img[tf.newaxis, :]
    resized_img = tf.cast(resized_img, dtype=tf.uint8)
    return resized_img, original_image

def detect_objects(interpreter, image, threshold_min=0.5, threshold_max=0.65):
    signature_fn = interpreter.get_signature_runner()
    output = signature_fn(images=image)

    count = int(np.squeeze(output['output_0']))
    scores = np.squeeze(output['output_1'])
    classes = np.squeeze(output['output_2'])
    boxes = np.squeeze(output['output_3'])

    results = []
    for i in range(count):
        if threshold_min <= scores[i] <= threshold_max:  # Verifica el rango
            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)
    return results

def run_odt_and_draw_results(image_path, interpreter, threshold_min=0.5, threshold_max=0.65):
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
    preprocessed_image, original_image = preprocess_image(
        image_path,
        (input_height, input_width)
    )
    results = detect_objects(interpreter, preprocessed_image, threshold_min, threshold_max)

    original_image_np = original_image.numpy().astype(np.uint8)
    center_x = original_image_np.shape[1] // 2

    for obj in results:
        ymin, xmin, ymax, xmax = obj['bounding_box']
        xmin = int(xmin * original_image_np.shape[1])
        xmax = int(xmax * original_image_np.shape[1])
        ymin = int(ymin * original_image_np.shape[0])
        ymax = int(ymax * original_image_np.shape[0])

        class_id = int(obj['class_id'])
        color = [int(c) for c in COLORS[class_id]]
        cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 2)
        y = ymin - 15 if ymin - 15 > 15 else ymin + 15
        label = "{}: {:.0f}%".format(CLASSES[class_id], obj['score'] * 100)
        cv2.putText(original_image_np, label, (xmin, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Determina la posición horizontal
        box_center_x = (xmin + xmax) // 2
        if box_center_x < center_x - 50:
            uart.write(b'1\n')
        elif box_center_x > center_x + 50:
            uart.write(b'3\n')
        else:
            uart.write(b'2\n')

    return original_image_np.astype(np.uint8)

# Configura la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

cv2.namedWindow("Detección en tiempo real", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detección en tiempo real", 1280, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    temp_image_path = os.path.join(cwd, 'temp_frame.jpg')
    cv2.imwrite(temp_image_path, frame)

    detection_result_image = run_odt_and_draw_results(
        temp_image_path, interpreter, threshold_min=0.5, threshold_max=0.65
    )

    detection_result_image = cv2.cvtColor(np.array(detection_result_image), cv2.COLOR_RGB2BGR)
    cv2.imshow("Detección en tiempo real", detection_result_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('Detección finalizada.')