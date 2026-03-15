```
services:
  vllm-qwen:
    container_name: vllm-qwen-emotion
    image: vllm/vllm-openai:v0.6.6.post1
    runtime: nvidia
    expose:
      - "30030"
    environment:
      - NVIDIA_VISIBLE_DEVICES=1
    command: >
      --model Qwen/Qwen2.5-1.5B-Instruct-AWQ
      --host 0.0.0.0
      --port 30030
      --quantization awq
      --dtype half
      --gpu-memory-utilization 0.1
      --max-model-len 512
      --max-num-seqs 64
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
    networks:
      - emotion-network

  nginx-proxy:
    container_name: nginx-emotion-proxy
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "30030:8080"
    depends_on:
      - vllm-qwen
    restart: unless-stopped
    networks:
      - emotion-network

networks:
  emotion-network:
    driver: bridge

```


## Sửa max-num-seqs từ 16 -> 64 làm tăng P95, P99 mặc dù Througput được tăng

```

```

![](image/Pasted%20image%2020260129163500.png)