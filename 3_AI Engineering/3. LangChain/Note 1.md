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