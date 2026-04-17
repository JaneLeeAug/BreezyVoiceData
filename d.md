python - << 'PY'
import inspect
from g2pw import api
print(inspect.getsource(api.download_model))
print("="*80)
print(inspect.getsource(api.G2PWConverter.__init__))
PY
