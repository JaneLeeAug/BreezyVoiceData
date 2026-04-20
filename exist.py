import os
import pandas as pd

folder = "./SD"   # 你的資料夾
output_csv = "exist.csv"

files = []

for f in os.listdir(folder):
    if f.endswith(".wav"):
        name = os.path.splitext(f)[0]  # 移除 .wav
        files.append(name)

df = pd.DataFrame({"exist": files})
df.to_csv(output_csv, index=False)

print(f"Saved {len(files)} entries to {output_csv}")
