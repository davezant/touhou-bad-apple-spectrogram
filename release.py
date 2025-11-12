import os
import subprocess
from tqdm import tqdm

ffmpeg_path = r"./binaries/ffmpeg.exe"
video_file = "badapple_video.mp4"
audio_file = "badapple_audio.mp3"
output_file = "badapple_final_video.mp4"

if not os.path.exists(video_file):
    raise FileNotFoundError(f"Video not found: {video_file}")
if not os.path.exists(audio_file):
    raise FileNotFoundError(f"Audio not found: {audio_file}")

print("Replacing video audio with MP3...")

cmd = [
    ffmpeg_path,
    "-y",
    "-i", video_file,
    "-i", audio_file,
    "-c:v", "copy",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-shortest",
    output_file
]

print("Processing video with audio...")
with tqdm(total=1, desc="Merging video+MP3", ncols=80) as pbar:
    subprocess.run(cmd, check=True)
    pbar.update(1)

print(f"\nFinal file generated: {output_file}")
