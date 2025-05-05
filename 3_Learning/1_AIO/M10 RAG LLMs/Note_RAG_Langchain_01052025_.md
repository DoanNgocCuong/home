Link chính: [M10W1T6 RAG Prompting Langchain GMT20250418 125200 Recording 1920x1050](https://www.youtube.com/watch?v=U6kR-UrMJww&list=PLQyIFBsiXn12Z6HuhlBQY-4qXykjnEsHi&index=1)



![[Pasted image 20250502235836.png]]

![[Pasted image 20250503000241.png]]

1. LangChain-Core => Sau cộng đồng chung tay phát triển gọi là LangChain-Community. 
- Langchain: Model I/O - Retrieval - Agents - Tools - Memory - Chains 
2. LangServe triển API (tích hợp FastAPI bên trong) 
3. LangSmith: mornitoring
4. Thời điểm sau này, phát triển LangGraph thay thế LangServe - LangGraph Platform (commercial)


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

---
done. 03/05/2025

```
Lời nói đầu: Biết LangChain từ giữa năm 2024. Nhưng cũng phải đến 2/5/2025 mới dành thời gian học về LangChain, (trong khoảng thời gian đó em có làm về Prompting rất nhiều ở công ty, số Prompt viết phải tầm 50 cái chạy thực trên Production, cũng làm RAG, làm Chain of Prompt đơn giản có, phức tạp có, ... tuy nhiên Langchain quá to so với niềm tin giới hạn lúc đó mà chưa động vào)


```

Bài Linkedin: https://www.linkedin.com/posts/doan-ngoc-cuong_doanngoccuong-langchain-langgraph-activity-7324117703378505728-k6ok?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAC3wojwBYfkOk3q0b6y8Z_UF_N5ELvjQYVI
Bài FB Wecommit100x: [Facebook](https://www.facebook.com/photo/?fbid=2156536948197061&set=gm.24166559526264376&idorvanity=3376347132378919)
Bài FullStackDataScience: [LangChain Tổng Quan và Lịch sử phát triển  | FSDS](https://fullstackdatascience.com/forum/topic/123)
Bài AIO: [Facebook](https://www.facebook.com/photo/?fbid=2156544034863019&set=gm.1628425914485435&idorvanity=1507316089929752)

```
****MỘT CÁCH TỔNG QUAN NHẤT VỀ LANGCHAIN - Bài giảng RAG của TA**** Dương Nguyễn Thuận  
##### MỘT CÁCH TỔNG QUAN NHẤT VỀ LANGCHAIN - 1 Framework phổ biến trong phát triển các ứng dụng LLMS, RAG, AI AGENTS, .... Langchain đơn giản hóa mọi giai đoạn của vòng đời ứng dụng LLM.
---
  
1. LangChain-Core => Sau cộng đồng chung tay phát triển gọi là LangChain-Community.  
- Main Components: Model I/O - Retrieval - Agents - Tools - Memory - Chains

2. LangServe triển API (tích hợp FastAPI, Pydantic bên trong)  
3. LangSmith: mornitoring  
4. Thời điểm sau này, phát triển LangGraph thay thế LangServe - và LangGraph Platform (commercial)

> Biết LangChain từ giữa năm 2024, nghe về Langchain cũng nhiều.  
> Trong khoảng thời gian từ 2024 đến cuối T4/2025 em có làm về Prompting rất nhiều ở công ty (số Prompt viết chạy thực trên Production cũng trên dưới 50 cái), cũng làm RAG, làm Chain of Prompt đơn giản có, phức tạp có, ... cơ mà toàn code chay từ đầu.  
> Phải đến đầu tháng 5/2025 có video record về RAG của TA Thuận em mới dành thời gian nghe và học về LangChain. Thank TA Dương Nguyễn Thuận ạ.
```