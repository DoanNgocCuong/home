Link chính: [M10W1T6 RAG Prompting Langchain GMT20250418 125200 Recording 1920x1050](https://www.youtube.com/watch?v=U6kR-UrMJww&list=PLQyIFBsiXn12Z6HuhlBQY-4qXykjnEsHi&index=1)

Đọc các dòng comment trên kênh Youtube 

## 1.1 Chain = prompt | llm

---
![[Pasted image 20250429183842.png]]
![[Pasted image 20250429183854.png]]

![[Pasted image 20250429183746.png]]
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

## 1.2 chain = prompt | llm | output_parser -> How to parse JSON output
1. https://js.langchain.com/docs/how_to/output_parser_json/
2. https://rgbitcode.com/blog/senspond/24