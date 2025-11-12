import os
import cv2
from tqdm import tqdm

# ====================================
# --- CONFIGURAÇÕES ---
# ====================================

frames_folder = "audio_frames"
output_video = "badapple_video.mp4"
fps = 30

# ====================================
# --- LISTA E ORDENA OS FRAMES ---
# ====================================

frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith(".png")])
if not frame_files:
    raise ValueError("There is no frame there!")

# Lê o primeiro frame para pegar tamanho
first_frame_path = os.path.join(frames_folder, frame_files[0])
frame = cv2.imread(first_frame_path)
if frame is None:
    raise FileNotFoundError(f"Error reading frame: {first_frame_path}")

height, width, channels = frame.shape
rotated_size = (height, width)  # largura e altura invertidas após rotação

# ====================================
# --- CONFIGURAÇÃO DO VÍDEO ---
# ====================================

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # type: ignore
video_writer = cv2.VideoWriter(output_video, fourcc, fps, rotated_size)

# ====================================
# --- ESCREVE CADA FRAME ---
# ====================================

for frame_file in tqdm(frame_files, desc="Generating video", ncols=80):
    frame_path = os.path.join(frames_folder, frame_file)
    img = cv2.imread(frame_path)
    if img is None:
        print(f"Warning: Frame {frame_file} cannot be read, skipping.")
        continue

    # Gira 90° anti-horário para não ficar de cabeça para baixo
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    video_writer.write(rotated_img)

video_writer.release()
print(f"\nSaved Video: {output_video} ({fps} FPS)")
