import os
import soundfile as sf
from tqdm import tqdm

folder = "./SD"

wav_files = []
for root, dirs, files in os.walk(folder):
    for f in files:
        if f.lower().endswith(".wav"):
            wav_files.append(os.path.join(root, f))

total_seconds = 0
deleted = 0

for path in tqdm(wav_files, desc="Processing wav files"):
    try:
        info = sf.info(path)
        total_seconds += info.duration
    except Exception:
        print(f"\n[Delete bad wav] {path}")
        try:
            os.remove(path)
            deleted += 1
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

print("\nSummary")
print("Total wav files:", len(wav_files))
print("Deleted bad wav files:", deleted)
print("Total seconds:", total_seconds)
print("Total hours:", total_seconds / 3600)
