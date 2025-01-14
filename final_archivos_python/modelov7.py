import os
import warnings
import tensorflow as tf
import cv2
import numpy as np
import serial  # Para la comunicación UART

# Configuración de UART
UART_PORT = '/dev/ttyACM0'  # Cambia esto al puerto adecuado
UART_BAUD_RATE = 9600        # La velocidad de transmisión UART
uart = serial.Serial(UART_PORT, UART_BAUD_RATE)

# Configuración directa
cwd = os.getcwd()
MODEL_PATH = "/home/pi/vision_artificial/inteligencia_artificial/embebidosII"  # Cambia esto a la ubicación real del modelo
MODEL_NAME = "model.tflite"       # Cambia esto si el nombre del modelo es diferente
DETECTION_THRESHOLD = 0.55
CLASSES = ['pelusa']

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

# Define una lista de colores para la visualización
COLORS = np.random.randint(0, 255, size=(len(CLASSES), 3), dtype=np.uint8)

def preprocess_image(image_path, input_size):
    ''' Preprocesa la imagen de entrada para pasarla al modelo TFLite '''
    img = tf.io.read_file(image_path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.uint8)
    original_image = img
    resized_img = tf.image.resize(img, input_size)
    resized_img = resized_img[tf.newaxis, :]
    resized_img = tf.cast(resized_img, dtype=tf.uint8)
    return resized_img, original_image

def detect_objects(interpreter, image, threshold):
    ''' Devuelve una lista de resultados de detección, cada uno con la información del objeto '''
    signature_fn = interpreter.get_signature_runner()

    # Pasa la imagen de entrada al modelo
    output = signature_fn(images=image)

    # Obtiene todas las salidas del modelo
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

def send_uart_data(data):
    ''' Envía los datos por UART '''
    uart.write(data.encode())  # Enviar el dato como string

def run_odt_and_draw_results(image_path, interpreter, threshold=0.5):
    ''' Ejecuta la detección de objetos en la imagen de entrada y dibuja los resultados '''
    # Carga las dimensiones de entrada requeridas por el modelo
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

    # Carga la imagen de entrada y préprocesala
    preprocessed_image, original_image = preprocess_image(
        image_path,
        (input_height, input_width)
    )

    # Ejecuta la detección de objetos en la imagen de entrada
    results = detect_objects(interpreter, preprocessed_image, threshold=threshold)

    # Prepara la imagen original para dibujar los resultados
    original_image_np = original_image.numpy().astype(np.uint8)

    # Define divisiones verticales para la imagen (3 cuadrantes)
    quadrant_width = original_image_np.shape[1] // 3
    cv2.line(original_image_np, (quadrant_width, 0), (quadrant_width, original_image_np.shape[0]), (255, 0, 0), 2)
    cv2.line(original_image_np, (2 * quadrant_width, 0), (2 * quadrant_width, original_image_np.shape[0]), (255, 0, 0), 2)

    if len(results) == 0:
        # Si no se detectan objetos, enviar "Objeto no detectado"
        send_uart_data("apagado\n")
    else:
        for obj in results:
            # Convierte las coordenadas relativas de la caja delimitadora a absolutas
            ymin, xmin, ymax, xmax = obj['bounding_box']
            xmin = int(xmin * original_image_np.shape[1])
            xmax = int(xmax * original_image_np.shape[1])
            ymin = int(ymin * original_image_np.shape[0])
            ymax = int(ymax * original_image_np.shape[0])

            # Determina en qué cuadrante se encuentra el objeto
            center_x = (xmin + xmax) // 2
            if center_x < quadrant_width:
                quadrant = 1  # Cuadrante izquierdo
            elif center_x < 2 * quadrant_width:
                quadrant = 2  # Cuadrante central
            else:
                quadrant = 3  # Cuadrante derecho

            # Envía el cuadrante detectado por UART
            send_uart_data(f"{quadrant}\n")

            # Encuentra el índice de la clase del objeto actual
            class_id = int(obj['class_id'])

            # Dibuja la caja delimitadora y la etiqueta en la imagen
            color = [int(c) for c in COLORS[class_id]]
            cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 2)
            y = ymin - 15 if ymin - 15 > 15 else ymin + 15
            label = "{}: {:.0f}% (Cuadrante {})".format(CLASSES[class_id], obj['score'] * 100, quadrant)
            cv2.putText(original_image_np, label, (xmin, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Devuelve la imagen final
    original_uint8 = original_image_np.astype(np.uint8)
    return original_uint8

# Configura la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# Configura la ventana para que sea redimensionable
cv2.namedWindow("Detección en tiempo real", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detección en tiempo real", 1280, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    # Guarda el cuadro como imagen temporal para procesar
    temp_image_path = os.path.join(cwd, 'temp_frame.jpg')
    cv2.imwrite(temp_image_path, frame)

    # Corre la inferencia usando la función de ayuda
    detection_result_image = run_odt_and_draw_results(
        temp_image_path,  # Pasa el archivo temporal
        interpreter,
        threshold=DETECTION_THRESHOLD
    )

    # Convierte el resultado a formato OpenCV si es necesario
    detection_result_image = cv2.cvtColor(np.array(detection_result_image), cv2.COLOR_RGB2BGR)

    # Muestra la imagen con los resultados
    cv2.imshow("Detección en tiempo real", detection_result_image)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()

# Cierra la conexión UART
uart.close()

print('Detección finalizada.')
