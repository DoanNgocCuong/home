
1. Model qwen2.5-1.5B-AWQ

```bash
# qwen2.5_docker-compose.yml
name: vllm-emotion-classifier

services:
  vllm-qwen:
    container_name: vllm-qwen-emotion
    image: vllm/vllm-openai:v0.6.6.post1  # CUDA 12.1 compatible
    runtime: nvidia
    network_mode: host
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
    command: >
      --model Qwen/Qwen2.5-1.5B-Instruct-AWQ
      --host 0.0.0.0
      --port 30030
      --quantization awq
      --dtype half
      --gpu-memory-utilization 0.2
      --max-model-len 512
      --max-num-seqs 16
      --max-num-batched-tokens 512
      --enable-prefix-caching
      --enable-chunked-prefill
      --swap-space 4
      --trust-remote-code
      --disable-log-requests
    restart: always
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

git commit -m "[gpu-memory-utilization 0.2 thì tải được khoảng 30 user cùng lúc, RPS 15 (mỗi user nghỉ 1-3s)]" 

```bash

# qwen2.5_docker-compose.yml
name: vllm-emotion-classifier

services:
  vllm-qwen:
    container_name: vllm-qwen-emotion
    image: vllm/vllm-openai:v0.6.6.post1  # CUDA 12.1 compatible
    runtime: nvidia
    network_mode: host
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
    command: >
      --model Qwen/Qwen2.5-1.5B-Instruct-AWQ
      --host 0.0.0.0
      --port 30030
      --quantization awq
      --dtype half
      --gpu-memory-utilization 0.2
      --max-model-len 512
      --max-num-seqs 16
      --max-num-batched-tokens 512
      --enable-prefix-caching
      --enable-chunked-prefill
      --swap-space 4
      --trust-remote-code
      --disable-log-requests
    restart: always
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]

```

# 1. Khi để: gpu-memory-utilization 0.2

![1765785822493](image/report/1765785822493.png)

# 2. Còn khi để: gpu-memory-utilization 0.1

![1765785902297](image/report/1765785902297.png)


---
