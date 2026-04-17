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
CUDA_VISIBLE_DEVICES=0 time python batch_inference.py \
--csv_file ../BreezyVoiceData/pairing_chunks/pairing_part_000.csv \
--speaker_prompt_audio_folder ../BreezyVoiceData/speakerWav \
--output_audio_folder ./SD 2>&1 | tee SD000_results.txt



source /proj/MR_dataset/mtk53732/miniconda3/etc/profile.d/conda.sh

---
(bz) gpu_mtk53732@colglx2002:~/BreezyVoice$ # python single_inference.py --text_to_speech [text to be converted into audio] --text_prompt [the prompt of that audio file] --audio_path [reference audio file]
python single_inference.py --content_to_synthesize "今天天氣真好" --speaker_prompt_text_transcription "在密碼學中，加密是將明文資訊改 
變為難以讀取的密文內容，使之不可讀的方法。只有擁有解密方法的對象,經由解密過程才能將密文還原為正常可讀的內容。" --speaker_prompt_audio_path "./data/example.wav"
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/cuda/__init__.py:56: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
Traceback (most recent call last):
  File "/proj/gpu_mtk53732/BreezyVoice/single_inference.py", line 10, in <module>
    import torchaudio
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torchaudio/__init__.py", line 2, in <module>
    from . import _extension  # noqa  # usort: skip
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torchaudio/_extension/__init__.py", line 38, in <module>
    _load_lib("libtorchaudio")
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torchaudio/_extension/utils.py", line 60, in _load_lib
    torch.ops.load_library(path)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/_ops.py", line 1032, in load_library
    ctypes.CDLL(path)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/ctypes/__init__.py", line 374, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libcudart.so.11.0: cannot open shared object file: No such file or directory





export PYTHONNOUSERSITE=1
