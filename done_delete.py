import os
import pandas as pd
from tqdm import tqdm

# 1. 讀取 ./SD 裡的 wav 檔名
sd_folder = "./SD"
sd_names = set()

for f in os.listdir(sd_folder):
    if f.endswith(".wav"):
        sd_names.add(os.path.splitext(f)[0])  # SD000300424

print("Total SD wav files:", len(sd_names))


# 2. 處理 100 個 CSV
csv_dir = "../BreezyVoiceData/pairing_chunks"

for i in tqdm(range(100)):
    csv_path = f"{csv_dir}/pairing_part_{i:03d}.csv"

    df = pd.read_csv(csv_path)

    before = len(df)

    # 3. 刪掉對應列
    df = df[~df["output_audio_filename"].isin(sd_names)]

    after = len(df)

    # 4. 覆寫 CSV
    df.to_csv(csv_path, index=False)

    print(f"{csv_path}: removed {before-after}")
