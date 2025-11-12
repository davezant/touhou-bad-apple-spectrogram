import os
from tqdm import tqdm

folder = "."
wav_pattern = "cache/badapple_step_"
mp3_pattern = "cache/temp_block_"

files_to_delete = []

files_to_delete.extend([f for f in os.listdir(folder)
                        if f.startswith(wav_pattern) and f.endswith(".wav")])

files_to_delete.extend([f for f in os.listdir(folder)
                        if f.startswith(mp3_pattern) and f.endswith(".mp3")])

if not files_to_delete:
    print("No files found to delete.")
else:
    print(f"{len(files_to_delete)} files found to delete.")

for f in tqdm(files_to_delete, desc="Deleting files", ncols=80):
    try:
        os.remove(os.path.join(folder, f))
    except Exception as e:
        print(f"Error deleting {f}: {e}")

print("Temporary files removed successfully.")
