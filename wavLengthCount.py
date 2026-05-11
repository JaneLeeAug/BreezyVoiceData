# waveLenthCount.py

import os
import pandas as pd
import soundfile as sf
from tqdm import tqdm

CSV_PATH = "./pairing_table.csv"
WAV_FOLDER = "./SD"

DURATION_COL = "duration(s)"
OUTPUT_COL = "output_audio_filename"

# =========================
# Read CSV
# =========================
df = pd.read_csv(CSV_PATH)

# 如果沒有 duration(s) 欄位就新增
if DURATION_COL not in df.columns:
    df[DURATION_COL] = ""

total_seconds = 0
updated_count = 0
missing_count = 0
bad_wav_count = 0

# =========================
# Process each row
# =========================
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):

    duration_value = row[DURATION_COL]

    # -------------------------------------------------
    # Case 1:
    # 已經有數字 -> 直接累加
    # -------------------------------------------------
    if pd.notna(duration_value) and str(duration_value).strip() != "":
        try:
            total_seconds += float(duration_value)
        except Exception:
            pass
        continue

    # -------------------------------------------------
    # Case 2:
    # duration(s) 為空 -> 去 SD 找 wav 計算
    # -------------------------------------------------
    wav_name = f"{row[OUTPUT_COL]}.wav"
    wav_path = os.path.join(WAV_FOLDER, wav_name)

    if not os.path.exists(wav_path):
        missing_count += 1
        continue

    try:
        info = sf.info(wav_path)
        duration = info.duration

        # 寫回 CSV
        df.at[idx, DURATION_COL] = duration

        # 累加
        total_seconds += duration
        updated_count += 1

    except Exception:
        print(f"\n[Bad wav] {wav_path}")
        bad_wav_count += 1

# =========================
# Save CSV
# =========================
df.to_csv(CSV_PATH, index=False)

# =========================
# Summary
# =========================
print("\n========== Summary ==========")
print("Updated empty duration rows:", updated_count)
print("Missing wav files:", missing_count)
print("Bad wav files:", bad_wav_count)

print("\nTotal seconds:", total_seconds)
print("Total hours:", total_seconds / 3600)
