wget -P proj/MR_dataset https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash proj/MR_dataset/Miniconda3-latest-Linux-x86_64.sh -b -p proj/MR_dataset/miniconda3

source proj/MR_dataset/miniconda3/etc/profile.d/conda.sh

conda --version

conda create -n bz python=3.10
conda activate bz


---

echo 'export PATH="$HOME/proj/MR_dataset/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
