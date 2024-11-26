import cv2
import tensorflow as tf
import numpy as np

# Cargar el modelo entrenado desde la dirección del segundo código
model = tf.keras.models.load_model("/home/fernando/Escritorio/inteligencia_artificial/entrenamiento_2do_parcial/modelov1.keras")

# Diccionario de etiquetas
etiquetas = {
    0: "Borrador",
    1: "Marcador Azul",
    2: "Marcador Negro",
    3: "Marcador Rojo",
    4: "Ninguno"
}

# Preprocesar cuadro
def preprocess_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Cambiar a RGB si es necesario
    frame_resized = cv2.resize(frame_rgb, (224, 224))  # Cambia según las dimensiones de entrada
    frame_normalized = frame_resized / 255.0  # Ajusta la normalización si es necesario
    return np.expand_dims(frame_normalized, axis=0)

# Inicializar la cámara
cap = cv2.VideoCapture(2)  # Mantener la cámara 2 como en el primer código
if not cap.isOpened():
    print("No se puede acceder a la cámara.")
    exit()

print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame.")
        break

    preprocessed_frame = preprocess_frame(frame)
    
    # Depuración: verificar dimensiones y valores
    print(f"Dimensiones del cuadro preprocesado: {preprocessed_frame.shape}")

    prediction = model.predict(preprocessed_frame, verbose=0)
    print(f"Predicción completa: {prediction}")

    predicted_class = np.argmax(prediction, axis=1)[0]
    label = etiquetas.get(predicted_class, "Desconocido")
    print(f"Predicción: {label}")

    # Mostrar la predicción en el cuadro
    cv2.putText(frame, f"Prediccion: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Video en tiempo real', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()