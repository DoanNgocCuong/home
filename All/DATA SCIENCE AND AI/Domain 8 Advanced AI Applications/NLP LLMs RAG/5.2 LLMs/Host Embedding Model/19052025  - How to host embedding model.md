![[Pasted image 20250519155653.png]]

```bash
from sentence_transformers import SentenceTransformer
import os

# Đường dẫn lưu model
model_path = os.path.join(os.path.dirname(os.path.dirname(_file_)), "model")
os.makedirs(model_path, exist_ok=True)

# Tên model trên Hugging Face Hub
model_name = 'paraphrase-multilingual-mpnet-base-v2'

print(f"Bắt đầu tải model '{model_name}'...")
print(f"Thư mục lưu model: {model_path}")

# Load model và lưu vào thư mục chỉ định
model = SentenceTransformer(model_name, cache_folder=model_path)

print(f"Model '{model_name}' đã được load thành công về local.")

# Bây giờ bạn có thể sử dụng model để encode các câu
sentences = [
    "Đây là một câu ví dụ.",
    "This is an example sentence.",
    "Hola, esto es una frase de ejemplo."
]

print("Đang tạo embeddings...")
embeddings = model.encode(sentences)

print("Embeddings của các câu:")
for sentence, embedding in zip(sentences, embeddings):
    print(f"Câu: {sentence}")
    print(f"Embedding shape: {embedding.shape}")
    print("-" * 20)
```