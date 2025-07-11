Link: [M8W2T6 Project QA for Content Inquiry Text Classification and NER 20250214](https://www.youtube.com/watch?v=G4JAQhg4NWg)
Link bài Linkedin: https://www.linkedin.com/posts/doan-ngoc-cuong_wecommit100x-wecommit100xsharing-doanngoccuong-activity-7297579264684568576-ygzg?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAC3wojwBYfkOk3q0b6y8Z_UF_N5ELvjQYVI



Traditional QA systems, developed before the advent of large language models (LLMs), combine document retrieval with document reading. They typically work in two stages: a retriever selects top relevant documents from a large corpus, and a reader extracts or generates the answer based on the retrieved content.


| **Aspect**                                                      | **Description**                                                                                                                                                                                                                                                       |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **QA Systems**                                                  | Traditional QA systems, developed before the advent of large language models (LLMs), combine document retrieval with document reading.                                                                                                                                |
| **Two-Part System**                                             | - **Retriever:** Searches a large corpus for top relevant documents.<br>- **Reader:** Processes retrieved documents with the question to extract/generate the answer.                                                                                                 |
| **TYPE OF RETRIEVER- QA Context**                               | - **Visual QA (VQA):** Uses images as context and typically applies a classification approach.<br>- **Text-Only QA:** Uses text documents and often employs an extractive approach.                                                                                   |
| **TYPE OF READER - Response Answer Approach**                   | - **Classification Approach:** Selects an answer from a set of options (common in VQA).<br>- **Extractive Approach:** Identifies the start and end of the answer span (similar to NER).<br>- **Generative Approach:** Uses autoregressive models to generate answers. |
| **RAG (Retrieval Augmented Generation) or Generative Approach** | Combining the ability to retrieve external information as context and supplementing the question's context helps LLMs address hallucination errors and outdated content.                                                                                              |
|                                                                 |                                                                                                                                                                                                                                                                       |
![[Pasted image 20250218174931.png]]

![[Pasted image 20250218175106.png]]