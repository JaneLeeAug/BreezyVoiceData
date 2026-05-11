#!/bin/bash

TMP_INIT=$(mktemp /tmp/init1.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)

if [ -f ~/.bashrc ]; then
    echo "source ~/.bashrc" >> "$TMP_INIT"
fi

echo "set -m" >> "$TMP_INIT"

echo '
cd /proj/gpu_d_09023/mtk53732/BreezyVoice

start_part=48

for gpu in {0..7}
do
    for local_idx in {0..1}
    do
        part=$((start_part + gpu * 6 + local_idx))
        part_str=$(printf "%03d" "$part")

        CUDA_VISIBLE_DEVICES=0 python batch_inference.py \
            --model_path /proj/gpu_d_09023_MR_dataset_ARCHIVE/mtk53732/pretrained_models/BreezyVoice-300M/ \
            --csv_file /proj/gpu_d_09023_MR_dataset_ARCHIVE/mtk53732/pairingTable/pairing_part_${part_str}.csv \
            --speaker_prompt_audio_folder /proj/gpu_d_09023_MR_dataset_ARCHIVE/mtk53732/speakerWav/ \
            --output_audio_folder /proj/gpu_d_09023/mtk53732/SD \
            > SD_B200_${part_str}.txt 2>&1 &
    done
done
' >> "$TMP_INIT"

exec bash --rcfile "$TMP_INIT" -i
