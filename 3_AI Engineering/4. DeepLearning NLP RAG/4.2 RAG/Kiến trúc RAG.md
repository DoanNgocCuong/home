![[Pasted image 20241219220354.png]]

Prompting vs. RAG vs. Finetuning, which one is best for you, clearly explained:  
  
When building LLM-based apps, it is unlikely you can start using the model right away without adjustments. To maintain high utility, you either need:  
  
• Prompt engineering  
• Fine-tuning  
• RAG  
• Or a hybrid approach (RAG + fine-tuning)  
  
This visual will help you decide:  
  
Two important parameters guide this decision:  
  
• The amount of external knowledge required for your task.  
  
• The amount of adaptation you need.  
↳ Adaptation means changing the behavior of the model, its vocabulary, writing style, etc.  
  
Here's how to decide:  
  
• Use RAGs to generate outputs based on a custom knowledge base if the vocabulary & writing style of the LLM remains the same.  
  
• Use fine-tuning to change the structure (behaviour) of the model than knowledge.  
  
• Prompt engineering is sufficient if you don't have a custom knowledge base and don't want to change the behavior.  
  
• And finally, if your application demands a custom knowledge base and a change in the model's behavior, use a hybrid (RAG + Fine-tuning) approach