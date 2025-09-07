
```bash
PS D:\GIT\BasicTasksLearning_AIVietnamAIO_20252026\3. FSDS\Module 5\B2_RAG\demo-rag> uv run .\main.py
Enter your question (What do beetles eat?) (or 'exit' to quit): Beetles eat?
2025-07-04 17:10:07,759 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
content='' additional_kwargs={'tool_calls': [{'id': 'call_xGyWFjGr4GOvbCmcs2biI4D8', 'function': {'arguments': '{"__arg1":"Beetles diet"}', 'name': 'search_docs'}, 'type': 'function'}], 'refusal': None} response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 120, 'total_tokens': 139, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_34a54ae93c', 'id': 'chatcmpl-BpXeoGf3EiWvFybFoloPtDrGUcBgK', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None} id='run--f5b1ea02-bca1-4f6d-9b10-e956c71cd9a2-0' tool_calls=[{'name': 'search_docs', 'args': {'__arg1': 'Beetles diet'}, 'id': 'call_xGyWFjGr4GOvbCmcs2biI4D8', 'type': 'tool_call'}] usage_metadata={'input_tokens': 120, 'output_tokens': 19, 'total_tokens': 139, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
[llm/start] [llm:ChatOpenAI] Entering LLM run with input:
{
  "prompts": [
    "System: You are a helpful, factual assistant answering user questions using retrieved context. To fetch relevant documents, you will use the `search_docs` tool. Respond in a concise, neutral tone for a general audience. Use a maximum of three short sentences.If the answer isn’t in the context, say you don’t know.\nHuman: Beetles eat?\nAI: \nTool: [\"Beetles are herbivores and eat plants, leaves, and flowers.\", \"Beetles are omnivores and eat a variety of foods, including other insects.\", \"Some beetles are scavengers and eat decaying organic matter.\"]"
  ]
}
2025-07-04 17:10:09,863 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[llm/end] [llm:ChatOpenAI] [2.09s] Exiting LLM run with output:
{
  "generations": [
    [
      {
        "text": "Beetles have diverse diets; some are herbivores that eat plants, leaves, and flowers, while others are omnivores that consume a variety of foods, including other insects. Additionally, some beetles are scavengers that feed on decaying organic matter.",
        "generation_info": {
          "finish_reason": "stop",
          "logprobs": null
        },
        "type": "ChatGeneration",
        "message": {
          "lc": 1,
          "type": "constructor",
          "id": [
            "langchain",
            "schema",
            "messages",
            "AIMessage"
          ],
          "kwargs": {
            "content": "Beetles have diverse diets; some are herbivores that eat plants, leaves, and flowers, while others are omnivores that consume a variety of foods, including other insects. Additionally, some beetles are scavengers that feed on decaying organic matter.",
            "additional_kwargs": {
              "refusal": null
            },
            "response_metadata": {
              "token_usage": {
                "completion_tokens": 55,
                "prompt_tokens": 198,
                "total_tokens": 253,
                "completion_tokens_details": {
                  "accepted_prediction_tokens": 0,
                  "audio_tokens": 0,
                  "reasoning_tokens": 0,
                  "rejected_prediction_tokens": 0
                },
                "prompt_tokens_details": {
                  "audio_tokens": 0,
                  "cached_tokens": 0
                }
              },
              "model_name": "gpt-4o-mini-2024-07-18",
              "system_fingerprint": "fp_34a54ae93c",
              "id": "chatcmpl-BpXddBmtKUxIv84TD9xTafgunEJN0",
              "service_tier": "default",
              "finish_reason": "stop",
              "logprobs": null
            },
            "type": "ai",
            "id": "run--52a54c07-fea3-4242-bada-372b2f4d713e-0",
            "usage_metadata": {
              "input_tokens": 198,
              "output_tokens": 55,
              "total_tokens": 253,
              "input_token_details": {
                "audio": 0,
                "cache_read": 0
              },
              "output_token_details": {
                "audio": 0,
                "reasoning": 0
              }
            },
            "tool_calls": [],
            "invalid_tool_calls": []
          }
        }
      }
    ]
  ],
  "llm_output": {
    "token_usage": {
      "completion_tokens": 55,
      "prompt_tokens": 198,
      "total_tokens": 253,
      "completion_tokens_details": {
        "accepted_prediction_tokens": 0,
        "audio_tokens": 0,
        "reasoning_tokens": 0,
        "rejected_prediction_tokens": 0
      },
      "prompt_tokens_details": {
        "audio_tokens": 0,
        "cached_tokens": 0
      }
    },
    "model_name": "gpt-4o-mini-2024-07-18",
    "system_fingerprint": "fp_34a54ae93c",
    "id": "chatcmpl-BpXddBmtKUxIv84TD9xTafgunEJN0",
    "service_tier": "default"
  },
  "run": null,
  "type": "LLMResult"
}
2025-07-04 17:10:09,863 - src.utils - INFO - Response: Beetles have diverse diets; some are herbivores that eat plants, leaves, and flowers, while others are omnivores that consume a variety of foods, including other insects. Additionally, some beetles are scavengers that feed on decaying organic matter.
Enter your question (What do beetles eat?) (or 'exit' to quit):
```

