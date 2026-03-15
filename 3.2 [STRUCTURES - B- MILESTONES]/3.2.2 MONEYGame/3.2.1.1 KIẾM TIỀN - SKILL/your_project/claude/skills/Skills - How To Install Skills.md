
- [https://github.com/sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) : Bộ sưu tập 1,254+ agentic skills cho Claude Code, Gemini CLI, Cursor, Copilot… phủ toàn bộ vòng đời phát triển phần mềm
- [https://github.com/Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) : Kho skills chuyên dụng cho AI Research, FineTune, và các workflow nghiên cứu mô hình AI
- [https://github.com/get-zeked/perplexity-super-skills](https://github.com/get-zeked/perplexity-super-skills) : Skills siêu năng lực cho Perplexity AI, tăng cường khả năng truy vấn, phân tích và tổng hợp thông tin
- [https://github.com/get-zeked/dev-engineering-super-skill](https://github.com/get-zeked/dev-engineering-super-skill) : Skills kỹ thuật phát triển phần mềm chuyên sâu, tối ưu cho engineering workflow
- [https://github.com/vm0-ai/vm0-skills](https://github.com/vm0-ai/vm0-skills) : Bộ skills tập trung vào automation, giúp tự động hóa các tác vụ lặp lại trong quy trình phát triển
- [https://github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) : Danh sách tổng hợp awesome các skills, prompts, và cấu hình tốt nhất cho Claude Code
- [https://github.com/msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) : Bộ skills đa lĩnh vực (agency-style) bao gồm nhiều mảng như marketing, dev, content, và business automation

# Ví dụ:

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
