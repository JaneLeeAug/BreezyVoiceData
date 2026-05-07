import csv
import os
from tqdm import tqdm

INPUT_FILE = "pairing_table.csv"
OUTPUT_DIR = "pairing_chunks"
NUM_PARTS = 100

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 先算總行數（扣掉 header）
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    total_rows = sum(1 for _ in f) - 1

rows_per_part = total_rows // NUM_PARTS
extra = total_rows % NUM_PARTS

print(f"Total rows: {total_rows}")
print(f"Rows per part: {rows_per_part}")
print(f"Extra rows: {extra}")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)

    part = 0
    row_count = 0
    target_rows = rows_per_part + (1 if part < extra else 0)

    outfile = open(f"{OUTPUT_DIR}/pairing_part_{part:03d}.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(outfile)
    writer.writerow(header)

    for row in tqdm(reader, total=total_rows):
        writer.writerow(row)
        row_count += 1

        if row_count >= target_rows:
            outfile.close()
            part += 1

            if part >= NUM_PARTS:
                break

            row_count = 0
            target_rows = rows_per_part + (1 if part < extra else 0)

            outfile = open(f"{OUTPUT_DIR}/pairing_part_{part:03d}.csv", "w", newline="", encoding="utf-8")
            writer = csv.writer(outfile)
            writer.writerow(header)

    outfile.close()
