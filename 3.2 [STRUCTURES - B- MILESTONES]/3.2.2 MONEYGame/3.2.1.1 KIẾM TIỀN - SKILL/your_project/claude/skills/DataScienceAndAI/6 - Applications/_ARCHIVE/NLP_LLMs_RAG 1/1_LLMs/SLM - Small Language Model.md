https://huggingface.co/QuantFactory/SmolLM2-135M-GGUF

HuggingFaceTB/SmolLM2-135M-Instruct (đã test 50-170ms)
Ngang với: Qwen/Qwen2.5-0.5B-Instruct-AWQ


| Model                                                                                                       | Size | Quantization | Model Size | Context    | Link Download                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------- | ---- | ------------ | ---------- | ---------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Qwen3-0.6B](https://github.com/QwenLM/Qwen3)                                                               | 0.6B | Base FP16    | ~1.2GB     | 32K tokens | [GitHub Qwen3](https://github.com/QwenLM/Qwen3)                                                                 | - [16 query heads và 8 key/value heads (GQA)](https://skywork.ai/blog/models/qwen3-0-6b-fp8-free-chat-online-skywork-ai/) - giảm 50% KV cache memory<br>    <br>- 32,768 token context window natively<br>    <br>- Hỗ trợ **thinking mode** và **non-thinking mode** trong cùng một model<br>    <br>- [Grouped Query Attention architecture](https://skywork.ai/blog/models/qwen3-0-6b-fp8-free-chat-online-skywork-ai/) tối ưu cho inference speed |
| [Qwen3-0.6B-FP8](https://skywork.ai/blog/models/qwen3-0-6b-fp8-free-chat-online-skywork-ai/)                | 0.6B | FP8          | ~600MB     | 32K tokens | [Skywork AI](https://skywork.ai/blog/models/qwen3-0-6b-fp8-free-chat-online-skywork-ai/)                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Qwen3-0.6B-GGUF Q4_K_M                                                                                      | 0.6B | GGUF INT4    | ~180-220MB | 32K tokens | [Ollama](https://ollama.com/library/qwen3) (via ollama pull qwen3:0.6b)                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [Qwen3-ViT-0.5B](https://huggingface.co/models?other=base_model%3Aquantized%3AAname-Tommy%2FQwen3-ViT-0.5B) | 0.5B | Various      | ~150-300MB | -          | [HuggingFace Search](https://huggingface.co/models?other=base_model%3Aquantized%3AAname-Tommy%2FQwen3-ViT-0.5B) |                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

| Model                                                                                    | Size | Quantization    | Latency | Accuracy           | MMLU Score | Link                                                                        |
| ---------------------------------------------------------------------------------------- | ---- | --------------- | ------- | ------------------ | ---------- | --------------------------------------------------------------------------- |
| [Qwen2.5-1.5B-Instruct-AWQ](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-AWQ)       | 1.5B | AWQ INT4        | 30-40ms | **+5-7% vs 0.5B**  | 60%        | [HF Link](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-AWQ)            |
| [Phi-3.5-mini-INT4-ONNX](https://huggingface.co/nvidia/Phi-3.5-mini-Instruct-ONNX-INT4)  | 3.8B | INT4 AWQ (ONNX) | 40-50ms | **+8-10% vs 0.5B** | 69%        | [NVIDIA](https://huggingface.co/nvidia/Phi-3.5-mini-Instruct-ONNX-INT4)     |
| [Gemma-2-2B-IT-AWQ-INT4](https://huggingface.co/Esperanto/gemma-2b-it-kvc-AWQ-int4-onnx) | 2B   | AWQ INT4 (ONNX) | 35-45ms | **+6-8% vs 0.5B**  | 56%        | [Esperanto](https://huggingface.co/Esperanto/gemma-2b-it-kvc-AWQ-int4-onnx) |

---

 # Model: "Qwen/Qwen2.5-0.5B-Instruct-GPTQ-Int4"



```
Accuracy Ranking:
1. GGUF (best accuracy)
2. GPTQ
3. AWQ

Speed Ranking:
1. AWQ (fastest) ✅
2. GPTQ
3. GGUF (slowest)
```

---
```
CUDA_VISIBLE_DEVICES=0 python -m vllm.entrypoints.openai.api_server \
    --model 'Qwen/Qwen2.5-0.5B-Instruct-AWQ' \
    --host 0.0.0.0 \
    --port 30030 \
    --quantization awq \
    --dtype half \
    --gpu-memory-utilization 0.3 \
    --max-model-len 512 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 512 \
    --enable-prefix-caching \
    --enable-chunked-prefill \
    --swap-space 4 \
    --trust-remote-code \
    --disable-log-requests


Esperanto/gemma-2b-it-kvc-AWQ-int4-onnx
```


# SO sánh Qwen 0.5B với 1.5B 
response time

```
curl --location 'http://103.253.20.30:30030/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
    "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
    "messages": [
      {
        "role": "system",
        "content": "CLASSIFY: '\''yes'\'' if Pika'\''s response confirms a correct factual answer. Otherwise, '\''no'\''. Output ONLY '\''yes'\'' or '\''no'\''."
      },
      {
        "role": "user", 
        "content": "Previous Question: Fantastic! Cụm từ tiếp theo cậu nha. Khi chào tạm biệt bạn bè, tớ hay dùng cụm này nè. Bắt đầu chậm trước nha See you soon \n Previous Answer: đúng rùi \n Previous Answer: See you soon \n Pika'\''s response need check: I think this lesson is interesting"
      }
    ],
    "temperature": 0,
    "max_tokens": 1, 
    "stop": ["\n", " ", ".", ","]
  }'
```

---


# Tối ưu: 
## Trên dev con Qwen 2.5 - 1.5B mình host chiếm tới 5GB VRAM => Sau giảm: gpu-memory-utilization 0.2 về 0.1 thì giảm được 1 nửa (CCU sẽ khoảng 15)  

> a Trúc support việc nhắc giảm GPU VRAM chiếm dụng ngày 22/01/2026
> woa, sao a Trúc tính toán dung lượng VRAM model nhanh phết nhỉ . 
> Mình có muốn có năng lực đó không và bằng cách nào. 


---

## 27022026 - Lỗi Spelling 

> Câu chuyện: 1 ngày đẹp trời khi đang ở trong group tag và báo lỗi moods trả ra không hợp lệ và tag mình. 
> 1. Bản có chứa `sobbing` chỉ trên dev chưa lên Production mà sao đã bị trả ra? 
> => Khi bị người khác ping lỗi, thông thường chúng ta sẽ nghĩ: MÌNH LÀM ĐÚNG RỒI MÀ, LỖI NÀY TỪ PHÍA NGƯỜI KHÁC. Và mình cũng bị mắc lỗi này. 
> => Cho dù về sau là lỗi người khác thật thì cũng hãy nhớ. MÌNH SẼ LUÔN NGHĨ: CÓ THỂ LÀ LỖI MÌNH, LỖI NGƯỜI KHÁC, TRACE LOG LÀ RÕ VÀ KO TRÁCH MÌNH, KO TRÁCH NGƯỜI. 
> 2. Sau khi trace log thì mình thấy có 2 vấn đề: 
>    +, Bên mình trả ra:                 "content": "achivement", bị lỗi spelling. (cụ thể đúng phải là: achievement)
>    +, Bên anh Hưng: random chỉ được phép random trong 3 cái, mà sao lại random cả kho để mà trả ra cái sobbins khóc?? và lỗi này bị từ lâu rùi
>    => CỨ CÓ LOG TRACE LÀ NGON. 

```
1. MÌNH SẼ LUÔN NGHĨ: CÓ THỂ LÀ LỖI MÌNH, LỖI NGƯỜI KHÁC, TRACE LOG LÀ RÕ VÀ KO TRÁCH MÌNH, KO TRÁCH NGƯỜI. 
2. Luôn phải có LOG để xử lý trong mọi tình huống bug phía service mình hoặc service khác. 
```


![](image/Pasted%20image%2020260227095009.png)


![](image/Pasted%20image%2020260227094210.png)


Vấn đề ở đây khá rõ ràng:

**Model trả về `"achivement"` — viết sai chính tả** (thiếu chữ `e`, đúng phải là `"achievement"`).

---

Các cách đã test 

### Cách 1: Constrained output / Guided decoding** — Nếu vLLM server hỗ trợ, dùng `guided_choice` để ép model chỉ output đúng token trong danh sách cho phép. Với vLLM, bạn có thể thêm vào request:

```json
{
  "guided_choice": ["happy", "achievement", "thinking", "calm", "sad", "worried", "angry", "surprised"]
}
```

Cách số 3 là **giải pháp gốc rễ** tốt nhất — model sẽ không thể output sai chính tả vì bị constrain chỉ chọn trong danh sách. Bạn đang dùng vLLM phải không? Nếu đúng thì `guided_choice` là cách triệt để nhất, không cần fuzzy matching hay xử lý typo gì cả.


```bash
curl --location 'https://robot-ai-slm.hacknao.edu.vn/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "messages": [
    {
      "role": "system",
      "content": "Classify emotion. Output ONE word ONLY.\n\nRULES:\n- happy: yêu, tuyệt, cảm ơn, vui, hạnh phúc\n- achievement: chúc mừng, tuyệt vời, giỏi\n- thinking: Tại sao, suy nghĩ, hỏi, tò mò\n- calm: không sao, yên tĩnh, bình thường\n- sad: thất vọng, tiếc, buồn\n- worried: lo, sợ, bối rối, lo lắng\n- angry: khó chịu, tức giận, nổi giận\n- surprised: Bất ngờ, ngạc nhiên\n\nOUTPUT: (happy, achievement, thinking, calm, sad, sing, worried, angry, surprised)"
    },
    {
      "role": "user",
      "content": "Previous Pika Robot'\''s Response: {{previous_question}}\nNow Pika Robot'\''s Response need check: 「すごい」はベトナム語で「tuyệt vời」って言うよ！他にも知りたい言葉ある？ \"Sugoi\" in Vietnamese is \"tuyệt vời\"!"
    }
  ],
  "temperature": 0,
  "max_tokens": 5,
  "guided_choice": ["happy", "achievement", "thinking", "calm", "sad", "worried", "angry", "surprised"],
  "stop": [
    "\n",
    " ",
    ".",
    ","
  ]
}'
```

Tuy nhiên cách này kéo response_time từ 50ms lên tận 3s

---

### Cách 2 (đã work)📋 — Enum trong System Prompt (Không cần thay đổi infra)

Thêm ràng buộc rõ ràng hơn trong prompt, kết hợp `stop` tokens:

```
OUTPUT MUST BE EXACTLY ONE OF: happy|achievement|thinking|calm|sad|worried|angry|surprised
DO NOT OUTPUT ANYTHING ELSE. COPY EXACTLY FROM THE LIST ABOVE.
```

```
```


Ô, thật bất ngờ khi dùng giải pháp này đã work. 

![](image/Pasted%20image%2020260227104026.png)

![](image/Pasted%20image%2020260227104049.png)



## 2/3/2026 PROBLEM SOLVING khi xử lý vấn đề 
![](image/Pasted%20image%2020260302094654.png)

### Sai lầm 1: Bị cảm xúc chi phối dẫn tới việc phản ứng sai: Mọi người hỏi tại sao lại trả ra biểu cảm Pika 'angry' ở đây. 

=> Câu trả lời cảm xúc: Là do Pika nói có chứa từ tức giận. Câu này LLM sẽ bắt, ko phải bắt theo keyword mà là phân nhóm dựa trên câu nói của Pika => thành ra bị gán nhầm vào tức giận. 

=> Câu trả lời chính xác là: 

1. Đoạn này nếu chuẩn ra sẽ ra biểu cảm là trung tính. 
2. Tại sao nó không trả ra biểu cảm trung tính mà lại trả ra biểu cảm angry? 
   +, 1 do Models SLM giới hạn của model nhỏ 
   +, giới hạn của Prompt 
   +, Độ chính xác của SLM và Prompt như thế thì phương án gợi ý là có thể bỏ các nhóm tiêu cực đi. 


### Sai lầm 2: Khi chị ... hỏi: Sao chị nhớ đã bỏ đi các moods tiêu cực rùi mà vẫn còn

=> trả lời cảm xúc: rụt rè và bảo : hình như đợt trước anh ... chưa bỏ chị ạ . 
=> Trả lời chuẩn: Cảm xúc chắc chắn, chị đợi xíu em check log ạ. 
+. Đợt trước đoạn đó tụi em recommend xoá, nhưng ... muốn giữ lại chị ạ. 

=> Làm sao để ko bị tâm phản ứng khi xử lý các vấn đề


---

### Xử lý

Những tình huống bạn gặp phải khi xử lý bug của model Qwen/SLM là những ví dụ cực kỳ điển hình của việc bộ não tự động bật chế độ "chiến đấu hoặc bỏ chạy" (fight or flight) khi cảm thấy bị đe dọa (bị ping lỗi, bị sếp/đồng nghiệp chất vấn).

Để không bị "tâm phản ứng" chi phối, chúng ta sẽ áp dụng chính **Ma Trận Chuyển Hóa 3x2** và **Khung 3C** của bạn để bóc tách và giải quyết triệt để vấn đề này.


---
## 07/03/2026 - PROMPTING 

### Prompt 1 

```bash
curl --location 'http://103.253.20.30:30030/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "messages": [
    {
      "role": "system",
      "content": "You are an emotion classifier for Pika Robot'\''s responses.\nTask:\n* Read the conversation snippet.\n* Focus ONLY on \"Now Pika Robot'\''s Response need check\" and identify the MAIN emotion expressed in that turn.\n\nEmotion rules:\nChoose exactly ONE emotion from this list and output only that word:\nhappy, calm, excited, playful, no_problem, encouraging, curious, surprised, proud, thats_right, sad, angry, worry, afraid, noisy, thinking"
    },
    {
      "role": "user",
      "content": "Previous Pika Robot'\''s Response: Chào cậu!\nNow Pika Robot'\''s Response need check: Tớ là Pika!"
    }
  ],
  "temperature": 0,
  "max_tokens": 5,
  "stop": [
    "\n",
    " ",
    ".",
    ","
  ]
}'
```


### Prompt 2 : Rõ ràng về mặt Prompt và kết quả tốt hơn

```bash
curl --location 'http://103.253.20.30:30030/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "messages": [
    {
      "role": "system",
      "content": "Classify Pika Robot'\''s Vietnamese utterance. Output ONE category only.\n\nCLASSIFICATION RULES (first match wins):\n\nACTION INTENTS\n- guidance: nhìn xuống, lên, trái, phải\n- sing: \"hát\", \"múa\", \"bài hát\", \"hát cho cậu nghe\"\n- imaginative: \"biến thành\", \"giả làm\", \"đóng vai\", \"tưởng tượng\"\n- underwater: \"biển\", \"bơi lội\", \"dưới nước\", \"lặn\"\n- secret: \"bí mật\", \"quay cuồng\", \"làm trò\", \"goofy\"\n\nEMOTION INTENTS\n- achievement: \"giỏi lắm\", \"đúng rồi\", \"chúc mừng\", \"xuất sắc\", \"tuyệt vời\"\n- thinking: \"Tại sao\", \"Tò mò quá\", \"suy nghĩ\", \"để tớ nghĩ xem\", \"hỏi\"\n- sending_heart: \"yêu cậu\", \"gửi trái tim\", \"vui\", \"tuyệt\", \"cảm ơn\", \"vui vẻ\", \"hạnh phúc\", \"tốt\"\n- sad: \"buồn\", \"thất vọng\", \"tiếc quá\", \"buồn bã\", \"tủi thân\"\n- worried: \"lo lắng\", \"sợ\", \"bối rối\", \"lo\", \"sợ hãi\", \"bối rối\"\n- angry: \"bực\", \"giận\", \"khó chịu\", \"tức giận\", \"nổi giận\"\n- surprised: \"Bất ngờ\", \"ngạc nhiên\", \"không ngờ\", \"Á\"\n- calm: \"không sao\", \"bình thường\", \"nhớ lại\", \"bình tĩnh\", \"yên tĩnh\"\n\nOUTPUT: ONE word from (guidance, sending_heart, sing, imaginative, underwater, secret, achievement, thinking, happy, sad, worried, angry, surprised, calm)."
    },
    {
      "role": "user",
      "content": "Previous Pika Robot'\''s Response: Xin chào cậu!\nNow Pika Robot'\''s Response need check: Cậu tuyệt thế nhỉ"
    }
  ],
  "temperature": 0,
  "max_tokens": 3,
  "stop": [
    "\n",
    " ",
    ".",
    ","
  ]
}'
```

### Prompt 3 : Rõ ràng về mặt prompt để tránh lỗi Spelling

```bash
curl --location 'http://103.253.20.30:30030/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "messages": [
    {
      "role": "system",
      "content": "Classify emotion. Output ONE word ONLY.\n\nRULES:\n- happy: yêu, tuyệt, cảm ơn, vui, hạnh phúc\n- achievement: chúc mừng, tuyệt vời, giỏi\n- thinking: Tại sao, suy nghĩ, hỏi, tò mò\n- calm: không sao, yên tĩnh, bình thường\n- sad: thất vọng, tiếc, buồn\n- worried: lo, sợ, bối rối, lo lắng\n- angry: khó chịu, tức giận, nổi giận\n- surprised: Bất ngờ, ngạc nhiên\n\nOUTPUT MUST BE EXACTLY ONE OF: happy|achievement|thinking|calm|sad|worried|angry|surprised\nDO NOT OUTPUT ANYTHING ELSE. COPY EXACTLY FROM THE LIST ABOVE."
    },
    {
      "role": "user",
      "content": "Previous Pika Robot'\''s Response: {{previous_question}}\nNow Pika Robot'\''s Response need check: 「すごい」はベトナム語で「tuyệt vời」って言うよ！他にも知りたい言葉ある？ \"Sugoi\" in Vietnamese is \"tuyệt vời\"!"
    }
  ],
  "temperature": 0,
  "max_tokens": 5,
  "stop": [
    "\n",
    " ",
    ".",
    ","
  ]
}'
```

### Prompt 4 : Return only số => giúp tối ưu về response time hơn nữa

```bash
Task: classify robot response into category 1-5.

1=happy (fun, excited, playful, storytelling)
2=achievement (praise: "Wow!", "Tuyet voi!", thanks, correct)
3=thinking (question, instruction, choice, suggestion, request)
4=calm (reassure, comfort, "khong sao", "to khoe", gentle)
5=surprised (ONLY greeting by name: "Chao [name]!", "Hello!")

RULE: if sentence asks or suggests something -> 3
RULE: "Wow!" or "Cam on" -> 2
RULE: "Chao" + name -> 5

"Hay qua!" -> 1
"Wow!" -> 2
"Cau muon thu?" -> 3
"Khong sao dau" -> 4
"Chao Soc!" -> 5
"Yeah!" -> 1
"Cam on cau!" -> 2
"Hay la minh choi?" -> 3
"To khoe lam" -> 4
"Hello Manh!" -> 5

Reply ONLY: 1, 2, 3, 4, or 5.
```