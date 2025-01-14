import cv2
import os

# Directorios
input_dir = '/home/pi/vision_artificial/inteligencia_artificial/embebidosII/video'
output_dir = '/home/pi/vision_artificial/inteligencia_artificial/embebidosII/imagenes'
os.makedirs(output_dir, exist_ok=True)

# Obtener lista de videos en la carpeta
video_files = [f for f in os.listdir(input_dir) if f.endswith(('.mp4', '.avi', '.mov'))]

for video in video_files:
    video_path = os.path.join(input_dir, video)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error al abrir el video: {video}")
        continue

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frames = 150
    step = frame_count // target_frames if frame_count > target_frames else 1

    current_frame = 0
    saved_frames = 0

    while saved_frames < target_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % step == 0:
            filename = os.path.join(output_dir, f'{os.path.splitext(video)[0]}_frame_{saved_frames:03d}.jpg')
            cv2.imwrite(filename, frame)
            saved_frames += 1
            print(f'Imagen guardada: {filename}')

        current_frame += 1

    cap.release()

cv2.destroyAllWindows()
