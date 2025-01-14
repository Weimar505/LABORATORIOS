import cv2
import numpy as np
import tensorflow as tf

# Constantes
MODEL_PATH = "object_detection_model.tflite"
DETECTION_THRESHOLD = 0.5

# Inicialización del intérprete TFLite
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Obtén los detalles de las entradas y salidas
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Imprime los detalles de las salidas para diagnóstico
print("Detalles de las salidas del modelo:")
for i, output_detail in enumerate(output_details):
    print(f"Salida {i}: {output_detail}")

# Función para detectar objetos
def detect_objects(interpreter, image, threshold):
    """Detecta objetos usando el modelo."""
    input_index = input_details[0]['index']
    interpreter.set_tensor(input_index, image)
    interpreter.invoke()

    # Obtén las salidas del modelo
    results = []
    count_tensor = interpreter.get_tensor(output_details[0]['index'])
    count = int(count_tensor[0][0])  # Extraer el valor escalar correctamente
    scores = interpreter.get_tensor(output_details[1]['index'])[0]  # Extraer primera dimensión
    boxes = interpreter.get_tensor(output_details[2]['index'])[0]  # Extraer primera dimensión
    class_ids = interpreter.get_tensor(output_details[3]['index'])[0]  # Clase de los objetos

    for i in range(count):
        if scores[i] >= threshold:
            ymin, xmin, ymax, xmax = boxes[i]
            results.append({
                'bounding_box': (ymin, xmin, ymax, xmax),
                'score': scores[i],
                'class_id': int(class_ids[i])  # Agregar el ID de clase
            })
    return results

# Función para preprocesar la imagen
def preprocess_image(image, input_size):
    """Preprocesa la imagen para el modelo TFLite."""
    resized_image = cv2.resize(image, input_size)
    normalized_image = np.expand_dims(resized_image / 255.0, axis=0).astype(np.float32)
    return normalized_image

# Función para dibujar resultados
def draw_results(image, results):
    """Dibuja los resultados en la imagen."""
    for obj in results:
        ymin, xmin, ymax, xmax = obj['bounding_box']
        start_point = (int(xmin * image.shape[1]), int(ymin * image.shape[0]))
        end_point = (int(xmax * image.shape[1]), int(ymax * image.shape[0]))
        color = (0, 255, 0)
        thickness = 2
        cv2.rectangle(image, start_point, end_point, color, thickness)
        label = f"ID: {obj['class_id']}, Score: {obj['score']:.2f}"
        cv2.putText(image, label, (start_point[0], start_point[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
    return image

# Main para procesar video en tiempo real
if __name__ == "__main__":
    # Captura de video en tiempo real desde la cámara
    cap = cv2.VideoCapture(0)  # Usa 0 para la cámara predeterminada

    if not cap.isOpened():
        print("Error al acceder a la cámara.")
        exit()

    input_size = (input_details[0]['shape'][2], input_details[0]['shape'][1])

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo capturar el cuadro del video.")
                break

            # Preprocesar la imagen
            preprocessed_frame = preprocess_image(frame, input_size)

            # Detectar objetos
            results = detect_objects(interpreter, preprocessed_frame, DETECTION_THRESHOLD)

            # Dibujar resultados en el cuadro
            output_frame = draw_results(frame, results)

            # Mostrar el cuadro con detecciones
            cv2.imshow("Detecciones en Tiempo Real", output_frame)

            # Salir con la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error en el procesamiento: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
