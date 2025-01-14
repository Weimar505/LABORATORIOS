import cv2
import numpy as np
import tensorflow as tf

# Configuración de la cámara
camera_id = 0  # Cambia si usas otra cámara
capture = cv2.VideoCapture(camera_id)

# Configuración del modelo TFLite
tflite_model_path = "object_detection_model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Detalles de entrada y salida del modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape'][1:3]  # Tamaño esperado de entrada del modelo

# Función para procesar la detección
def detect_objects(frame):
    resized_frame = cv2.resize(frame, input_shape)
    normalized_frame = resized_frame / 255.0
    input_data = np.expand_dims(normalized_frame, axis=0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obtener las salidas del modelo
    bbox_output = interpreter.get_tensor(output_details[1]['index'])[0]  # Bounding boxes
    class_output = interpreter.get_tensor(output_details[0]['index'])[0]  # Confianza de clases

    return bbox_output, class_output

# Función para dibujar bounding boxes en la imagen
def draw_bounding_box(frame, bbox, confidence):
    height, width, _ = frame.shape
    if len(bbox) == 4:  # Verificar que bbox tenga 4 valores
        xmin = int(bbox[0] * width)
        ymin = int(bbox[1] * height)
        xmax = int(bbox[2] * width)
        ymax = int(bbox[3] * height)

        # Dibujar el rectángulo
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        label = f"Confianza: {confidence * 100:.2f}%"
        # Agregar el texto del label
        cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

print("Presiona 'q' para salir.")

# Crear una única ventana para mostrar la detección
display_window_name = "Detección en tiempo real"
cv2.namedWindow(display_window_name, cv2.WINDOW_NORMAL)

# Loop para capturar y procesar fotogramas de la cámara en tiempo real
while True:
    ret, frame = capture.read()
    if not ret:
        print("Error al capturar el fotograma.")
        break

    # Realizar detección de objetos
    bbox_output, class_output = detect_objects(frame)

    # Procesar cada detección
    for i in range(bbox_output.shape[0]):  # Número de detecciones
        bbox = bbox_output[i]  # Coordenadas de la caja
        confidence = class_output[i][0]  # Confianza de la clase

        if confidence > 0.1:  # Umbral de confianza
            draw_bounding_box(frame, bbox, confidence)

    # Mostrar el fotograma con las detecciones
    cv2.imshow(display_window_name, frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
capture.release()
cv2.destroyAllWindows()