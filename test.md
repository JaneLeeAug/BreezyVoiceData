(bz) gpu_mtk53732@colglx2002:~/BreezyVoice$ CUDA_VISIBLE_DEVICES=0 python batch_inference.py \
  --csv_file ../BreezyVoiceData/pairing_chunks/pairing_part_000.csv \
  --speaker_prompt_audio_folder ../BreezyVoiceData/speakerWav \
  --output_audio_folder ./SD
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/cuda/__init__.py:56: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
Disabling PyTorch because PyTorch >= 2.4 is required but found 2.3.1+cu118
PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
2026-04-17 15:24:52.401086231 [W:onnxruntime:Default, device_discovery.cc:164 DiscoverDevicesForPlatform] GPU device discovery failed: device_discovery.cc:89 ReadFileContents Failed to open file: "/sys/class/drm/card0/device/vendor"
Fetching 154 files: 100%|█████████████████████████████████████████████████████████████████████████| 154/154 [00:00<00:00, 2315.99it/s]
Download complete: : 0.00B [00:00, ?B/s]              model /proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/_jit_internal.py:739: FutureWarning: ignore(True) has been deprecated. TorchScript will now drop the function call on compilation. Use torch.jit.unused now. {}
  warnings.warn(
Download complete: : 0.00B [00:04, ?B/s]
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/lightning/fabric/__init__.py:41: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/diffusers/models/lora.py:393: FutureWarning: `LoRACompatibleLinear` is deprecated and will be removed in version 1.0.0. Use of `LoRACompatibleLinear` is deprecated. Please switch to PEFT backend by installing PEFT: `pip install peft`.
  deprecate("LoRACompatibleLinear", "1.0.0", deprecation_message)
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/nn/utils/weight_norm.py:28: UserWarning: torch.nn.utils.weight_norm is deprecated in favor of torch.nn.utils.parametrizations.weight_norm.
  warnings.warn("torch.nn.utils.weight_norm is deprecated in favor of torch.nn.utils.parametrizations.weight_norm.")
/proj/gpu_mtk53732/BreezyVoice/cosyvoice/dataset/processor.py:24: UserWarning: torchaudio._backend.set_audio_backend has been deprecated. With dispatcher enabled, this function is no-op. You can remove the function call.
  torchaudio.set_audio_backend('soundfile')
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/onnxruntime/capi/onnxruntime_inference_collection.py:123: UserWarning: Specified provider 'CUDAExecutionProvider' is not in available provider names.Available providers: 'AzureExecutionProvider, CPUExecutionProvider'
  warnings.warn(
load leagacy transf breakmodel
load leagacy transf breakmodel
text.cc: festival_Text_init
open voice lang map failed
set used by tts frd
Create TikTokenTokenizer with config_path=/proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d/CosyVoice-ttsfrd/resource/tokenizer/tiktoken.toml config_name=multilingual rank_path=/proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d/CosyVoice-ttsfrd/resource/tokenizer/multilingual.tiktoken
failed to do test: failed to open file: /proj/gpu_mtk53732/.cache/huggingface/hub/models--MediaTek-Research--BreezyVoice-300M/snapshots/e33b502e0ac21c16b0ee0d00df66ac3fa737393d/CosyVoice-ttsfrd/resource/tokenizer/tiktoken.toml
load tokenizer failed
break model index not valid
Traceback (most recent call last):
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connectionpool.py", line 464, in _make_request
    self._validate_conn(conn)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connectionpool.py", line 1093, in _validate_conn
    conn.connect()
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connection.py", line 796, in connect
    sock_and_verified = _ssl_wrap_socket_and_match_hostname(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connection.py", line 975, in _ssl_wrap_socket_and_match_hostname
    ssl_sock = ssl_wrap_socket(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/util/ssl_.py", line 483, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/util/ssl_.py", line 527, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/ssl.py", line 513, in wrap_socket
    return self.sslsocket_class._create(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/ssl.py", line 1104, in _create
    self.do_handshake()
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/ssl.py", line 1375, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1017)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connectionpool.py", line 787, in urlopen
    response = self._make_request(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connectionpool.py", line 488, in _make_request
    raise new_e
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1017)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/requests/adapters.py", line 645, in send
    resp = conn.urlopen(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/connectionpool.py", line 841, in urlopen
    retries = retries.increment(
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/urllib3/util/retry.py", line 535, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='storage.googleapis.com', port=443): Max retries exceeded with url: /esun-ai/g2pW/G2PWModel-v2-onnx.zip (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1017)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 76, in <module>
    main()
  File "/proj/gpu_mtk53732/BreezyVoice/batch_inference.py", line 63, in main
    bopomofo_converter = G2PWConverter()
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/g2pw/api.py", line 64, in __init__
    download_model(model_dir)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/g2pw/api.py", line 53, in download_model
    r = requests.get(MODEL_URL, allow_redirects=True)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/requests/api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/requests/sessions.py", line 592, in request
    resp = self.send(prep, **send_kwargs)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/requests/sessions.py", line 706, in send
    r = adapter.send(request, **kwargs)
  File "/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/requests/adapters.py", line 676, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='storage.googleapis.com', port=443): Max retries exceeded with url: /esun-ai/g2pW/G2PWModel-v2-onnx.zip (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1017)')))
