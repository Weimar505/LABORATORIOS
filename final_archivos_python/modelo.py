import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Carga el modelo .tflite
MODEL_PATH = "model.tflite"  # Cambia esto por la ruta a tu modelo

# Inicializa el int�rprete de TensorFlow Lite
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Obtiene detalles del modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape'][1:3]  # Altura y ancho esperados
input_dtype = input_details[0]['dtype']  # Tipo de datos esperado

# Configura la c�mara
cap = cv2.VideoCapture(0)  # Cambia a 2 para usar la c�mara en /dev/video2

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

    # Redimensiona la imagen al tama�o esperado por el modelo
    input_image = cv2.resize(frame, input_shape)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Ajusta el tipo de datos de entrada seg�n lo que espera el modelo
    if input_dtype == np.uint8:
        input_image = input_image.astype(np.uint8)
    elif input_dtype == np.float32:
        input_image = input_image.astype(np.float32) / 255.0

    input_image = np.expand_dims(input_image, axis=0)

    # Realiza la inferencia
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()

    # Obtiene los resultados
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_label_index = np.argmax(output_data)
    confidence = output_data[0][predicted_label_index]

    # Muestra el resultado en la imagen
    text = f"�ndice: {predicted_label_index}, Confianza: {confidence*100:.2f}%"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Muestra la imagen con el resultado en una sola ventana
    cv2.imshow("Detecci�n en tiempo real", frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
