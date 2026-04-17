Create TikTokenTokenizer with config_path=/proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d/CosyVoice-ttsfrd/resource/tokenizer/tiktoken.toml config_name=multilingual rank_path=/proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d/CosyVoice-ttsfrd/resource/tokenizer/multilingual.tiktoken
failed to do test: failed to open file: /proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d/CosyVoice-ttsfrd/resource/tokenizer/tiktoken.toml
load tokenizer failed
break model index not valid
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
WARNING:huggingface_hub.utils._http:Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
tokenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 49.0/49.0 [00:00<00:00, 96.0kB/s]
vocab.txt: 110kB [00:00, 2.24MB/s]
tokenizer.json: 269kB [00:00, 1.39MB/s]
Parameter 'function'=<function process_batch.<locals>.gen_audio at 0x77d8f2906dd0> of the transform datasets.arrow_dataset.Dataset._map_single couldn't be hashed properly, a random hash was used instead. Make sure your transforms and parameters are serializable with pickle or dill for the dataset fingerprinting and caching to work. If you reuse this transform, the caching mechanism will consider it to be different from the previous calls and recompute everything. This warning is only shown once. Subsequent hashing failures won't be shown.
WARNING:datasets.fingerprint:Parameter 'function'=<function process_batch.<locals>.gen_audio at 0x77d8f2906dd0> of the transform datasets.arrow_dataset.Dataset._map_single couldn't be hashed properly, a random hash was used instead. Make sure your transforms and parameters are serializable with pickle or dill for the dataset fingerprinting and caching to work. If you reuse this transform, the caching mechanism will consider it to be different from the previous calls and recompute everything. This warning is only shown once. Subsequent hashing failures won't be shown.
Map (num_proc=1):   0%|                                                                                                                   | 0/10728 [00:00<?, ? examples/s]
Traceback (most recent call last):
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 76, in <module>
    main()
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 67, in main
    process_batch(
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 51, in process_batch
    dataset = dataset.map(gen_audio, num_proc = 1)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/datasets/arrow_dataset.py", line 574, in wrapper
    out: Union["Dataset", "DatasetDict"] = func(self, *args, **kwargs)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/datasets/arrow_dataset.py", line 3623, in map
    for rank, done, content in iflatmap_unordered(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/datasets/utils/py_utils.py", line 624, in iflatmap_unordered
    [async_result.get(timeout=0.05) for async_result in async_results]
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/datasets/utils/py_utils.py", line 624, in <listcomp>
    [async_result.get(timeout=0.05) for async_result in async_results]
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/multiprocess/pool.py", line 774, in get
    raise self._value
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/multiprocess/pool.py", line 540, in _handle_tasks
    put(task)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/multiprocess/connection.py", line 209, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/multiprocess/reduction.py", line 54, in dumps
    cls(buf, protocol, *args, **kwds).dump(obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 429, in dump
    StockPickler.dump(self, obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 487, in dump
    self.save(obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 902, in save_tuple
    save(element)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 887, in save_tuple
    save(element)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 1266, in save_module_dict
    StockPickler.save_dict(pickler, obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 972, in save_dict
    self._batch_setitems(obj.items())
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 998, in _batch_setitems
    save(v)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 2046, in save_function
    _save_with_postproc(pickler, (_create_function, (
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 1157, in _save_with_postproc
    pickler.save_reduce(*reduction)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 692, in save_reduce
    save(args)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 887, in save_tuple
    save(element)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 603, in save
    self.save_reduce(obj=obj, *rv)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 717, in save_reduce
    save(state)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 1266, in save_module_dict
    StockPickler.save_dict(pickler, obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 972, in save_dict
    self._batch_setitems(obj.items())
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 998, in _batch_setitems
    save(v)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 603, in save
    self.save_reduce(obj=obj, *rv)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 717, in save_reduce
    save(state)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 1266, in save_module_dict
    StockPickler.save_dict(pickler, obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 972, in save_dict
    self._batch_setitems(obj.items())
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 998, in _batch_setitems
    save(v)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 603, in save
    self.save_reduce(obj=obj, *rv)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 717, in save_reduce
    save(state)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 1266, in save_module_dict
    StockPickler.save_dict(pickler, obj)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 972, in save_dict
    self._batch_setitems(obj.items())
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 998, in _batch_setitems
    save(v)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/dill/_dill.py", line 423, in save
    StockPickler.save(self, obj, save_persistent_id)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/pickle.py", line 578, in save
    rv = reduce(self.proto)
TypeError: cannot pickle 'onnxruntime.capi.onnxruntime_pybind11_state.InferenceSession' object
