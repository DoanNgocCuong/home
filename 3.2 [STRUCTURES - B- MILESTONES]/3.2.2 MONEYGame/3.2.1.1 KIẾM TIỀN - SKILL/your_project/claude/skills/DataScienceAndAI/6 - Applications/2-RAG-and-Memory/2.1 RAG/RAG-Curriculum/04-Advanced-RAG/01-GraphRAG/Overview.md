# GraphRAG: Knowledge Graph Enhanced Retrieval

## Tổng Quan

GraphRAG là approach của Microsoft kết hợp knowledge graphs với RAG. Thay vì flat documents, bạn extract ra một knowledge graph (entities, relationships, communities), sau đó retrieve dựa trên graph structure.

**Khi nào dùng:** Complex domain knowledge, multi-hop reasoning, entity relationships.
**Khi nào skip:** Simple Q&A, large unstructured data, limited budget.

## Vanilla RAG vs GraphRAG

```
Vanilla RAG:
Document 1: "Alice works at Company X..."
Document 2: "Company X was founded in 2020..."
            ↓
     Vector Search
            ↓
     Retrieve top-10 documents
            ↓
     Send to LLM
            ✗ Misses relationships between documents

GraphRAG:
Extracted Graph:
  Entities: Alice, Company X, 2020
  Relationships: Alice-[WORKS_AT]→Company X
                 Company X-[FOUNDED]→2020
  Communities: [Alice, Company X], [Company X Timeline]
            ↓
  Query: "Who founded Company X?"
            ↓
  Graph Traversal: Find nodes connected to "Company X" via FOUNDED
            ↓
  Retrieve relevant community context
            ↓
  Send to LLM with rich context
            ✓ Explicitly models relationships
```

## GraphRAG Architecture

```
┌─────────────────────────────────────────────────┐
│  Step 1: Graph Extraction                      │
│  (LLM extracts entities & relationships)       │
│                                                 │
│  Documents → LLM → (Entity, Relation) pairs   │
│  "Alice works at Company X"                   │
│  → (Alice, WORKS_AT, Company X)               │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│  Step 2: Graph Construction                    │
│  (Build knowledge graph)                        │
│                                                 │
│  Graph DB (Neo4j, ArangoDB)                    │
│     ╱───── Alice                               │
│    ╱      ╱   \                                │
│  WORKS_AT     MANAGES                          │
│    \        ╱                                  │
│     Company X                                  │
│           \                                    │
│        FOUNDED_AT                              │
│             \                                  │
│             2020                               │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│  Step 3: Community Detection                    │
│  (Identify communities via clustering)          │
│                                                 │
│  Community 1: {Alice, Company X} (People & Orgs)
│  Community 2: {Company X, 2020} (Timeline)    │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│  Step 4: Query-Time Retrieval                   │
│  (Retrieve relevant community + context)        │
│                                                 │
│  Query: "Who founded Company X?"               │
│  → Find "Company X" entity                     │
│  → Retrieve its communities                    │
│  → Get related entities & relationships        │
│  → Summarize for LLM                          │
└─────────────────────────────────────────────────┘
```

## Implementation Example

```python
from llama_index.graph_stores import Neo4jGraphStore
from llama_index import KnowledgeGraphIndex
from llama_index.llms import OpenAI

# Setup Neo4j connection
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
    database="neo4j"
)

# Create KG index (extracts entities & relationships)
llm = OpenAI(model="gpt-4")
kg_index = KnowledgeGraphIndex.from_documents(
    documents=documents,
    graph_store=graph_store,
    llm=llm,
    include_embeddings=True
)

# Query using graph + retrieval
query_engine = kg_index.as_query_engine(
    retriever_mode="hybrid",  # Graph + vector search
    retriever="kg_embedding"
)

# Multi-hop reasoning
response = query_engine.query("What is Alice's role at Company X?")
```

## Entity Extraction with LLM

```python
from pydantic import BaseModel, Field
from typing import List

class Entity(BaseModel):
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type (PERSON, ORG, LOCATION, etc)")

class Relationship(BaseModel):
    source: str = Field(description="Source entity")
    relation: str = Field(description="Relationship type (WORKS_AT, OWNS, etc)")
    target: str = Field(description="Target entity")

class GraphExtractionResult(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

# Use LLM with structured output
extraction_prompt = """Extract entities and relationships from this text.

Text: {text}

Entities: Name, Type (PERSON, ORG, LOCATION, EVENT, etc)
Relationships: Source, Relation, Target

Return as JSON."""

from llama_index.llms import OpenAI

llm = OpenAI(model="gpt-4")
result = llm.structured_predict(
    GraphExtractionResult,
    extraction_prompt.format(text="Alice works at Company X, which was founded in 2020.")
)

# Save to graph database
for entity in result.entities:
    graph_store.add_node(entity.name, entity_type=entity.type)

for rel in result.relationships:
    graph_store.add_relation(rel.source, rel.relation, rel.target)
```

