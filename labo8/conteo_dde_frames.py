import cv2

# Cargar el video
video = cv2.VideoCapture('prueba.mp4')  # Reemplaza 'video.mp4' con la ruta de tu archivo de video

# Verificar si el video se ha cargado correctamente
if not video.isOpened():
    print("Error al cargar el video.")
    exit()

# Obtener la cantidad total de cuadros (frames) del video
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# Obtener la tasa de fotogramas (frames per second)
fps = video.get(cv2.CAP_PROP_FPS)
# Calcular la duración del video en segundos
duration = total_frames / fps

print(f"Total de frames en el video: {total_frames}")
print(f"Tasa de fotogramas (FPS): {fps}")
print(f"Duración del video: {duration:.2f} segundos")

# Liberar el recurso de video
video.release()