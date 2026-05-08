import os
import time
import subprocess
import argparse
import pandas as pd
from datasets import Dataset
from single_inference import single_inference, CustomCosyVoice
from g2pw import G2PWConverter
from transformers import BertTokenizer

_real_from_pretrained = BertTokenizer.from_pretrained

def _patched_from_pretrained(model_name_or_path, *args, **kwargs):
    if model_name_or_path == "bert-base-chinese":
        print("[Patch] Redirect bert-base-chinese to local path")
        model_name_or_path = "/proj/gpu_d_09023_MR_dataset_ARCHIVE/mtk53732/pretrained_models/bert-base-chinese"
    return _real_from_pretrained(model_name_or_path, *args, **kwargs)

BertTokenizer.from_pretrained = _patched_from_pretrained


def process_batch(csv_file, speaker_prompt_audio_folder, output_audio_folder, model):
    # Load CSV with pandas
    data = pd.read_csv(csv_file)

    # Transform pandas DataFrame to HuggingFace Dataset
    dataset = Dataset.from_pandas(data)
    dataset = dataset.shuffle(seed = int(time.time()*1000))

    cosyvoice, bopomofo_converter = model

    def gen_audio(row):
        speaker_prompt_audio_path = os.path.join(
            speaker_prompt_audio_folder,
            f"{row['speaker_prompt_audio_filename']}.wav"
        )
        speaker_prompt_text_transcription = row['speaker_prompt_text_transcription']
        content_to_synthesize = row['content_to_synthesize']
        output_audio_path = os.path.join(
            output_audio_folder,
            f"{row['output_audio_filename']}.wav"
        )
    
        if not os.path.exists(speaker_prompt_audio_path):
            print(f"[SKIP] Speaker prompt file does not exist: {speaker_prompt_audio_path}")
            return row
    
        if os.path.exists(output_audio_path):
            print(f"[SKIP] Output already exists: {output_audio_path}")
            return row
    
        try:
            success = single_inference(
                speaker_prompt_audio_path,
                content_to_synthesize,
                output_audio_path,
                cosyvoice,
                bopomofo_converter,
                speaker_prompt_text_transcription,
            )
    
            if success is False:
                print(f"[SKIP] single_inference returned False: {output_audio_path}")
            else:
                print(f"[DONE] Generated: {output_audio_path}")
    
        except Exception as e:
            print("=" * 80)
            print("[FAILED] single_inference crashed")
            print("speaker_prompt_audio_path:", repr(speaker_prompt_audio_path))
            print("speaker_prompt_text_transcription:", repr(speaker_prompt_text_transcription))
            print("content_to_synthesize:", repr(content_to_synthesize))
            print("output_audio_path:", repr(output_audio_path))
            print("error:", repr(e))
            print("=" * 80)
    
        return row

def main():
    parser = argparse.ArgumentParser(description="Batch process audio generation.")
    parser.add_argument("--csv_file", required=True, help="Path to the CSV file containing input data.")
    parser.add_argument("--speaker_prompt_audio_folder", required=True, help="Path to the folder containing speaker prompt audio files.")
    parser.add_argument("--output_audio_folder", required=True, help="Path to the folder where results will be stored.")
    parser.add_argument("--model_path", type=str, required=False, default = "MediaTek-Research/BreezyVoice-300M",help="Specifies the model used for speech synthesis.")

    args = parser.parse_args()

    cosyvoice = CustomCosyVoice(args.model_path)
    # 20260506 
    bopomofo_converter = G2PWConverter(
        model_dir = "../g2pw"
    )

    os.makedirs(args.output_audio_folder, exist_ok=True)

    process_batch(
        csv_file=args.csv_file,
        speaker_prompt_audio_folder=args.speaker_prompt_audio_folder,
        output_audio_folder=args.output_audio_folder,
        model = (cosyvoice, bopomofo_converter),

    )

if __name__ == "__main__":
    main()

