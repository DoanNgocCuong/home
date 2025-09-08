import os
import wget

file_links = [
    {
        "title": "Attention Is All You Need",
        "url": "https://arxiv.org/pdf/1706.03762"
    },
    {
        "title": "BERT- Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "url": "https://arxiv.org/pdf/1810.04805"
    },
    {
        "title": "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
        "url": "https://arxiv.org/pdf/2201.11903"
    },
    {
        "title": "Instruction Tuning for Large Language Models- A Survey",
        "url": "https://arxiv.org/pdf/2308.10792"
    },
    {
        "title": "Llama 2- Open Foundation and Fine-Tuned Chat Models",
        "url": "https://arxiv.org/pdf/2307.09288"
    },
    {
        "title": "DeepSeek LLM Scaling Open-Source Language Models with Longtermism",
        "url": "https://arxiv.org/pdf/2401.02954"
    },
    {
        "title": "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model",
        "url": "https://arxiv.org/pdf/2405.04434"
    },
    {
        "title": "DeepSeek-V3 Technical Report",
        "url": "https://arxiv.org/pdf/2412.19437"
    },
    {
        "title": "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
        "url": "https://arxiv.org/pdf/2501.12948"
    },

]

def is_exist(file_link):
    return os.path.exists(f"./{file_link['title']}.pdf")

for file_link in file_links:
    if not is_exist(file_link):
        wget.download(file_link["url"], out=f"./{file_link['title']}.pdf")


