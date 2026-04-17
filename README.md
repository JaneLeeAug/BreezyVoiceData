wget -P proj/MR_dataset/mtk53732 https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash proj/MR_dataset/mtk53732/Miniconda3-latest-Linux-x86_64.sh -b -p proj/MR_dataset/mtk53732/miniconda3

source proj/MR_dataset/mtk53732/miniconda3/etc/profile.d/conda.sh

conda --version

conda create -n bz python=3.10
conda activate bz


echo 'export PATH="$HOME/proj/MR_dataset/mtk53732/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

---
conda activate bz

python -m pip install -U pip wheel "setuptools<81"
python -m pip install --no-build-isolation openai-whisper==20231117


python -m pip install --no-build-isolation -r requirements.txt

---
time python batch_inference.py \
  --csv_file ../BreezyVoiceData/pairing_chunks/pairing_part_000.csv\
  --speaker_prompt_audio_folder ../BreezyVoiceData/speakerWav \
  --output_audio_folder ./SD 2>&1 | tee SD000_results.txt



source /proj/MR_dataset/mtk53732/miniconda3/etc/profile.d/conda.sh
