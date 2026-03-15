
# note_RAG_Langchain_01052025_.md

## Chain = prompt | llm

---
![[attachments/Pasted image 20250429183842.png]]
![[attachments/Pasted image 20250429183854.png]]

![[attachments/Pasted image 20250429183746.png]]
```


user_prompt = "Write a detailed analogy between mathematics and a lighthouse."
message = prompt_template.format(prompt=user_prompt)
output = llm.invoke(message)
```

```

prompt = PromptTemplate.from_template("Instruct: {question}\nOutput:")


chain = prompt | llm

response = chain.invoke({"prompt": ""})

```
---

## chain = prompt | llm | output_parser -> How to parse JSON output
1. https://js.langchain.com/docs/how_to/output_parser_json/
2. https://rgbitcode.com/blog/senspond/24

[![LangChain - Output Parser 로 LLM 응답결과를 변형하기](https://tse3.mm.bing.net/th?id=OIP.X1ymjWpPodH_gAna4HMd3wHaDU&pid=Api)](https://rgbitcode.com/blog/senspond/24)
Dưới đây là một ví dụ về cách sử dụng `JsonOutputParser` trong LangChain với Python để yêu cầu một mô hình ngôn ngữ trả về dữ liệu có cấu trúc JSON. Chúng ta sẽ yêu cầu mô hình kể một câu chuyện cười và trả về kết quả dưới dạng JSON.

### 🧪 Mục tiêu: Yêu cầu mô hình kể một câu chuyện cười và trả về kết quả dưới dạng JSON

#### 1. Cài đặt các gói cần thiết

Trước tiên, bạn cần cài đặt các gói sau:

```bash
pip install langchain openai pydantic
```

#### 2. Định nghĩa schema JSON bằng Pydantic

Sử dụng thư viện Pydantic để xác định cấu trúc dữ liệu mong muốn:

```python
from pydantic import BaseModel, Field

class Joke(BaseModel):
    setup: str = Field(description="Câu mở đầu của câu chuyện cười")
    punchline: str = Field(description="Câu kết thúc của câu chuyện cười")
```

#### 3. Tạo mô hình và parser

Khởi tạo mô hình ngôn ngữ và parser để xử lý đầu ra:

```python
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import JsonOutputParser

model = ChatOpenAI(model_name="gpt-4", temperature=0)
parser = JsonOutputParser(pydantic_object=Joke)
```

#### 4. Tạo prompt và thực thi chuỗi

Tạo prompt để yêu cầu mô hình kể một câu chuyện cười và xử lý kết quả:

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Bạn là một AI chuyên kể chuyện cười."),
    ("human", "Hãy kể một câu chuyện cười.")
])

chain = prompt | model | parser

result = chain.invoke({})
print(result)
```

#### 5. Kết quả mẫu

Kết quả đầu ra sẽ có dạng:

```json
{
  "setup": "Tại sao con gà băng qua đường?",
  "punchline": "Để đến phía bên kia!"
}
```

---

Bạn có thể tìm hiểu thêm về cách sử dụng `JsonOutputParser` trong LangChain tại tài liệu chính thức:

- [How to parse JSON output | LangChain](https://python.langchain.com/docs/modules/model_io/output_parsers/json/)

Nếu bạn cần thêm ví dụ hoặc hỗ trợ về các trường hợp sử dụng cụ thể, hãy cho tôi biết! 