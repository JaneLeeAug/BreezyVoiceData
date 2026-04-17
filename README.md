wget -P proj/MR_dataset/mtk53732 https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash proj/MR_dataset/mtk53732/Miniconda3-latest-Linux-x86_64.sh -b -p proj/MR_dataset/mtk53732/miniconda3

source proj/MR_dataset/mtk53732/miniconda3/etc/profile.d/conda.sh

conda --version

conda create -n bz python=3.10
conda activate bz


echo 'export PATH="$HOME/proj/MR_dataset/mtk53732/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

---
Collecting openai-whisper==20231117 (from -r requirements.txt (line 18))
  Downloading openai-whisper-20231117.tar.gz (798 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 798.6/798.6 kB 4.9 MB/s  0:00:00
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [17 lines of output]
      Traceback (most recent call last):
        File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 389, in <module>
          main()
        File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 373, in main
          json_out["return_val"] = hook(**hook_input["kwargs"])
        File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 143, in get_requires_for_build_wheel
          return hook(config_settings)
        File "/tmp/pip-build-env-las2gqpc/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 333, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
        File "/tmp/pip-build-env-las2gqpc/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 301, in _get_build_requires
          self.run_setup()
        File "/tmp/pip-build-env-las2gqpc/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 520, in run_setup
          super().run_setup(setup_script=setup_script)
        File "/tmp/pip-build-env-las2gqpc/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 317, in run_setup
          exec(code, locals())
        File "<string>", line 5, in <module>
      ModuleNotFoundError: No module named 'pkg_resources'
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'openai-whisper' when getting requirements to build wheel
