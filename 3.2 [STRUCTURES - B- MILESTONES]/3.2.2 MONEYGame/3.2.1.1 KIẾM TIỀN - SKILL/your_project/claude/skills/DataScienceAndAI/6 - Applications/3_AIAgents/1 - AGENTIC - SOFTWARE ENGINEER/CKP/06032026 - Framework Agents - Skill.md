https://github.com/sickn33/antigravity-awesome-skills
https://github.com/Orchestra-Research/AI-Research-SKILLs

Khi Run 
```bash
npx @orchestra-research/ai-research-skills
```

```
❯ Install new skills 
  Install to project (local) → ./home/ubuntu 
  View installed skills 
  Update installed skills 
  Uninstall skills 
```

Khi chạy `npx @orchestra-research/ai-research-skills`, nó cài vào:

```
~/.orchestra/skills/
```

Đây là nơi lưu trữ thực tế của 44 skills về AI/ML:

```
~/.orchestra/skills/
├── 03-fine-tuning/      # axolotl, llama-factory, peft, unsloth
├── 06-post-training/    # grpo-rl-training, miles, openrlhf, simpo, slime, trl-fine-tuning, verl
├── 08-distributed-training/  # accelerate, deepspeed, megatron-core, pytorch-fsdp2, pytorch-lightning, ray-train
├── 10-optimization/     # awq, bitsandbytes, flash-attention, gguf, gptq, hqq
├── 11-evaluation/       # bigcode-evaluation-harness, lm-evaluation-harness, nemo-evaluator
├── 12-inference-serving/ # llama-cpp, sglang, tensorrt-llm, vllm
├── 13-mlops/            # mlflow, tensorboard, weights-and-biases
├── 15-rag/              # chroma, faiss, pinecone, qdrant, sentence-transformers
└── 16-prompt-engineering/  # dspy, guidance, instructor, outlines
```

Rồi sau đó, các skills này được **symlink** sang `~/.claude/skills/` để Claude Opus có thể sử dụng được.

Toàn vũ khí hạng nặng cả

![](image/Pasted%20image%2020260307162654.png)