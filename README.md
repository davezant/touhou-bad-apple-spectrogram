<p align="center">
  <img src="https://media1.tenor.com/m/D6bM8ez99HkAAAAC/sakuya-izayoi-speen.gif" width="300" alt="Bad Apple GIF"/>
</p>

<h1 align="center">🍎 Bad Apple Stenography</h1>

<p align="center">
  <strong>Turning sound into shadowy chaos — Bad Apple in spectrogram form!</strong>
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python" alt="Python 3.10+"/></a>
  <a href="https://ffmpeg.org"><img src="https://img.shields.io/badge/ffmpeg-required-orange?style=flat-square" alt="FFmpeg"/></a>
</p>

---

## 🔹 What’s This?

**Bad Apple as a Spectrogram**  
Just that. Watch it run… if you dare.  


---
### ⚠️ System Requirements & Resource Warning

> **Please note:** Processing the full set of frames and generating spectrogram-based audio can be **resource-intensive**.

- **Memory:** Ensure sufficient RAM is available (recommended **16 GB or more**) to prevent performance issues or crashes.
- **Disk Space:** Temporary and output files may require **10–20 GB** of free disk space.
- **Processing Speed:** Running on an SSD is strongly recommended for faster read/write operations.
- **System Load:** Close unnecessary applications to avoid excessive system load during processing.

Failure to meet these requirements may result in incomplete processing, application errors, or corrupted output files.


---

## 🛠 Requirements

- Python 3.10+  
- [FFmpeg](https://ffmpeg.org/download.html)  
- Python packages:  
  `numpy`, `Pillow`, `scipy`, `matplotlib`, `pydub`, `tqdm`, `opencv-python`

---

## 🎬 How to Use

1. Download `ffmpeg.exe` and place it in the `binaries/` folder.  
2. Download the frame images from `https://github.com/Felixoofed/badapple-frames/`, unzip and place them in the `frames/` folder.  

```bash
# 1️⃣ Generate audio chunks from frames
python generate_audio.py

# 2️⃣ Convert audio back into spectrogram frames
python generate_video.py

# 3️⃣ Compress WAV into MP3 blocks
python generate_mp3_from_wav.py

# 4️⃣ Merge MP3 blocks into one MP3
python merge_mp3.py

# 5️⃣ Merge compressed MP3 with video
python release.py

# 6️⃣ Clean temporary files
python clean.py
