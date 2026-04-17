(bz) gpu_mtk53732@colglx2002:~/BreezyVoice$ python - << 'PY'
import inspect
from g2pw import api
print(inspect.getsource(api.download_model))
print("="*80)
print(inspect.getsource(api.G2PWConverter.__init__))
PY
/proj/MR_dataset/mtk53732/miniconda3/envs/bz/lib/python3.10/site-packages/torch/cuda/__init__.py:56: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
Disabling PyTorch because PyTorch >= 2.4 is required but found 2.3.1+cu118
PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
2026-04-17 16:45:26.757232810 [W:onnxruntime:Default, device_discovery.cc:164 DiscoverDevicesForPlatform] GPU device discovery failed: device_discovery.cc:89 ReadFileContents Failed to open file: "/sys/class/drm/card0/device/vendor"
def download_model(model_dir):
    root = os.path.dirname(os.path.abspath(model_dir))

    r = requests.get(MODEL_URL, allow_redirects=True)
    zip_file = zipfile.ZipFile(BytesIO(r.content))
    zip_file.extractall(root)
    source_dir = os.path.join(root, zip_file.namelist()[0].split('/')[0])
    shutil.move(source_dir, model_dir)

================================================================================
    def __init__(self, model_dir='G2PWModel/', style='bopomofo', model_source=None, num_workers=None, batch_size=None,
                 turnoff_tqdm=True, enable_non_tradional_chinese=False):
        if not os.path.exists(os.path.join(model_dir, 'version')):
            download_model(model_dir)

        sess_options = onnxruntime.SessionOptions()
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
        sess_options.intra_op_num_threads = 2
        self.session_g2pw =  onnxruntime.InferenceSession(os.path.join(model_dir, 'g2pw.onnx'), sess_options=sess_options)
        
        self.config = load_config(os.path.join(model_dir, 'config.py'), use_default=True)

        self.num_workers = num_workers if num_workers else self.config.num_workers
        self.batch_size = batch_size if batch_size else self.config.batch_size
        self.model_source = model_source if model_source else self.config.model_source
        self.turnoff_tqdm = turnoff_tqdm

        self.tokenizer = BertTokenizer.from_pretrained(self.model_source)

        polyphonic_chars_path = os.path.join(model_dir, 'POLYPHONIC_CHARS.txt')
        monophonic_chars_path = os.path.join(model_dir, 'MONOPHONIC_CHARS.txt')
        self.polyphonic_chars = [line.split('\t') for line in open(polyphonic_chars_path).read().strip().split('\n')]
        self.monophonic_chars = [line.split('\t') for line in open(monophonic_chars_path).read().strip().split('\n')]
        self.labels, self.char2phonemes = get_char_phoneme_labels(self.polyphonic_chars) if self.config.use_char_phoneme else get_phoneme_labels(self.polyphonic_chars)

        self.chars = sorted(list(self.char2phonemes.keys()))
        self.pos_tags = TextDataset.POS_TAGS

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'bopomofo_to_pinyin_wo_tune_dict.json'), 'r') as fr:
            self.bopomofo_convert_dict = json.load(fr)
        self.style_convert_func = {
            'bopomofo': lambda x: x,
            'pinyin': self._convert_bopomofo_to_pinyin,
        }[style]

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'char_bopomofo_dict.json'), 'r') as fr:
            self.char_bopomofo_dict = json.load(fr)

        self.enable_non_tradional_chinese = enable_non_tradional_chinese
        if self.enable_non_tradional_chinese:
            self.s2t_dict = {}
            for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    'bert-base-chinese_s2t_dict.txt'), 'r').read().strip().split('\n'):
                s_char, t_char = line.split('\t')
                self.s2t_dict[s_char] = t_char
