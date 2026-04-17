(bz) gpu_mtk53732@colglx2002:~/BreezyVoice$ CUDA_VISIBLE_DEVICES=0 time python batch_inference.py \
--csv_file ../BreezyVoiceData/pairing_chunks/pairing_part_000.csv \
--speaker_prompt_audio_folder ../BreezyVoiceData/speakerWav \
--output_audio_folder ./SD 2>&1 | tee SD000_results.txt
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/cuda/__init__.py:56: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
Disabling PyTorch because PyTorch >= 2.4 is required but found 2.3.1+cu118
PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
2026-04-17 15:19:16.931434821 [W:onnxruntime:Default, device_discovery.cc:164 DiscoverDevicesForPlatform] GPU device discovery failed: device_discovery.cc:89 ReadFileContents Failed to open file: "/sys/class/drm/card0/device/vendor"
Fetching 154 files: 100%|██████████| 154/154 [00:00<00:00, 2791.92it/s]
model /proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d
Traceback (most recent call last):
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 76, in <module>
    main()
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 62, in main
    cosyvoice = CustomCosyVoice(args.model_path)
  File "/proj/gpu_mtk53732/BreezyVoice/single_inference.py", line 212, in __init__
    configs = load_hyperpyyaml(f)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/hyperpyyaml/core.py", line 188, in load_hyperpyyaml
    hparams = yaml.load(yaml_stream, Loader=loader)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/yaml/__init__.py", line 81, in load
    return loader.get_single_data()
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/ruamel/yaml/constructor.py", line 117, in get_single_data
    node = self.composer.get_single_node()
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/ruamel/yaml/composer.py", line 77, in get_single_node
    document = self.compose_document()
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/ruamel/yaml/composer.py", line 100, in compose_document
    node = self.compose_node(None, None)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/ruamel/yaml/composer.py", line 121, in compose_node
    if self.loader.max_depth and self.depth > self.loader.max_depth:
AttributeError: 'Loader' object has no attribute 'max_depth'
Command exited with non-zero status 1
8.82user 7.49system 0:12.27elapsed 133%CPU (0avgtext+0avgdata 743312maxresident)k
0inputs+16outputs (0major+282970minor)pagefaults 0swaps
