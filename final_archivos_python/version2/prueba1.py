import cv2
import numpy as np
import tensorflow as tf

# Ruta del modelo TFLite
tflite_model_path = "object_detection_model.tflite"

# Cargar el modelo TFLite
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Obtener detalles de entrada y salida del modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Tamaño de entrada del modelo
input_shape = input_details[0]['shape'][1:3]

# Función para realizar la predicción con el modelo TFLite
def detect_objects(frame):
    resized_frame = cv2.resize(frame, input_shape)
    normalized_frame = resized_frame / 255.0
    input_data = np.expand_dims(normalized_frame, axis=0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obtener la salida de las cajas delimitadoras y las clases
    bbox_output = interpreter.get_tensor(output_details[0]['index'])[0]  # Asegurarse de tomar el primer tensor
    class_output = interpreter.get_tensor(output_details[1]['index'])[0]

    print("bbox_output:", bbox_output)  # Imprime las cajas delimitadoras
    print("class_output:", class_output)  # Imprime las clases y sus probabilidades

    return bbox_output, class_output
# Función para dibujar bounding boxes en la imagen
def draw_bounding_box(frame, bbox, confidence, label):
    height, width, _ = frame.shape
    # Verificar la forma de bbox y asegurarse de que tenga 4 elementos
    if len(bbox) == 4:
        xmin = int(bbox[0] * width)
        ymin = int(bbox[1] * height)
        xmax = int(bbox[2] * width)
        ymax = int(bbox[3] * height)

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        label_text = f"{label}: {confidence * 100:.2f}%"
        cv2.putText(frame, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Inicializar la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

# Crear una única ventana para la visualización
cv2.namedWindow("Detección de Pelusa", cv2.WINDOW_NORMAL)

print("Presiona 'q' para salir.")

# Loop para procesar fotogramas en tiempo real
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el fotograma.")
        break

    # Realizar detección de objetos
    bbox_output, class_output = detect_objects(frame)

    # Iterar sobre todas las detecciones
    for i in range(len(bbox_output)):
        # Obtener la probabilidad de la clase con mayor confianza
        confidence = class_output[i]  # La probabilidad de la clase
        class_id = np.argmax(class_output)  # Índice de la clase con la mayor probabilidad

        # Si la clase detectada es "pelusa" (asumimos que la clase 0 es pelusa)
        if class_id == 0 and confidence > 0.3:  # Umbral de confianza
            draw_bounding_box(frame, bbox_output[i], confidence, "Pelusa")

    # Mostrar el fotograma con detecciones en la ventana abierta
    cv2.imshow("Detección de Pelusa", frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()