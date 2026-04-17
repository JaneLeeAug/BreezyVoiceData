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