## Community Detection for Hierarchical Retrieval

```python
import networkx as nx
from community import community_louvain

# Convert graph to NetworkX
G = nx.Graph()
for node in graph_store.get_nodes():
    G.add_node(node.name)

for rel in graph_store.get_relations():
    G.add_edge(rel.source, rel.target, relation_type=rel.relation)

# Detect communities using Louvain algorithm
communities = community_louvain.best_partition(G)

# Group nodes by community
community_groups = {}
for node, community_id in communities.items():
    if community_id not in community_groups:
        community_groups[community_id] = []
    community_groups[community_id].append(node)

# Summarize each community
for community_id, nodes in community_groups.items():
    # Get edges within community
    edges = [(u, v) for u, v in G.edges() if u in nodes and v in nodes]

    # Summarize context
    summary = summarize_community(nodes, edges)
    graph_store.add_community(community_id, summary)

def summarize_community(nodes: List[str], edges: List[tuple]) -> str:
    """Summarize a community with LLM"""
    context = f"Entities: {', '.join(nodes)}\n"
    context += "Relationships:\n"
    for u, v in edges:
        context += f"  {u} -- {v}\n"

    summary_prompt = f"""Summarize this community in 2-3 sentences:
{context}"""

    summary = llm.complete(summary_prompt)
    return summary.text
```

## Query-Time Multi-Hop Retrieval

```python
def graphrag_retrieve(query: str, hop_limit: int = 2):
    """Retrieve using multi-hop graph traversal"""

    # Step 1: Find entities mentioned in query
    entities = extract_entities(query)  # ["Company X", "Alice"]

    # Step 2: Multi-hop expansion
    retrieved_context = []
    visited = set()

    def traverse(entity, hops_remaining):
        if entity in visited or hops_remaining == 0:
            return

        visited.add(entity)

        # Get entity details
        entity_data = graph_store.get_node(entity)
        retrieved_context.append(entity_data)

        # Get related entities
        relations = graph_store.get_relations_for_entity(entity)
        for rel in relations:
            traverse(rel.target, hops_remaining - 1)

    # Start traversal from query entities
    for entity in entities:
        traverse(entity, hop_limit)

    # Step 3: Retrieve community summaries
    communities = get_communities_for_entities(entities)
    for community in communities:
        retrieved_context.append(community.summary)

    return retrieved_context

# Use in query
context = graphrag_retrieve("Who founded Company X?", hop_limit=2)
response = llm.complete(f"Based on context: {context}\n\nQuestion: Who founded Company X?")
```

## When to Use GraphRAG

**Good use cases:**
- Enterprise knowledge bases (org charts, employee relationships)
- Scientific papers (citations, methodology relationships)
- Medical data (conditions, treatments, interactions)
- Financial data (companies, investments, ownership)
- Knowledge bases with explicit entity relationships

**Poor use cases:**
- News articles (flat narrative, few relationships)
- General Q&A (Wikipedia-style)
- When you have <1000 documents
- When relationships are fuzzy/implicit

## Complexity vs Vanilla RAG

```
Setup Complexity:
  Vanilla RAG:       1 day (vector DB)
  GraphRAG:          1 week (KB, extraction, community detection)

Maintenance:
  Vanilla RAG:       Low (reindex documents)
  GraphRAG:          Medium (update graph, recompute communities)

Query Latency:
  Vanilla RAG:       50-150ms (vector search)
  GraphRAG:          100-300ms (graph traversal + retrieval)

Quality Improvement:
  Vanilla RAG:       Baseline
  GraphRAG:          +15-30% for relationship queries
                     +0-5% for simple factual queries
```

## Key Takeaway

GraphRAG adds richness by modeling relationships explicitly, making it excellent for:
1. Multi-hop reasoning (find indirect connections)
2. Entity-centric queries (what do we know about X?)
3. Relationship exploration (how are A and B connected?)

**But:** Don't use if your documents don't have clear entities/relationships.

**Best practice:** Start with vanilla RAG. Graduate to GraphRAG only when:
- Queries require multi-hop reasoning
- RAGAS recall score < 0.75 despite optimizations
- Your domain has rich entity relationships

**Time to ROI:** 2-3 weeks of development, payoff when handling complex queries better than competitors.
