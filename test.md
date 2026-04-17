pip uninstall -y hyperpyyaml ruamel.yaml ruamel.yaml.clib
pip install \
  hyperpyyaml==1.2.2 \
  ruamel-yaml==0.17.40 \
  ruamel-yaml-clib==0.2.15


  PYTHONNOUSERSITE=1 CUDA_VISIBLE_DEVICES=0 python batch_inference.py \
  --csv_file ../BreezyVoiceData/pairing_chunks/pairing_part_000.csv \
  --speaker_prompt_audio_folder ../BreezyVoiceData/speakerWav \
  --output_audio_folder ./SD
