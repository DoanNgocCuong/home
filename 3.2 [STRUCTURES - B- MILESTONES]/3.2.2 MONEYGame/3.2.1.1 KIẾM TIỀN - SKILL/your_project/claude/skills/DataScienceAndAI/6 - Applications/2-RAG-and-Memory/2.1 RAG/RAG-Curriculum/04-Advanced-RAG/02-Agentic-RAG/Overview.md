# Agentic RAG: LLM-as-Agent for Complex Queries

## Tổng Quan

Agentic RAG sử dụng LLM không chỉ để generate response, mà để **orchestrate retrieval process**. LLM becomes the agent - nó quyết định:
- Cần retrieve gì?
- Cần refine query thế nào?
- Có cần gọi external tools không?
- Có đủ info để trả lời chưa?

**Game changer:** Queries không cần optimal phrasing - agent handles complex reasoning.

## Vanilla RAG vs Agentic RAG

```
Vanilla RAG:
User Query
    ↓
[Fixed Pipeline] → Retrieve → Generate → Response
                  (one-shot, no adaptation)

Agentic RAG (A-RAG):
User Query
    ↓
LLM thinks: "What do I need to answer this?"
    ├─ If need context: Call retriever
    ├─ If need calculation: Call calculator tool
    ├─ If need external API: Call API tool
    ├─ Iterate until satisfied
    ↓
Generate final response
    ↓
Response
(adaptive, multi-step reasoning)
```

## Agentic RAG Framework (Feb 2026)

Recent papers (Feb 2026) show A-RAG outperforms vanilla RAG:

```
Benchmark: HotpotQA (complex reasoning)

Vanilla RAG:
  ├─ Hybrid search + reranking: 58% accuracy
  └─ Latency: 200ms

A-RAG (with self-reflection):
  ├─ Step 1: LLM analyzes query
  ├─ Step 2: Decide retrieval strategy
  ├─ Step 3: Retrieve + evaluate sufficiency
  ├─ Step 4: If insufficient, refine query
  ├─ Step 5: Generate final answer
  └─ Accuracy: 72% (+24%)
  └─ Latency: 800ms

Trade-off: +24% accuracy but 4x latency
```

## Implementation: ReAct Pattern (Reasoning + Acting)

ReAct (Reasoning + Acting) is the standard pattern for agentic RAG:

```python
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI

# Define tools
tools = [
    retriever_tool,      # Search knowledge base
    calculator_tool,     # Math operations
    search_tool,         # External search API
    extraction_tool      # Extract info from docs
]

# Create agent
agent = ReActAgent.from_tools(
    tools=tools,
    llm=OpenAI(model="gpt-4"),
    verbose=True  # See reasoning chain
)

# Query
response = agent.chat("What is the market cap of Company X in 2024?")
```

## Step-by-Step: How Agentic RAG Works

```
1. LLM Analyzes Query
   Input: "What was Company X's revenue in 2023 compared to 2022?"
   Thought: "This requires finding 2 financial metrics."

2. Plan Actions
   Plan:
     1. Retrieve 2023 annual report
     2. Extract 2023 revenue
     3. Retrieve 2022 annual report
     4. Extract 2022 revenue
     5. Calculate difference
     6. Format answer

3. Execute First Action
   Action: retrieve("Company X 2023 annual report")
   Observation: [Retrieved document with 2023 data]
   Thought: "Found 2023 revenue = $5B. Now need 2022."

4. Execute Next Action
   Action: retrieve("Company X 2022 annual report")
   Observation: [Retrieved document with 2022 data]
   Thought: "Found 2022 revenue = $4B. Can calculate diff."

5. Execute Calculation
   Action: calculate(5000000000 - 4000000000)
   Observation: $1000000000
   Thought: "100% growth. Have all info needed."

6. Generate Final Response
   "Company X revenue grew from $4B in 2022 to $5B in 2023,
   a 25% increase."

7. Return to User
   Response with chain-of-thought visible
```

## Code Example: Multi-Step Agent

```python
from llama_index import VectorStoreIndex, Document
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI

# Create separate indices for different document types
company_docs = [Document(text=doc) for doc in company_documents]
financial_docs = [Document(text=doc) for doc in financial_documents]

company_index = VectorStoreIndex.from_documents(company_docs)
financial_index = VectorStoreIndex.from_documents(financial_docs)

# Create tools from indices
tools = [
    QueryEngineTool(
        query_engine=company_index.as_query_engine(),
        metadata=ToolMetadata(
            name="company_search",
            description="Search company information, org structure, products"
        )
    ),
    QueryEngineTool(
        query_engine=financial_index.as_query_engine(),
        metadata=ToolMetadata(
            name="financial_search",
            description="Search financial data, revenues, profits, costs"
        )
    )
]

# Create agent
agent = ReActAgent.from_tools(
    tools=tools,
    llm=OpenAI(model="gpt-4"),
    max_iterations=10,  # Prevent infinite loops
    verbose=True
)

# Complex query requiring multiple steps
response = agent.chat(
    "Compare Company X's revenue growth to Company Y's growth over the last 3 years"
)

# Output shows chain-of-thought:
# Thought: "Need to compare 2 companies over 3 years..."
# Action: company_search("Company X revenue 2021-2023")
# Observation: "Company X revenue: 2021=$2B, 2022=$4B, 2023=$5B"
# Action: company_search("Company Y revenue 2021-2023")
# Observation: "Company Y revenue: 2021=$3B, 2022=$3.5B, 2023=$3.8B"
# Thought: "Have data, can compare..."
# Final Response: "Company X grew 150% while Company Y grew 26%..."
```

