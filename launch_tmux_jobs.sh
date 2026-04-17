#!/usr/bin/env bash

set -euo pipefail

CONDA_SH="/proj/MR_dataset/mtk53732/miniconda3/etc/profile.d/conda.sh"
CONDA_ENV="bz"

CSV_DIR="../BreezyVoiceData/pairing_chunks"
AUDIO_DIR="../BreezyVoiceData/speakerWav"
OUTPUT_DIR="./SD"

mkdir -p "$OUTPUT_DIR"

for i in $(seq 0 99); do
    SESSION_NAME=$(printf "SD%03d" "$i")
    CSV_FILE=$(printf "%s/pairing_part_%03d.csv" "$CSV_DIR" "$i")
    LOG_FILE=$(printf "SD%03d_results.txt" "$i")

    # GPU 分配：每 13 個 job 一張 GPU
    GPU=$(( i / 13 ))

    # 最後保險，避免超過 GPU 7
    if [ "$GPU" -gt 7 ]; then
        GPU=7
    fi

    # 如果 session 已存在就跳過
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "[SKIP] tmux session $SESSION_NAME already exists"
        continue
    fi

    CMD=$(cat <<EOF
source "$CONDA_SH"
conda activate "$CONDA_ENV"
CUDA_VISIBLE_DEVICES=$GPU time python batch_inference.py \
  --csv_file "$CSV_FILE" \
  --speaker_prompt_audio_folder "$AUDIO_DIR" \
  --output_audio_folder "$OUTPUT_DIR" 2>&1 | tee "$LOG_FILE"
EOF
)

    tmux new-session -d -s "$SESSION_NAME" "bash -lc '$CMD'"

    echo "[OK] launched $SESSION_NAME on GPU $GPU -> $(basename "$CSV_FILE")"
done
