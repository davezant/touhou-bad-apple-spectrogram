import os
from pydub import AudioSegment
from tqdm import tqdm

wav_folder = "cache/"
mp3_bitrate = "64k"
num_blocks = 5

AudioSegment.converter = os.path.join("./binaries/ffmpeg.exe")

wav_files = sorted([f for f in os.listdir(wav_folder) if f.startswith("badapple_step_") and f.endswith(".wav")])
if not wav_files:
    raise FileNotFoundError("No WAV files found to process.")

total_files = len(wav_files)
files_per_block = total_files // num_blocks

mp3_intermediarios = []

for block_idx in range(num_blocks):
    start = block_idx * files_per_block
    end = start + files_per_block if block_idx < num_blocks - 1 else total_files
    block_files = wav_files[start:end]

    combined_block = AudioSegment.silent(duration=0)
    
    print(f"\nProcessing block {block_idx+1}/{num_blocks} ({len(block_files)} WAVs)...")
    
    for wav_file in tqdm(block_files, desc="Concatenating WAVs in block", ncols=80):
        audio = AudioSegment.from_wav(os.path.join(wav_folder, wav_file))
        combined_block += audio
    
    mp3_path = f"cache/temp_block_{block_idx+1}.mp3"
    combined_block.export(mp3_path, format="mp3", bitrate=mp3_bitrate)
    mp3_intermediarios.append(mp3_path)

print("MP3 files created.")