## Self-Correction in Agentic RAG

Agent can evaluate its own answers and retry:

```python
class SelfCorrectingAgent:
    def __init__(self, agent, llm):
        self.agent = agent
        self.llm = llm

    async def query_with_correction(self, question: str, max_attempts: int = 3):
        """Query with self-correction loop"""

        for attempt in range(max_attempts):
            # Get answer
            answer = self.agent.chat(question)

            # Self-evaluate
            evaluation = self.llm.complete(f"""
            Question: {question}
            Answer: {answer}

            Does this answer directly address the question?
            Rate: 1-5 (1=completely wrong, 5=perfect)
            If <5, what's missing?
            """)

            if evaluation.score >= 4:
                return answer

            # If poor quality, agent tries again with feedback
            refined_question = f"""{question}

            Previous attempt didn't fully address it. Issues: {evaluation.issues}
            Try again, being more specific about..."""

            self.agent.chat(refined_question)

        return answer
```

## Tool Use: Extending Agent Capabilities

```python
from typing import List
from llama_index.tools import BaseTool

class ExcelExtractionTool(BaseTool):
    """Extract data from Excel files"""

    def __call__(self, filename: str, sheet: str, query: str) -> str:
        import pandas as pd

        df = pd.read_excel(filename, sheet_name=sheet)
        # Use pandas query or LLM to extract info
        return str(df.query(query))

class CalculatorTool(BaseTool):
    """Perform calculations"""

    def __call__(self, expression: str) -> str:
        try:
            result = eval(expression)
            return str(result)
        except:
            return "Invalid expression"

class WebSearchTool(BaseTool):
    """Search web for current info"""

    def __call__(self, query: str) -> str:
        # Call Serper, Google, or similar
        results = web_search(query)
        return "\n".join([r["snippet"] for r in results[:3]])

# Add to agent
tools = [
    ExcelExtractionTool(),
    CalculatorTool(),
    WebSearchTool()
]

agent = ReActAgent.from_tools(tools=tools, llm=llm)
```

## When to Upgrade from Vanilla to Agentic

**Upgrade if:**
- Queries require multiple retrieval steps
- Questions have complex reasoning chains
- Need dynamic tool use (calc, search, extraction)
- User satisfaction < 70% on complex queries

**Don't upgrade if:**
- 90%+ of queries are simple factual lookup
- Latency < 300ms is hard requirement
- Dataset is small/simple

## Latency vs Accuracy Trade-off

```
System          Accuracy    Latency    Cost
────────────────────────────────────────────
Vanilla RAG     68%         150ms      $0.005
Vanilla + ReRank 75%        250ms      $0.010
Agentic RAG     80%         800ms      $0.030

Recommendation by use case:
- Customer support (high uptime, fast): Vanilla + ReRank
- Research (accuracy > speed): Agentic RAG
- Hybrid: Use vanilla for simple, agent for complex
```

## Hybrid Approach: Route Simple vs Complex

```python
def should_use_agentic(query: str) -> bool:
    """Decide whether to use agent or vanilla RAG"""

    # Quick heuristics
    question_words = ["how", "why", "compare", "what if"]
    if any(word in query.lower() for word in question_words):
        return True  # Likely needs reasoning

    if len(query.split()) > 10:
        return True  # Complex query

    return False  # Simple query

# Router
if should_use_agentic(user_query):
    response = agentic_agent.chat(user_query)
else:
    response = vanilla_rag.query(user_query)
```

## Key Takeaway

**Agentic RAG = LLM-as-Orchestrator, not just generator.**

When to use:
- Complex, multi-step questions
- Need dynamic tool selection
- Accuracy > latency tradeoff acceptable

Key differences from vanilla:
1. **LLM plans** - Decides retrieval strategy
2. **Iteration** - Refines queries based on results
3. **Self-correction** - Evaluates answer quality
4. **Tool use** - Calls external APIs/tools

**Setup:**
- Choose ReAct or similar framework
- Define clear tools for agent
- Set max_iterations to prevent infinite loops
- Monitor token usage (agents use 3-5x more)

**Timeline:** 3-5 days to implement. 2-3x latency cost but +15-20% accuracy. Worth it for high-complexity domains.
