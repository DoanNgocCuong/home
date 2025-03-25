1. [Welcome to the 🤗 AI Agents Course - Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction)
2. https://docs.livekit.io/agents/
3. [The Top 10 arXiv Papers About AI Agents (especially Voice AI Agents) | Deepgram](https://deepgram.com/learn/top-arxiv-papers-about-ai-agents-and-voice-ai-agents)
4. https://www.automationanywhere.com/company/blog/automation-ai/exploring-ai-agents-types-capabilities-and-real-world-applications

---


Gần đây, có nhiều nghiên cứu tập trung vào việc cải thiện cơ chế quản lý bộ nhớ trong các tác nhân AI:

- **A-MEM: Agentic Memory for LLM Agents:** Nghiên cứu này đề xuất một hệ thống bộ nhớ tác nhân cho các mô hình ngôn ngữ lớn, cho phép tổ chức bộ nhớ một cách linh hoạt và hiệu quả hơn. Hệ thống này tạo ra các mạng lưới kiến thức liên kết thông qua việc lập chỉ mục và liên kết động, dựa trên nguyên tắc của phương pháp Zettelkasten. citeturn0search5
    
- **Zep: A Temporal Knowledge Graph Architecture for Agent Memory:** Zep là một kiến trúc đồ thị tri thức tạm thời được thiết kế để cải thiện khả năng ghi nhớ của các tác nhân AI. Nó vượt trội hơn so với các hệ thống hiện có như MemGPT trong việc truy xuất bộ nhớ sâu và phù hợp với các ứng dụng thực tế trong doanh nghiệp. citeturn0search7
    
- **A Survey on the Memory Mechanism of Large Language Model based Agents:** Bài khảo sát này tập trung vào cơ chế bộ nhớ của các tác nhân dựa trên mô hình ngôn ngữ lớn, nhấn mạnh tầm quan trọng của khả năng tự tiến hóa và tương tác dài hạn giữa tác nhân và môi trường. citeturn0search1
    

Tổng kết, cả LangGraph và Mem0 đều cung cấp các giải pháp linh hoạt cho việc quản lý bộ nhớ trong các tác nhân AI, giúp cải thiện khả năng tương tác và cá nhân hóa. Các nghiên cứu mới nhất tiếp tục mở rộng khả năng của bộ nhớ trong AI, hướng tới việc tạo ra các tác nhân AI thông minh và hiệu quả hơn.



---
# Deep Research: Nguồn 12/3/2025

```
Citations

[

langchain-ai.github.io

Memory

Short-term memory, or thread -scoped memory, can be recalled at any time from within a single conversational thread with a user. LangGraph manages short- term memory as a part of your agent's 51. State is persisted to a database using a checkpointer so the thread can be resumed at any time. Short-term memory updates when the graph is invoked or a step is completed, and the State is read at the start of each step.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Short,the%20start%20of%20each%20step)[

langchain-ai.github.io

Memory

LangGraph manages short-term memory as part of the agent's state, persisted via thread-scoped checkpoints. This state can normally include the conversation history along with other stateful data, such as uploaded files, retrieved documents, or generated artifacts. By storing these in the graph's state, the bot can access the full context for a given conversation while maintaining separation between different threads.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=LangGraph%20manages%20short,maintaining%20separation%20between%20different%20threads)[

langchain-ai.github.io

Memory

Short-term memory, or thread -scoped memory, can be recalled at any time from within a single conversational thread with a user. LangGraph manages short- term memory as a part of your agent's 51. State is persisted to a database using a checkpointer so the thread can be resumed at any time. Short-term memory updates when the graph is invoked or a step is completed, and the State is read at the start of each step.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Short,the%20start%20of%20each%20step)[

langchain-ai.github.io

Memory

Long conversations pose a challenge to today's LLMs. The full history may not even fit inside an LLM's context window, resulting in an irrecoverable error. Even if your LLM technically supports the full context length, most LLMs still perform poorly over long contexts. They get "distracted" by stale or off-topic content, all while suffering from slower response times and higher costs.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Long%20conversations%20pose%20a%20challenge,response%20times%20and%20higher%20costs)[

langchain-ai.github.io

Memory

Chat models accept context using messages, which include developer provided instructions (a system message) and user inputs (human messages). In chat applications, messages alternate between human inputs and model responses, resulting in a list of messages that grows longer over time. Because context windows are limited and token-rich message lists can be costly, many applications can benefit from using techniques to manually remove or forget stale information.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Chat%20models%20accept%20context%20using,remove%20or%20forget%20stale%20information)[

langchain-ai.github.io

Memory

Summarizing past conversations¶

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Summarizing%20past%20conversations%C2%B6)[

langchain-ai.github.io

Memory

def summarize_conversation(state: State):

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=def%20summarize_conversation)[

langchain-ai.github.io

Memory

Long-term memory is shared across conversational threads. It can be recalled at any time and in any thread. Memories are scoped to any custom namespace, not just within a single thread ID. LangGraph provides stores (reference doc) to let you save and recall long-term memories.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Long,term%20memories)[

langchain-ai.github.io

Memory

Long-term memory in LangGraph allows systems to retain information across different conversations or sessions. Unlike short-term memory, which is thread-

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Long,term%20memory%2C%20which%20is%20thread)[

langchain-ai.github.io

Memory

LangGraph stores long-term memories as JSON documents in a store ( 54). Each memory is organized under a custom `namespace` (similar to a folder) and a distinct `key` (like a filename). Namespaces often include user or org IDs or other labels that makes it easier to organize information. This structure enables hierarchical organization of memories. Cross-namespace searching is then supported through content filters. See the example below for an example.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=LangGraph%20stores%20long,example%20below%20for%20an%20example)[

langchain-ai.github.io

Memory

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use. store = InMemoryStore(index={"embed": embed, "dims": 2}) user_id = "my-user" application_context = "chitchat" namespace = (user_id, application_context) store.put( namespace, "a-memory",

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=,memory)[

langchain-ai.github.io

Memory

user_id = "my-user" application_context = "chitchat" namespace = (user_id, application_context) store.put( namespace, "a-memory", { "rules": [ "User likes short, direct language",

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=user_id%20%3D%20%22my,User%20likes%20short%2C%20direct%20language)[

langchain-ai.github.io

Memory

# get the "memory" by ID item = store.get(namespace, "a-memory") # search for "memories" within this namespace, filtering on content equivalence, sorted by vector similarity items = store.search( namespace, filter={"my-key": "my-value"}, query="language preferences" )

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=,value%22%7D%2C%20query%3D%22language%20preferences%22)[

langchain-ai.github.io

Memory

Long-term memory is shared across conversational threads. It can be recalled at any time and in any thread. Memories are scoped to any custom namespace, not just within a single thread ID. LangGraph provides stores ( 54) to let you save and recall long-term memories.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Long,term%20memories)[

langchain-ai.github.io

Memory

Different applications require various types of memory. Although the analogy isn't perfect, examining human memory types can be insightful. Some research (e.g., the CoALA paper) have even mapped these human memory types to those used in AI agents.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Different%20applications%20require%20various%20types,those%20used%20in%20AI%20agents)[

langchain-ai.github.io

Memory

Memory Type What is Stored Human Example Agent Example Semantic Facts Things I learned in school Facts about a user Episodic Experiences Things I did Past agent actions Procedural Instructions Instincts or motor skills Agent system prompt

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Memory%20Type%20What%20is%20Stored,motor%20skills%20Agent%20system%20prompt)[

langchain-ai.github.io

Memory

Semantic memory, both in humans and AI agents, involves the retention of specific facts and concepts. In humans, it can include information learned in school and the understanding of concepts and their relationships. For AI agents, semantic memory is often used to personalize applications by remembering facts or concepts from past interactions.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Semantic%20memory%2C%20both%20in%20humans,or%20concepts%20from%20past%20interactions)[

langchain-ai.github.io

Memory

# Profile¶

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=)[

langchain-ai.github.io

Memory

Alternatively, memories can be a collection of documents that are continuously updated and extended over time. Each individual memory can be more narrowly scoped and easier to generate, which means that you're less likely to lose information over time. It's easier for an LLM to generate new objects for new information than reconcile new information with an existing profile. As a result, a document collection tends to lead to higher recall downstream.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=Alternatively%2C%20memories%20can%20be%20a,lead%20to%20higher%20recall%20downstream)[

langchain-ai.github.io

Memory

pairs you've selected to represent your domain.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=pairs%20you%27ve%20selected%20to%20represent,your%20domain)[

langchain-ai.github.io

Memory

However, this shifts some complexity memory updating. The model must now delete or update existing items in the list, which can be tricky. In addition, some models may default to over-inserting and others may default to over-updating. See the Trustcall package for one way to manage this and consider evaluation (e.g., with a tool like LangSmith) to help you tune the behavior.

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=However%2C%20this%20shifts%20some%20complexity,help%20you%20tune%20the%20behavior)[

langchain-ai.github.io

Memory

When do you want to update memories?

](https://langchain-ai.github.io/langgraph/concepts/memory/#:~:text=When%20do%20you%20want%20to,update%20memories)[

![Favicon](https://www.google.com/s2/favicons?domain=https://redis.io&sz=32)redis.io

Smarter memory management for AI agents with Mem0 and Redis - Redis

We’re happy to announce the integration of Mem0 with Redis, a powerful combination that enhances the capabilities of AI agents by providing efficient and scalable memory management. Mem0 is a self-improving memory layer for LLM applications and AI agents, enabling personalized AI experiences that save costs and delight users. Key features of Mem0 include:

](https://redis.io/blog/smarter-memory-management-for-ai-agents-with-mem0-and-redis/#:~:text=We%E2%80%99re%20happy%20to%20announce%20the,Key%20features%20of%20Mem0%20include)[

![Favicon](https://www.google.com/s2/favicons?domain=https://redis.io&sz=32)redis.io

Smarter memory management for AI agents with Mem0 and Redis - Redis

* Optimize AI responses: Deliver more accurate and personalized AI outputs by using historical context and user preferences. * Easy integration: Seamlessly enhance your existing AI solutions with Mem0’s memory layer, compatible with OpenAI, Claude, and more.

](https://redis.io/blog/smarter-memory-management-for-ai-agents-with-mem0-and-redis/#:~:text=,with%20OpenAI%2C%20Claude%2C%20and%20more)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.graphlit.com&sz=32)graphlit.com

Survey of AI Agent Memory Frameworks - Graphlit

Short-Term (Context Window) Memory: – Letta: Utilizes an in-context memory design, showing messages and system prompts within a configurable token limit. Also features core memory blocks that remain visible in the prompt window, and a recall memory for recently accessed data. – Mem0.ai: Offers personalization by storing conversation history and user preferences in memory. Provides short-term memory in chat contexts, enhanced by local or remote vector stores. – Zep: Maintains session-based interactions, storing conversation transcripts as

](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks#:~:text=Short,interactions%2C%20storing%20conversation%20transcripts%20as)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.graphlit.com&sz=32)graphlit.com

Survey of AI Agent Memory Frameworks - Graphlit

sets remain accessible. – Mem0.ai: Supports persistent memory stores keyed to users, sessions, or projects. Offers batch operations (batch-delete, batch-update) and advanced filtering or searching. Embedding integration allows for semantic retrieval across large data sets. – Zep: Relies on a knowledge graph or a memory store to retain facts, messages, and metadata over multiple sessions. Provides robust cloud features (like classification and advanced search) for session data. – CrewAI: Long-term knowledge resides in a specialized entity memory layer where

](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks#:~:text=sets%20remain%20accessible,specialized%20entity%20memory%20layer%20where)[

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.mem0.ai&sz=32)docs.mem0.ai

Memory Types - Mem0

How Mem0 Implements Long-Term Memory

](https://docs.mem0.ai/core-concepts/memory-types#:~:text=How%20Mem0%20Implements%20Long)[

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.mem0.ai&sz=32)docs.mem0.ai

Memory Types - Mem0

Mem0’s long-term memory system builds on these foundations by:

](https://docs.mem0.ai/core-concepts/memory-types#:~:text=Mem0%E2%80%99s%20long,on%20these%20foundations%20by)[

![Favicon](https://www.google.com/s2/favicons?domain=https://microsoft.github.io&sz=32)microsoft.github.io

Mem0: Long-Term Memory and Personalization for Agents | AutoGen 0.2

Comprehensive Memory Management Manage long-term, short-term, semantic, and episodic memories Self-Improving Memory Adaptive system that learns from user interactions Cross-Platform Consistency Unified user experience across various AI platforms ️ Centralized Memory Control Effortless storage, updating, and deletion of memories Simplified Development API-first approach for streamlined integration Activity Dashboard

](https://microsoft.github.io/autogen/0.2/docs/ecosystem/mem0/#:~:text=Comprehensive%20Memory%20Management%20Manage%20long,for%20streamlined%20integration%20Activity%20Dashboard)[

![Favicon](https://www.google.com/s2/favicons?domain=https://microsoft.github.io&sz=32)microsoft.github.io

Mem0: Long-Term Memory and Personalization for Agents | AutoGen 0.2

* Short-term Memory: Manage temporary information within a single interaction * Semantic Memory: Organize and retrieve conceptual knowledge * Episodic Memory: Store and recall specific events or experiences * Self-Improving System: Continuously refine understanding based on user

](https://microsoft.github.io/autogen/0.2/docs/ecosystem/mem0/#:~:text=%2A%20Short,refine%20understanding%20based%20on%20user)[

![Favicon](https://www.google.com/s2/favicons?domain=https://redis.io&sz=32)redis.io

Smarter memory management for AI agents with Mem0 and Redis - Redis

* Improve future conversations: Build smarter AI that learns from every interaction and delivers context-rich responses without repetitive questions. * Save money: Cut LLM costs by up to 80% with intelligent data filtering, sending only the most relevant information to AI models. * Optimize AI responses: Deliver more accurate and personalized AI outputs by using historical context and user preferences. * Easy integration: Seamlessly enhance your existing AI solutions with Mem0’s memory layer, compatible with OpenAI, Claude, and more.

](https://redis.io/blog/smarter-memory-management-for-ai-agents-with-mem0-and-redis/#:~:text=,with%20OpenAI%2C%20Claude%2C%20and%20more)[

news.ycombinator.com

Show HN: Mem0 – open-source Memory Layer for AI apps | Hacker News

Hi this looks interesting. From your description it looks like mem0 remembers details and context of previous chats but not the actual text of chats. Is this a correct assumption?

](https://news.ycombinator.com/item?id=41447317#:~:text=Hi%20this%20looks%20interesting,Is%20this%20a%20correct%20assumption)[

news.ycombinator.com

Show HN: Mem0 – open-source Memory Layer for AI apps | Hacker News

3. Content management: Claude has minimum length requirements for caching (1024 characters for Sonnet, 2048 for Haiku). Mem0 can handle information of any length, from short facts to longer contexts. 4. Customization: Developers have greater control over Mem0's memory management, including options for prioritizing or deprioritizing information based on relevance or time. Claude's caching system offers less direct control. 5. Information retrieval: Mem0 is designed for more precise and targeted information retrieval, while Claude's cache works with broader contextual blocks.

](https://news.ycombinator.com/item?id=41447317#:~:text=3,works%20with%20broader%20contextual%20blocks)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.graphlit.com&sz=32)graphlit.com

Survey of AI Agent Memory Frameworks - Graphlit

Mem0.ai’s Platform and SDKs – Offers both managed and open-source versions with Python, JavaScript, and cURL examples. – Includes memory search, advanced filtering (logical AND/OR, metadata queries), and structured batching for memory creation or deletion. – Supports integration with frameworks like LangChain, MultiOn, CrewAI, LlamaIndex, or custom solutions.

](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks#:~:text=Mem0,CrewAI%2C%20LlamaIndex%2C%20or%20custom%20solutions)[

news.ycombinator.com

Show HN: Mem0 – open-source Memory Layer for AI apps | Hacker News

As mentioned in the post, we use a hybrid datastore approach that handles these cases effectively and that's where the graph aspect comes into picture.

](https://news.ycombinator.com/item?id=41447317#:~:text=As%20mentioned%20in%20the%20post%2C,graph%20aspect%20comes%20into%20picture)[

![Favicon](https://www.google.com/s2/favicons?domain=https://redis.io&sz=32)redis.io

Smarter memory management for AI agents with Mem0 and Redis - Redis

Redis stands out as the top data platform for managing long-term memory in AI agents—here’s why:

](https://redis.io/blog/smarter-memory-management-for-ai-agents-with-mem0-and-redis/#:~:text=Redis%20stands%20out%20as%20the,memory%20in%20AI%20agents%E2%80%94here%E2%80%99s%20why)[

news.ycombinator.com

Show HN: Mem0 – open-source Memory Layer for AI apps | Hacker News

1. Purpose and duration: Claude's cache is designed for short-term memory, clearing every 5 minutes. In contrast, Mem0 is built for long-term information storage, retaining data indefinitely unless instructed otherwise. 2. Flexibility and control: Mem0 offers more flexibility, allowing developers to update, delete, or modify stored information as needed. Claude's cache is more static - new information creates additional entries rather than updating existing ones. 3. Content management: Claude has minimum length requirements for caching (1024 characters for Sonnet, 2048 for Haiku). Mem0 can handle information of any length, from short facts to longer contexts. 4. Customization: Developers have

](https://news.ycombinator.com/item?id=41447317#:~:text=1,Customization%3A%20Developers%20have)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.graphlit.com&sz=32)graphlit.com

Survey of AI Agent Memory Frameworks - Graphlit

Mem0.ai’s Platform and SDKs – Offers both managed and open-source versions with Python, JavaScript, and cURL examples. – Includes memory search, advanced filtering (logical AND/OR, metadata queries), and structured batching for memory creation or deletion. – Supports integration with frameworks like LangChain, MultiOn, CrewAI, LlamaIndex, or custom solutions.

](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks#:~:text=Mem0,CrewAI%2C%20LlamaIndex%2C%20or%20custom%20solutions)[

![Favicon](https://www.google.com/s2/favicons?domain=https://microsoft.github.io&sz=32)microsoft.github.io

Mem0: Long-Term Memory and Personalization for Agents | AutoGen 0.2

Mem0 Platform provides a smart, self-improving memory layer for Large Language Models (LLMs), enabling developers to create personalized AI experiences that evolve with each user interaction.

](https://microsoft.github.io/autogen/0.2/docs/ecosystem/mem0/#:~:text=Mem0%20Platform%20provides%20a%20smart%2C,evolve%20with%20each%20user%20interaction)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.graphlit.com&sz=32)graphlit.com

Survey of AI Agent Memory Frameworks - Graphlit

sets remain accessible. – Mem0.ai: Supports persistent memory stores keyed to users, sessions, or projects. Offers batch operations (batch-delete, batch-update) and advanced filtering or searching. Embedding integration allows for semantic retrieval across large data sets.

](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks#:~:text=sets%20remain%20accessible,retrieval%20across%20large%20data%20sets)[

news.ycombinator.com

Show HN: Mem0 – open-source Memory Layer for AI apps | Hacker News

designed for more precise and targeted information retrieval, while Claude's cache works with broader contextual blocks.

](https://news.ycombinator.com/item?id=41447317#:~:text=designed%20for%20more%20precise%20and,works%20with%20broader%20contextual%20blocks)[

![Favicon](https://www.google.com/s2/favicons?domain=https://redis.io&sz=32)redis.io

Smarter memory management for AI agents with Mem0 and Redis - Redis

1. Fast performance: Redis’ in-memory architecture delivers microsecond-level read and write operations, which is critical for apps where memory retrieval times can significantly impact user experience. 2. Fastest and fully featured vector search: Redis provides an in-built, fully

](https://redis.io/blog/smarter-memory-management-for-ai-agents-with-mem0-and-redis/#:~:text=1.%20Fast%20performance%3A%20Redis%E2%80%99%20in,built%2C%20fully)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.anthropic.com&sz=32)anthropic.com

Introducing 100K Context Windows \ Anthropic

We’ve expanded Claude’s context window from 9K to 100K tokens, corresponding to around 75,000 words! This means businesses can now submit hundreds of pages of materials for Claude to digest and analyze, and conversations with Claude can go on for hours or even days.

](https://www.anthropic.com/news/100k-context-windows#:~:text=We%E2%80%99ve%20expanded%20Claude%E2%80%99s%20context%20window,for%20hours%20or%20even%20days)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

Personalized LLM Response Generation with Parameterized User Memory Injection

this paradigm suffers from the long-context window limitation of LLM (Liu et al., 2024 ). Memory-based approaches provide a solution by leveraging a memory to store user historical content. When a new user query comes, a retriever will first retrieve relevant user information from the memory to prompt LLM produce personalized responses (Dalvi et al., 30; Madaan et al., 2022 ; Lewis et al., 32; Zhang et al., 2023 ). Unfortunately, they are limited in capturing fine-grained information due to the nature of similarity comparison retrieval process (Zhang et al., 33). Additionally, user historical content can be complex and noisy, posing

](https://arxiv.org/html/2404.03565v2#:~:text=this%20paradigm%20suffers%20from%20the,be%20complex%20and%20noisy%2C%20posing)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.lukew.com&sz=32)lukew.com

LukeW | Generative Agents

* In the center of the architecture that powers generative agents is a memory stream that maintains a record of agents' experiences in natural language. * From the memory stream, records are retrieved as relevant to the agents' cognitive processes. A retrieval function that takes the agent's current situation as input and returns a subset of the memory stream to pass to a LLM, which then generates the final output behavior of the agents. * Retrieval is a linear combination of the recency, importance, and relevance function for each piece of memory. * The importance function is a prompt that asks the large-range model for the

](https://www.lukew.com/ff/entry.asp?2030#:~:text=,range%20model%20for%20the)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.lukew.com&sz=32)lukew.com

LukeW | Generative Agents

* From the memory stream, records are retrieved as relevant to the agents' cognitive processes. A retrieval function that takes the agent's current situation as input and returns a subset of the memory stream to pass to a LLM, which then generates the final output behavior of the agents. * Retrieval is a linear combination of the recency, importance, and relevance function for each piece of memory. * The importance function is a prompt that asks the large-range model for the event status. You're basically asking the agent in natural language, this is who you are. How important is this to you?

](https://www.lukew.com/ff/entry.asp?2030#:~:text=,important%20is%20this%20to%20you)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2304.03442] Generative Agents: Interactive Simulacra of Human Behavior

conversations; they remember and reflect on days past as they plan the next day. To enable generative agents, we describe an architecture that extends a large language model to store a complete record of the agent's experiences using natural language, synthesize those memories over time into higher-level reflections, and retrieve them dynamically to plan behavior. We instantiate generative agents to populate an interactive sandbox environment inspired by The Sims, where end users can interact with a small town of twenty five agents using natural language. In an evaluation, these generative agents produce believable individual and emergent social behaviors: for example, starting with

](https://arxiv.org/abs/2304.03442#:~:text=conversations%3B%20they%20remember%20and%20reflect,behaviors%3A%20for%20example%2C%20starting%20with)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.lukew.com&sz=32)lukew.com

LukeW | Generative Agents

* Retrieval is a linear combination of the recency, importance, and relevance function for each piece of memory. * The importance function is a prompt that asks the large-range model for the event status. You're basically asking the agent in natural language, this is who you are. How important is this to you? * The relevance function clusters records of agents' memory into higher-level abstract thoughts that are called reflections. Once they are synthesized, these reflections are just a type of memory and are just stored in the memory stream

](https://www.lukew.com/ff/entry.asp?2030#:~:text=,stored%20in%20the%20memory%20stream)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.getzep.com&sz=32)getzep.com

Zep Is The New State of the Art In Agent Memory

Zep Is The New State of the Art In Agent Memory Zep is a temporal knowledge graph-based memory layer for AI agents that continuously learns from user interactions and changing business data.

](https://www.getzep.com/blog/state-of-the-art-agent-memory/#:~:text=Zep%20Is%20The%20New%20State,interactions%20and%20changing%20business%20data)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

Personalized LLM Response Generation with Parameterized User Memory Injection

from real-world bionic memory mechanism to propose a novel parameterized M emory-i njected approach using parameter-efficient fine-tuning (PEFT), combined with a Bayesian Optimisation searching strategy to achieve L LM P ersonalization(MiLP). Our MiLP takes advantage from the alignment between real- world memory mechanism and the LLM’s architecture. Extensive experiments have shown the superiority and effectiveness of MiLP. To encourage further research into this area, we are releasing our implementations^{1}^{1}1 https://github.com/MatthewKKai/MiLP.

](https://arxiv.org/html/2404.03565v2#:~:text=from%20real,1%7D1%20https%3A%2F%2Fgithub.com%2FMatthewKKai%2FMiLP)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

Personalized LLM Response Generation with Parameterized User Memory Injection

with a Bayesian Optimisation searching strategy to achieve L LM P ersonalization(MiLP). Our MiLP takes advantage from the alignment between real- world memory mechanism and the LLM’s architecture. Extensive experiments have shown the superiority and effectiveness of MiLP. To encourage further research

](https://arxiv.org/html/2404.03565v2#:~:text=with%20a%20Bayesian%20Optimisation%20searching,To%20encourage%20further%20research)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

Personalized LLM Response Generation with Parameterized User Memory Injection

context learning to organize the user historical content as prompts, providing them to LLM so that personal information can be considered (Petrov and Macdonald, 2023 ; Kang et al., 27; Liu et al., 2023 ). However, this paradigm suffers from the long-context window limitation of LLM (Liu et al., 29). Memory-based approaches provide a solution by leveraging a memory to store user historical content. When a new user query comes, a retriever will first retrieve relevant user information from the memory to prompt LLM produce personalized responses (Dalvi et al., 2022 ; Madaan et al., 31; Lewis et al., 2020 ; Zhang et al., 33).

](https://arxiv.org/html/2404.03565v2#:~:text=context%20learning%20to%20organize%20the,33)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

Personalized LLM Response Generation with Parameterized User Memory Injection

nature of similarity comparison retrieval process (Zhang et al., 2023 ). Additionally, user historical content can be complex and noisy, posing difficulties for LLMs to focus on the most relevant information without a proper learnable process. To address this, recent studies have proposed parameterizing and projecting user historical content into a learnable representation space (Ning et al., 34; Deng et al., 2022 ; Zhong et al., 36). Instead of using text to prompt LLMs, the learned user representations can be neglected in the LLM’s decoding process via cross-attention to enable personalized response generation. In this study, we take a further step by

](https://arxiv.org/html/2404.03565v2#:~:text=nature%20of%20similarity%20comparison%20retrieval,take%20a%20further%20step%20by)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

Personalized large language models (LLMs) aim to tailor interactions, content, and recommendations to individual user preferences. While parameter-efficient fine-tuning (PEFT) methods excel in performance and generalization, they are costly and limit communal benefits when used individually. To this end, we introduce PERSONALIZED PIECES (PER-PCS) 1 ,

](https://aclanthology.org/2024.emnlp-main.371.pdf#:~:text=Personalized%20large%20language%20models%20,PCS%29%201)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

and assemble personalized PEFT efficiently with collaborative efforts. PER-PCS involves selecting sharers, breaking their PEFT into pieces, and training gates for each piece. These pieces are added to a pool, from which target users can select and assemble personalized PEFT using their history data. This approach preserves privacy and enables fine-grained user modeling without excessive storage and computation demands. Experimental

](https://aclanthology.org/2024.emnlp-main.371.pdf#:~:text=and%20assemble%20personalized%20PEFT%20efficiently,Experimental)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

Efficient Interactions

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=Efficient%20Interactions)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

Secondly, by eliminating the need for customers to repeat information, the AI can respond immediately with data it already holds. Consequently, this efficiency streamlines every interaction.

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=Secondly%2C%20by%20eliminating%20the%20need,this%20efficiency%20streamlines%20every%20interaction)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.generational.pub&sz=32)generational.pub

Memory in AI Agents - by Kenn So - Generational

Memory transforms an AI from a basic question-answering tool into a conversation partner that can use pronouns and implicit references ...

](https://www.generational.pub/p/memory-in-ai-agents#:~:text=Memory%20transforms%20an%20AI%20from,pronouns%20and%20implicit%20references)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

1. E-Commerce

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=1.%20E)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

For instance, imagine your online store’s AI recommending products based on a customer’s past purchases. Moreover, it could even remember details like clothing sizes or favorite brands, thereby making shopping more convenient and tailored to individual tastes.

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=For%20instance%2C%20imagine%20your%20online,and%20tailored%20to%20individual%20tastes)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

For instance, imagine your online store’s AI recommending products based on a customer’s past purchases. Moreover, it could even remember details like clothing sizes or favorite brands, thereby making shopping more convenient and tailored to individual tastes.

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=For%20instance%2C%20imagine%20your%20online,and%20tailored%20to%20individual%20tastes)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

customer’s past purchases. Moreover, it could even remember details like clothing sizes or favorite brands, thereby making shopping more convenient and tailored to individual tastes.

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=customer%E2%80%99s%20past%20purchases,and%20tailored%20to%20individual%20tastes)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

4. Healthcare

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=4)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

2. Banking

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=2)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus.com

AI Agent Memory: Human Touch for Business Growth

3. Travel and Tourism

](https://www.qiscus.com/en/blog/ai-agent-memory/#:~:text=3)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.me.bot&sz=32)me.bot

AI-native memory for personalization & AGI - Me.bot

AI-native memory for personalization & AGI - Me.bot In the L2 System, the LLM serves as the core processor, with the context of the LLM acting as RAM and the memory system functioning as the hard ...

](https://www.me.bot/blog/ai-native-memory-for-personalization-agi#:~:text=AI,functioning%20as%20the%20hard)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

Personalized LLM Response Generation with Parameterized User Memory Injection

Incorporating user historical information properly to LLM can be a key towards LLM personalization. Existing works can be concluded into three lines as illustrated in Fig. 1 . Text-Prompt based methods draw inspiration from in- context learning to organize the user historical content as prompts, providing them to LLM so that personal information can be considered (Petrov and Macdonald, 26; Kang et al., 2023 ; Liu et al., 28). However, this paradigm suffers from the long-context window limitation of LLM (Liu et al., 2024). Memory-based approaches provide a solution by leveraging a memory to store user historical content. When a new user query comes, a

](https://arxiv.org/html/2404.03565v2#:~:text=Incorporating%20user%20historical%20information%20properly,new%20user%20query%20comes%2C%20a)

All Sources

[

langchain-ai.github

5



](https://langchain-ai.github.io/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.mem0.ai&sz=32)docs.mem0

2



](https://docs.mem0.ai/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.graphlit.com&sz=32)graphlit

](https://www.graphlit.com/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv

5



](https://arxiv.org/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium

2



](https://medium.com/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://microsoft.github.io&sz=32)microsoft.github

](https://microsoft.github.io/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://redis.io&sz=32)redis

2



](https://redis.io/)[

news.ycombinator

2



](https://news.ycombinator.com/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.cognee.ai&sz=32)cognee

](https://www.cognee.ai/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology

](https://aclanthology.org/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.lukew.com&sz=32)lukew

](https://www.lukew.com/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.qiscus.com&sz=32)qiscus

2



](https://www.qiscus.com/)[

![Favicon](https://www.google.com/s2/favicons?domain=https://www.anthropic.com&sz=32)anthropic

](https://www.anthropic.com/)
```


```
Trích dẫn

[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

BERT with History Answer Embedding for Conversational Question Answering

4.2.1 Competing Methods. We consider all the methods on the QuAC leaderboard as baselines. The competing methods are: • BiDAF++ [3]: BiDAF++ augments BiDAF [14] with self-attention and contextualized embeddings. • BiDAF++ w/ 2-Context [3]: It incorporates 2 history turns in BiDAF++ by encoding the dialog turn # in question embeddings and concatenating marker embeddings to passage embeddings. • FlowQA [7]: It considers conversation history by integrating intermediate representation generated when answering previous

](https://arxiv.org/pdf/1905.05412#:~:text=4,representation%20generated%20when%20answering%20previous)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

BERT with History Answer Embedding for Conversational Question Answering

[2] D. Chen, A. Fisch, J. Weston, and A. Bordes. Reading Wikipedia to Answer Open-Domain Questions. In ACL, 2017. [3] E. Choi, H. He, M. Iyyer, M. Yatskar, W. Yih, Y. Choi, P. Liang, and L. S. Zettlemoyer. QuAC: Question Answering in Context. In EMNLP, 2018. [4] W. B. Croft and R. H. Thompson. I3R: A new approach to the design of document retrieval systems. JASIS, 38:389–404, 1987.

](https://arxiv.org/pdf/1905.05412#:~:text=,JASIS%2C%2038%3A389%E2%80%93404%2C%201987)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

integrated memory components to track user-assistant chat histories, enabling more accurate and personalized responses. However, their long-term memory capabilities in sustained interactions remain underexplored. We introduce LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs

](https://arxiv.org/abs/2410.10813#:~:text=integrated%20memory%20components%20to%20track,context%20LLMs)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term memory design into three stages: indexing, retrieval, and reading. Built upon key experimental insights, we propose several memory design optimizations including session decomposition for value granularity, fact-augmented key

](https://arxiv.org/abs/2410.10813#:~:text=meticulously%20curated%20questions%20embedded%20within,augmented%20key)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[1410.3916] Memory Networks

> Abstract:We describe a new class of learning models called memory networks. Memory networks reason with inference components combined with a long-term memory component; they learn how to use these jointly. The long-term memory can be read and written to, with the goal of using it for prediction. We investigate these models in the context of question answering (QA) where the long-term memory effectively acts as a (dynamic) knowledge base, and the output is a textual response. We evaluate them on a large-scale QA task, and a smaller, but more complex, toy task generated from a simulated world. In the latter, we show the reasoning power of such models by chaining multiple supporting sentences to

](https://arxiv.org/abs/1410.3916#:~:text=,chaining%20multiple%20supporting%20sentences%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[1410.3916] Memory Networks

these models in the context of question answering (QA) where the long-term memory effectively acts as a (dynamic) knowledge base, and the output is a textual response. We evaluate them on a large-scale QA task, and a smaller, but more complex, toy task generated from a simulated world. In the latter, we show the reasoning power of such models by chaining multiple supporting sentences to answer questions that require understanding the intension of verbs.

](https://arxiv.org/abs/1410.3916#:~:text=these%20models%20in%20the%20context,understanding%20the%20intension%20of%20verbs)[

![Favicon](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)en.wikipedia.org

Differentiable neural computer - Wikipedia

In artificial intelligence , a differentiable neural computer (DNC) is a memory augmented 47 architecture (MANN), which is typically (but not by definition) recurrent in its implementation. The model was published in 2016 by Alex Graves et al. of 49.[ 1 ]

](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=In%20artificial%20intelligence%20%2C%20a,1)[

![Favicon](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)en.wikipedia.org

Differentiable neural computer - Wikipedia

DNC indirectly takes inspiration from Von-Neumann architecture , making it likely to outperform conventional architectures in tasks that are fundamentally algorithmic that cannot be learned by finding a 52.

](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=DNC%20indirectly%20takes%20inspiration%20from,by%20finding%20a%20%2052)[

![Favicon](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)en.wikipedia.org

Differentiable neural computer - Wikipedia

So far, DNCs have been demonstrated to handle only relatively simple tasks, which can be solved using conventional programming. But DNCs don't need to be programmed for each problem, but can instead be trained. This attention span allows the user to feed complex data structures such as 54 sequentially, and recall them for later use. Furthermore, they can learn aspects of symbolic reasoning and apply it to working memory. The researchers who published the method see promise that DNCs can be trained to perform complex, structured tasks[ 1 ][ 2 ] and address big-data applications that require some sort of reasoning, such as generating video commentaries or semantic text

](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=So%20far%2C%20DNCs%20have%20been,video%20commentaries%20or%20semantic%20text)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[1410.3916] Memory Networks

memory component; they learn how to use these jointly. The long-term memory can be read and written to, with the goal of using it for prediction. We investigate these models in the context of question answering (QA) where the long-term memory effectively acts as a (dynamic) knowledge base, and the output is a textual response. We evaluate them on a large-scale QA task, and a smaller, but more complex, toy task generated from a simulated world. In the latter, we show the reasoning power of such models by chaining multiple supporting sentences to

](https://arxiv.org/abs/1410.3916#:~:text=memory%20component%3B%20they%20learn%20how,chaining%20multiple%20supporting%20sentences%20to)[

openreview.net

Language model with Plug-in Knowldge Memory | OpenReview

of knowledge PLM needs to solve certain task. In this paper, we introduce PlugLM, a pre-training model with differentiable plug-in memory(DPM). The key intuition behind is to decouple the knowledge storage from model parameters with an editable and scalable key-value memory and leverage knowledge in an explainable manner by knowledge retrieval in the DPM. We conduct extensive experiments under various settings to justify this design choice. In domain adaptation setting, PlugLM could be easily adapted to different domains with plugable in-domain memory---obtaining 3.95 F1 improvements across four domains, without any in-domain training. PlugLM could also keep absorbing new knowledge

](https://openreview.net/forum?id=Plr5l7r0jY6#:~:text=of%20knowledge%20PLM%20needs%20to,also%20keep%20absorbing%20new%20knowledge)[

openreview.net

Language model with Plug-in Knowldge Memory | OpenReview

adaptation setting, PlugLM could be easily adapted to different domains with plugable in-domain memory---obtaining 3.95 F1 improvements across four domains, without any in-domain training. PlugLM could also keep absorbing new knowledge after pre-training is done by knowledge updating operation in the DPM without re-training. Finally, we show that by incorporating training samples into DPM with knowledge prompting, PlugLM could further be improved by the instruction of in-task knowledge.

](https://openreview.net/forum?id=Plr5l7r0jY6#:~:text=adaptation%20setting%2C%20PlugLM%20could%20be,task%20knowledge)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2005.11364] Open-Retrieval Conversational Question Answering

retrieval conversational question answering (ORConvQA) setting, where we learn to retrieve evidence from a large collection before extracting answers, as a further step towards building functional conversational search systems. We create a dataset, OR-QuAC, to facilitate research on ORConvQA. We build an end- to-end system for ORConvQA, featuring a retriever, a reranker, and a reader that are all based on Transformers. Our extensive experiments on OR-QuAC demonstrate that a learnable retriever is crucial for ORConvQA. We further show that our system can make a substantial improvement when we enable history modeling in all system components. Moreover, we show that the reranker component contributes to

](https://arxiv.org/abs/2005.11364#:~:text=retrieval%20conversational%20question%20answering%20,the%20reranker%20component%20contributes%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2005.11364] Open-Retrieval Conversational Question Answering

passage. These simplifications neglect the fundamental role of retrieval in conversational search. To address this limitation, we introduce an open- retrieval conversational question answering (ORConvQA) setting, where we learn to retrieve evidence from a large collection before extracting answers, as a further step towards building functional conversational search systems. We create a dataset, OR-QuAC, to facilitate research on ORConvQA. We build an end- to-end system for ORConvQA, featuring a retriever, a reranker, and a reader that are all based on Transformers. Our extensive experiments on OR-QuAC demonstrate that a learnable retriever is crucial for ORConvQA. We further show that our

](https://arxiv.org/abs/2005.11364#:~:text=passage,We%20further%20show%20that%20our)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2005.11364] Open-Retrieval Conversational Question Answering

to-end system for ORConvQA, featuring a retriever, a reranker, and a reader that are all based on Transformers. Our extensive experiments on OR-QuAC demonstrate that a learnable retriever is crucial for ORConvQA. We further show that our system can make a substantial improvement when we enable history modeling in all system components. Moreover, we show that the reranker component contributes to

](https://arxiv.org/abs/2005.11364#:~:text=to,the%20reranker%20component%20contributes%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

interlocutors revealed in the previous conversation is abstractively summarized and stored in memory. Specifically, the memory management mechanism decides which information to keep in memory. For this purpose, we define four pairwise operations (PASS, REPLACE, APPEND, and DELETE) to find and eliminate the information that can cause confusion or redundancy in later conversations. For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=interlocutors%20revealed%20in%20the%20previous,in%02coming%20summary%20is%20%E2%80%9CJust%20got)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got positive results from COVID test”, the two sentences are contradictory, in which the former needs to be replaced in memory by the latter. Through this process, only valid information remains in new memory. Then, in subsequent sessions, a relevant information from this memory is retrieved and given as additional condition for generating chatbot

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=For%20example%2C%20if%20the%20previous,additional%20condi%02tion%20for%20generating%20chatbot)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

Specifically, the memory management mechanism decides which information to keep in memory. For this purpose, we define four pairwise operations (PASS, REPLACE, APPEND, and DELETE) to find and eliminate the information that can cause confusion or redundancy in later conversations. For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got positive results from

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=Specifically%2C%20the%20memory%20management%20mechanism,%E2%80%9CJust%20got%20positive%20results%20from)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

find and eliminate the information that can cause confusion or redundancy in later conversations. For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got positive results from COVID test”, the two sentences are contradictory, in which the former needs to be replaced in memory by the latter. Through this process, only valid information remains in new memory. Then, in subsequent sessions, a relevant

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=find%20and%20eliminate%20the%20information,in%20sub%02sequent%20sessions%2C%20a%20relevant)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

With extensive experiments and ablations, we show that the proposed memory management mechanism becomes more advantageous in terms of memorability as the sessions proceed, leading to better engagingness and humanness in multisession dialogues. Our contributions are as follows: 1. We make a step towards long-term conversations with dynamic memory that must be kept up-to-date.

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=With%20extensive%20experiments%20and%20ablations%2C,date)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2308.15022] Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

long conversation, these chatbots fail to recall past information and tend to generate inconsistent responses. To address this, we propose to recursively generate summaries/ memory using large language models (LLMs) to enhance long- term memory ability. Specifically, our method first stimulates LLMs to memorize small dialogue contexts and then recursively produce new memory using previous memory and following contexts. Finally, the chatbot can easily generate a highly consistent response with the help of the latest memory. We evaluate our method on both open and closed LLMs, and the experiments on the widely-used public dataset show that our method can generate more consistent responses in a long-

](https://arxiv.org/abs/2308.15022#:~:text=long%20conversation%2C%20these%20chatbots%20fail,consistent%20responses%20in%20a%20long)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2308.15022] Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

consistent response with the help of the latest memory. We evaluate our method on both open and closed LLMs, and the experiments on the widely-used public dataset show that our method can generate more consistent responses in a long- context conversation. Also, we show that our strategy could nicely complement both long-context (e.g., 8K and 16K) and retrieval-enhanced LLMs, bringing further long-term dialogue performance. Notably, our method is a potential solution to enable the LLM to model the extremely long context. The code and scripts will be released later.

](https://arxiv.org/abs/2308.15022#:~:text=consistent%20response%20with%20the%20help,scripts%20will%20be%20released%20later)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

To deliver coherent and personalized experiences in long-term conversations, existing approaches typically perform retrieval augmented response generation by constructing memory banks from conversation history at either the turn-level, session-level, or through summarization techniques. In this paper, we present two key findings: (1) The granularity of memory unit matters: Turn-level, session-level, and summarization-based methods each exhibit limitations in both memory retrieval accuracy and the semantic quality of the retrieved content. (2) Prompt compression methods, such as LLMLingua-2, can effectively serve as a denoising mechanism, enhancing memory retrieval accuracy across different granularities.

](https://arxiv.org/html/2502.05589v2#:~:text=To%20deliver%20coherent%20and%20personalized,retrieval%20accuracy%20across%20different%20granularities)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

Building on these insights, we propose SeCom, a method that constructs the memory bank at segment level by introducing a conversation Se gmentation model that partitions long-term conversations into topically coherent segments, while applying Com pression based denoising on memory units to enhance memory retrieval. Experimental results show that SeCom exhibits a significant performance advantage over baselines on long-term conversation benchmarks LOCOMO and Long-MT-Bench+. Additionally, the proposed conversation segmentation method demonstrates superior performance on dialogue segmentation datasets such as DialSeg711, TIAGE, and SuperDialSeg.

](https://arxiv.org/html/2502.05589v2#:~:text=Building%20on%20these%20insights%2C%20we,as%20DialSeg711%2C%20TIAGE%2C%20and%20SuperDialSeg)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

showing a 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term memory design into three stages: indexing, retrieval, and reading. Built upon key experimental insights, we propose several memory design optimizations including session decomposition for value granularity, fact-augmented key expansion for indexing, and time-aware query expansion for refining the search scope. Extensive experiments show that these optimizations greatly improve both memory recall and downstream question answering on LongMemEval. Overall, our study provides valuable resources and guidance for advancing the long-term

](https://arxiv.org/abs/2410.10813#:~:text=showing%20a%2030,term)[

![Favicon](https://www.google.com/s2/favicons?domain=https://ar5iv.labs.arxiv.org&sz=32)ar5iv.labs.arxiv.org

[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory

personality over time by synthesizing information from previous interactions. To mimic anthropomorphic behaviors and selectively preserve memory, MemoryBank incorporates a memory updating mechanism, inspired by the Ebbinghaus Forgetting Curve theory. This mechanism permits the AI to forget and reinforce memory based on time elapsed and the relative significance of the memory, thereby offering a more human-like memory mechanism and enriched user experience. MemoryBank is versatile in accommodating both closed-source models like ChatGPT and open- source models such as ChatGLM. To validate MemoryBank’s effectiveness, we exemplify its application through the creation of an LLM-based chatbot named

](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=personality%20over%20time%20by%20synthesizing,based%20chatbot%20named)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

Memory Updating

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Updating)[

![Favicon](https://www.google.com/s2/favicons?domain=https://ar5iv.labs.arxiv.org&sz=32)ar5iv.labs.arxiv.org

[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory

psychological counseling, and secretarial assistance. Recognizing the necessity for long-term memory, we propose MemoryBank, a novel memory mechanism tailored for LLMs. MemoryBank enables the models to summon relevant memories, continually evolve through continuous memory updates, comprehend, and adapt to a user’s personality over time by synthesizing information from previous interactions. To mimic anthropomorphic behaviors and selectively preserve memory, MemoryBank incorporates a memory updating mechanism, inspired by the Ebbinghaus Forgetting Curve theory. This mechanism permits the AI to forget and reinforce memory based on time elapsed and the relative significance of the memory, thereby offering a

](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=psychological%20counseling%2C%20and%20secretarial%20assistance,the%20memory%2C%20thereby%20offering%20a)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

* Selective Forgetting: Drawing inspiration from the Ebbinghaus Forgetting Curve, MemoryBank ensures that not all stored memories remain equally strong. Over time, if a memory isn’t recalled or reinforced, its strength decays and it may eventually be pruned from active storage. This selective forgetting keeps the memory bank relevant and uncluttered. * Reinforcement of Key Memories: Conversely, memories that are frequently accessed are reinforced. Each time a memory is recalled, its “strength” is boosted, ensuring that important details persist over longer periods — mirroring how human memory works through repeated retrieval.

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=,memory%20works%20through%20repeated%20retrieval)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management

to improve retrieval quality, we argue that such memories provide rich, important contextual cues for RG (e.g., changes in user behaviors) in long-term conversations. We present THEANINE, a framework for LLM-based lifelong dialogue agents. THEANINE discards memory removal and manages large-scale memories by linking them based on their temporal and cause-effect relation. Enabled by this linking structure, THEANINE augments RG with memory timelines - series of memories representing the evolution or causality of relevant past events. Along with THEANINE, we introduce TeaFarm, a counterfactual-driven evaluation scheme, addressing the limitation of G-Eval and human efforts when assessing agent

](https://arxiv.org/abs/2406.10996#:~:text=to%20improve%20retrieval%20quality%2C%20we,human%20efforts%20when%20assessing%20agent)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management

constantly memorize perceived information and properly retrieve it for response generation (RG). While prior studies focus on getting rid of outdated memories to improve retrieval quality, we argue that such memories provide rich, important contextual cues for RG (e.g., changes in user behaviors) in long-term conversations. We present THEANINE, a framework for LLM-based lifelong dialogue agents. THEANINE discards memory removal and manages large-scale memories by linking them based on their temporal and cause-effect relation. Enabled by this linking structure, THEANINE augments RG with memory timelines - series of memories representing the evolution or causality of relevant past events. Along

](https://arxiv.org/abs/2406.10996#:~:text=constantly%20memorize%20perceived%20information%20and,Along)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management

conversations. We present THEANINE, a framework for LLM-based lifelong dialogue agents. THEANINE discards memory removal and manages large-scale memories by linking them based on their temporal and cause-effect relation. Enabled by this linking structure, THEANINE augments RG with memory timelines - series of memories representing the evolution or causality of relevant past events. Along with THEANINE, we introduce TeaFarm, a counterfactual-driven evaluation scheme, addressing the limitation of G-Eval and human efforts when assessing agent

](https://arxiv.org/abs/2406.10996#:~:text=conversations,human%20efforts%20when%20assessing%20agent)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue

the Long-term Dialogue Agent (LD-Agent), which incorporates three independently tunable modules dedicated to event perception, persona extraction, and response generation. For the event memory module, long and short-term memory banks are employed to separately focus on historical and ongoing sessions, while a topic- based retrieval mechanism is introduced to enhance the accuracy of memory retrieval. Furthermore, the persona module conducts dynamic persona modeling for both users and agents. The integration of retrieved memories and extracted personas is subsequently fed into the generator to induce appropriate responses. The effectiveness, generality, and cross-domain capabilities of LD-Agent are

](https://arxiv.org/abs/2406.05925#:~:text=the%20Long,Agent%20are)[

openreview.net

200 The event memory module is designed to perceive 201 historical events to generate coherent responses 202 across interval time. As shown in Figure 2, this 203 event memory module is segmented into two major 204 sub-modules that focus separately on long-term 205 and short-term memory. 206 2.2.1 Long-term Memory 207 Memory Storage. The long-term memory mod208 ule aims to extract and encode events from past 209 sessions. Specifically, this involves recording

](https://openreview.net/pdf?id=lwCxVgVYoK#:~:text=200%20The%20event%20memory%20module,Specifically%2C%20this%20involves%20recording)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue

generation. For the event memory module, long and short-term memory banks are employed to separately focus on historical and ongoing sessions, while a topic- based retrieval mechanism is introduced to enhance the accuracy of memory retrieval. Furthermore, the persona module conducts dynamic persona modeling for both users and agents. The integration of retrieved memories and extracted personas is subsequently fed into the generator to induce appropriate responses. The effectiveness, generality, and cross-domain capabilities of LD-Agent are empirically demonstrated across various illustrative benchmarks, models, and

](https://arxiv.org/abs/2406.05925#:~:text=generation,various%20illustrative%20benchmarks%2C%20models%2C%20and)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

Memory Storage: The Warehouse of Memories

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Storage%3A%20The%20Warehouse%20of,Memories)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

level overviews of daily events and key interactions, much like how humans remember “the gist” of an experience rather than every minute detail. * User Portraits: Beyond mere conversation logs, MemoryBank constructs dynamic user portraits. These profiles encapsulate a user’s personality traits, recurring preferences, and evolving interests, enabling the LLM to tailor its responses over time.

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=level%20overviews%20of%20daily%20events,tailor%20its%20responses%20over%20time)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

* User Portraits: Beyond mere conversation logs, MemoryBank constructs dynamic user portraits. These profiles encapsulate a user’s personality traits, recurring preferences, and evolving interests, enabling the LLM to tailor its responses over time.

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=,tailor%20its%20responses%20over%20time)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

capabilities in sustained interactions remain underexplored. We introduce LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained

](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,on%20memorizing%20information%20across%20sustained)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

capabilities in sustained interactions remain underexplored. We introduce LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term

](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,term)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

interactions. We then present a unified framework that breaks down the long-term memory design into three stages: indexing, retrieval, and reading. Built upon key experimental insights, we propose several memory design optimizations including session decomposition for value granularity, fact-augmented key expansion for indexing, and time-aware query expansion for refining the search scope. Extensive experiments show that these optimizations greatly improve both memory recall and downstream question answering on LongMemEval. Overall, our study provides valuable resources and guidance for advancing the long-term

](https://arxiv.org/abs/2410.10813#:~:text=interactions,term)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

(i) LOCOMO (Maharana et al., 2024), which is the longest conversation dataset to date, with an average of 300 turns with 9K tokens per sample. For the test set, we prompt GPT-4 to generate QA pairs for each session as in Alonso et al. (2024). We also conduct evaluation on the recently released official

](https://arxiv.org/html/2502.05589v2#:~:text=%28i%29%20LOCOMO%C2%A0%28Maharana%20et%C2%A0al,on%20the%20recently%20released%20official)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

long-conversation benchmark LOCOMO. Interestingly, there is a significant performance disparity in Turn-Level and Session-Level methods when using different retrieval models. For instance, switching from the MPNet-based retriever to the BM25-based retriever results in performance improvements up to

](https://arxiv.org/html/2502.05589v2#:~:text=long,in%20performance%20improvements%20up%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

Methods LOCOMO Long-MT-Bench+ GPT4Score BLEU Rouge2 BERTScore GPT4Score BLEU Rouge2 BERTScore SeCom 69.33 7.19 13.74 88.60 88.81 13.80 19.21 87.72 Denoise 59.87 6.49 12.11 88.16 87.51 12.94 18.73 87.44

](https://arxiv.org/html/2502.05589v2#:~:text=Methods%20LOCOMO%20Long,44)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

match at L389 LOCOMO Zero History 24.86 1.94 17.36 3.72 13.24 85.83 0.00 0 Full History 54.15 6.26 27.20 12.07 22.39 88.06 210.34 13,330 Turn-Level (MPNet) 57.99 6.07 26.61 11.38 21.60 88.01 54.77 3,288

](https://arxiv.org/html/2502.05589v2#:~:text=match%20at%20L389%20LOCOMO%20Zero,77%203%2C288)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

LOCOMO Zero History 24.86 1.94 17.36 3.72 13.24 85.83 0.00 0 Full History 54.15 6.26 27.20 12.07 22.39 88.06 210.34 13,330 Turn-Level (MPNet) 57.99 6.07 26.61 11.38 21.60 88.01 54.77 3,288

](https://arxiv.org/html/2502.05589v2#:~:text=LOCOMO%20Zero%20History%2024,77%203%2C288)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

3.2 Dataset Construction To study this task, we build a new dataset based on CareCall dataset2(Bae et al., 2022), which consists of single sessions of open-domain dialogues between bots and users. We choose this dataset because the sessions contain various topics that are likely to change in a short period of time, such as user’s health, sleep, and diet, as well as those in a relatively longer period of time, such as family, pets, and frequently visited places. We extend this

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=3,We%20extend%20this)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

single-session dataset to a multi-session setting, which is a similar procedure presented in MSC (Xu et al., 2022a). Our resulting dataset contains more persona updates than other datasets (Xu et al., 2 https://github.com/naver-ai/carecall-corpus Statistics Sessions 7,665 Session 1 2,812

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=single,Sessions%207%2C665%20Session%201%202%2C812)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

Query Rewriting

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Query%20Rewriting)
```