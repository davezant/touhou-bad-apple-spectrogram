import os
import numpy as np
from PIL import Image
from scipy.io import wavfile
import matplotlib.pyplot as plt
from tqdm import tqdm

frames_folder = "frames"
frames_folder_out = "audio_frames"
os.makedirs(frames_folder_out, exist_ok=True)

h, w = 480, 360
fs = 24000
frames_per_step = 50
total_frames = 6572
num_steps = (total_frames + frames_per_step - 1) // frames_per_step

frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith(".jpg") or f.endswith(".png")])
if len(frame_files) != total_frames:
    print(f"Warning: number of frames found ({len(frame_files)}) differs from {total_frames}")
total_frames = len(frame_files)

frame_counter = 0

for step in range(num_steps):
    start_frame = step * frames_per_step
    end_frame = min(start_frame + frames_per_step, total_frames)
    batch_files = frame_files[start_frame:end_frame]

    print(f"\n--- Step {step+1}/{num_steps}: frames {start_frame} to {end_frame-1} ---")

    all_audio = []

    for idx, frame_file in enumerate(tqdm(batch_files, desc=f"Processing frames step {step+1}", ncols=80)):
        frame_path = os.path.join(frames_folder, frame_file)

        img = Image.open(frame_path).resize((w, h))
        data = np.array(img, dtype='float')

        if data.ndim == 3:
            data = 0.2989*data[:,:,0] + 0.5870*data[:,:,1] + 0.1140*data[:,:,2]
        data = data / np.max(data)
        data = np.flip(data, axis=0)

        phdata = np.exp(1j * 23 * np.random.randn(h, w))
        data_complex = data * phdata

        d1 = np.conjugate(np.flip(data_complex, axis=1)[:, :-1])
        data_full = np.concatenate((d1, data_complex), axis=1)
        data_full = np.fft.ifftshift(data_full, axes=1)

        data_ifft = np.fft.ifft(data_full, axis=1)
        data_flat = np.real(data_ifft.flatten())
        data_flat /= np.max(np.abs(data_flat))

        data_int16 = (data_flat * 32767).astype(np.int16)
        data_stereo = np.array([data_int16, data_int16]).T

        all_audio.append(data_stereo)
        frame_counter += 1

    final_audio = np.concatenate(all_audio, axis=0)

    output_wav = f"cache/badapple_step_{step+1}.wav"
    wavfile.write(output_wav, int(fs), final_audio)
    print(f"WAV generated: {output_wav} ({final_audio.shape[0]/fs:.1f}s)")

    if final_audio.ndim == 2:
        audio_mono = final_audio.mean(axis=1)
    else:
        audio_mono = final_audio

    samples_per_frame = len(audio_mono) // len(batch_files)
    frames_audio = [audio_mono[i*samples_per_frame:(i+1)*samples_per_frame] for i in range(len(batch_files))]

    for idx, frame_data in enumerate(tqdm(frames_audio, desc=f"Generating spectrograms step {step+1}", ncols=80)):
        plt.figure(figsize=(w/100, h/100), dpi=100, facecolor='black')
        plt.specgram(frame_data, NFFT=1024, Fs=fs, noverlap=512, cmap='inferno', scale='dB')
        plt.axis('off')
        plt.tight_layout(pad=0)

        frame_out_path = os.path.join(frames_folder_out, f"frame_{start_frame + idx:04d}.png")
        plt.savefig(frame_out_path, dpi=100, bbox_inches='tight', pad_inches=0, facecolor='black')
        plt.close()

print("\nProcessing complete: all frames and WAVs generated in steps of 50 frames")
