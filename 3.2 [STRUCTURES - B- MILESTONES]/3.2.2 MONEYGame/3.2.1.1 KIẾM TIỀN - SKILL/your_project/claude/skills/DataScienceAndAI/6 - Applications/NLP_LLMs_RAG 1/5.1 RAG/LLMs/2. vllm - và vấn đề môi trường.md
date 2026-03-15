```
Traceback (most recent call last):

  File "/home/ubuntu/.local/bin/vllm", line 3, in <module>

    from vllm.scripts import main

  File "/home/ubuntu/.local/lib/python3.11/site-packages/vllm/__init__.py", line 3, in <module>

    from vllm.engine.arg_utils import AsyncEngineArgs, EngineArgs

  File "/home/ubuntu/.local/lib/python3.11/site-packages/vllm/engine/arg_utils.py", line 8, in <module>

    import torch

  File "/home/ubuntu/.local/lib/python3.11/site-packages/torch/__init__.py", line 409, in <module>

    from torch._C import *  # noqa: F403

    ^^^^^^^^^^^^^^^^^^^^^^

ImportError: /home/ubuntu/.local/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so: undefined symbol: cuptiActivityEnableDriverApi, version libcupti.so.12
```


## Fix cho CUDA 12.2

- Current versions (inside venv)
  - CUDA driver: 535.230.02 (CUDA 12.2 shown by nvidia-smi)
  - PyTorch: 2.8.0+cu128
  - torchvision: 0.23.0
  - torchaudio: 2.8.0
  - vLLM: 0.11.0
  - transformers: 4.57.1
  - tokenizers: 0.22.1

- Why it failed before
  - Global vLLM vs venv Torch ABI mismatch.
  - vLLM 0.6.3 didn’t support DotsOCR or Qwen2-VL well.
  - EngineCore instability and later KV cache OOM with big defaults.

- What fixed it
  - Force venv usage; install matched stack: vLLM 0.11.0 + Torch 2.8.0 (cu12.8).
  - Start via venv python; add safe flags: dtype float16, enforce-eager.
  - Reduce memory pressure: max-model-len 8192, max-num-batched-tokens 4096.

- Quick verify commands
```bash
# GPU/driver
nvidia-smi

# Inside venv
source /home/ubuntu/fintech/OCR/.venv311/bin/activate
python -c "import torch, vllm, transformers; print('torch', torch.__version__, 'vllm', vllm.__version__, 'tfm', transformers.__version__)"
pip show torchvision torchaudio | awk 'NR<=5'
```

