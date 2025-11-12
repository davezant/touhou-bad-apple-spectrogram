import os
import cv2
from tqdm import tqdm

frames_folder = "audio_frames"
output_video = "badapple_video.mp4"
fps = 30


frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith(".png")])
if not frame_files:
    raise ValueError("There is no frame there!")

first_frame_path = os.path.join(frames_folder, frame_files[0])
frame = cv2.imread(first_frame_path)
if frame is None:
    raise FileNotFoundError(f"Error reading frame: {first_frame_path}")

height, width, channels = frame.shape
rotated_size = (height, width)  


fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
video_writer = cv2.VideoWriter(output_video, fourcc, fps, rotated_size)


for frame_file in tqdm(frame_files, desc="Generating video", ncols=80):
    frame_path = os.path.join(frames_folder, frame_file)
    img = cv2.imread(frame_path)
    if img is None:
        print(f"Warning: Frame {frame_file} cannot be read, skipping.")
        continue


    rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    video_writer.write(rotated_img)

video_writer.release()
print(f"\nSaved Video: {output_video} ({fps} FPS)")

