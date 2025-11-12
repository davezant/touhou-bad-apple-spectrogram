import os
import subprocess
from tqdm import tqdm
import re

mp3_folder = "cache/"
output_mp3 = "badapple_audio.mp3"
target_total_sec = 3*60 + 39
ffmpeg_path = r"./binaries/ffmpeg.exe"

def atempo_chain(speed):
    filters = []
    while speed > 2.0:
        filters.append("atempo=2.0")
        speed /= 2.0
    while speed < 0.5:
        filters.append("atempo=0.5")
        speed /= 0.5
    filters.append(f"atempo={speed:.6f}")
    return ",".join(filters)

mp3_files = sorted([f for f in os.listdir(mp3_folder) 
                    if f.startswith("temp_block_") and f.endswith(".mp3")])
if not mp3_files:
    raise FileNotFoundError("No intermediate MP3 files found.")

durations = []
print("Calculating block durations...")
for mp3_file in tqdm(mp3_files, ncols=80):
    result = subprocess.run([ffmpeg_path, "-i", mp3_file],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if m:
        h, m_, s = m.groups()
        dur_sec = int(h)*3600 + int(m_)*60 + float(s)
        durations.append(dur_sec)
    else:
        raise RuntimeError(f"Could not get duration of {mp3_file}")

total_original_sec = sum(durations)
print(f"Total original duration: {total_original_sec:.2f}s")

temp_adjusted = []
print("Speeding up blocks to fit final duration...")
for idx, mp3_file in enumerate(tqdm(mp3_files, ncols=80)):
    block_fraction = durations[idx] / total_original_sec
    target_block_sec = target_total_sec * block_fraction
    speed = durations[idx] / target_block_sec
    filter_str = atempo_chain(speed)
    temp_file = f"cache/temp_adj_{idx+1}.mp3"
    
    subprocess.run([
        ffmpeg_path, "-y", "-i", mp3_file,
        "-filter:a", filter_str,
        "-b:a", "64k",
        temp_file
    ], check=True)
    
    temp_adjusted.append(temp_file)

concat_list = "concat_list.txt"
with open(concat_list, "w") as f:
    for t in temp_adjusted:
        f.write(f"file '{os.path.abspath(t)}'\n")

subprocess.run([
    ffmpeg_path, "-y", "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    output_mp3
], check=True)

print(f"\nFinal MP3 generated: {output_mp3}")

for t in temp_adjusted + [concat_list]:
    os.remove(t)

print("Temporary files removed.")
