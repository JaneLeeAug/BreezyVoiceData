import os
import soundfile as sf
from tqdm import tqdm

folder = "./SD"

# 先收集所有 wav 檔
wav_files = []
for root, dirs, files in os.walk(folder):
    for f in files:
        if f.endswith(".wav"):
            wav_files.append(os.path.join(root, f))

total_seconds = 0

for path in tqdm(wav_files, desc="Processing wav files"):
    info = sf.info(path)
    total_seconds += info.duration

print("Total seconds:", total_seconds)
print("Total hours:", total_seconds / 3600)
