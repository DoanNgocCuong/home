<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# agent design system

Perfect! Em sẽ build **Agent Design System** chi tiết cho anh em - một framework hoàn chỉnh để thiết kế agents ở level production.

***

# AGENT DESIGN SYSTEM: Complete Framework

!

![Agent Design System Architecture: Complete Framework for Building Production-Grade AI Agents](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/b51cb9f4e9d902c6f2060f45644c73c4/d091596c-8920-4a20-8d78-df87107db8f8/98726233.png)

Agent Design System Architecture: Complete Framework for Building Production-Grade AI Agents

***

## I. CORE LAYERS (4 Tầng Cơ Bản)

### **LAYER 1: PERCEPTION (Input Processing)**

```
┌─────────────────────────────────────────────────────┐
│ PERCEPTION LAYER: Understand User Intent            │
└─────────────────────────────────────────────────────┘

INPUT TYPES:
├─ Natural Language
│  ├─ "Research AAPL Q3 10-K"
│  ├─ "Compare AAPL vs GOOGL on margin"
│  └─ "Flag high-risk positions in my portfolio"
│
├─ Structured Data
│  ├─ JSON: {ticker: "AAPL", action: "research"}
│  ├─ CSV: Portfolio data upload
│  └─ API: Real-time stream
│
└─ Multi-modal
   ├─ Image: Screenshot of chart
   ├─ Audio: Voice command
   └─ Document: PDF upload

┌──────────────────────────────────────────┐
│ PARSING PIPELINE                         │
├──────────────────────────────────────────┤
│                                          │
│ 1. Input Validation                      │
│    ✓ Format check                        │
│    ✓ Schema validation                   │
│    ✓ Size limits                         │
│                                          │
│ 2. Intent Recognition                    │
│    • NLU model: What does user want?     │
│    • Action classification               │
│    • Parameter extraction                │
│                                          │
│ 3. Context Augmentation                  │
│    • User profile (tier, history)        │
│    • Portfolio context (if relevant)     │
│    • Market state (current time, prices) │
│                                          │
│ 4. Enrichment                            │
│    • Ticker resolution (AAPL → 0000320193) │
│    • Date normalization                  │
│    • Ambiguity resolution                │
│                                          │
└──────────────────────────────────────────┘

OUTPUT: Standardized Request Object
{
  user_id: "uuid-xxx",
  request_id: "uuid-yyy",
  action: "RESEARCH",
  ticker: "AAPL",
  quarter: "Q3",
  parameters: {
    include_news: true,
    include_peers: true,
    output_format: "pdf"
  },
  context: {
    user_tier: "PRO",
    portfolio_value: "$1.2M",
    has_position: true,
    position_size: "$50K"
  }
}
```


***

### **LAYER 2: REASONING (Planning \& Decision)**

```
┌─────────────────────────────────────────────────────┐
│ REASONING LAYER: Plan Steps & Make Decisions        │
└─────────────────────────────────────────────────────┘

INPUT: Standardized Request Object

┌──────────────────────────────────────────┐
│ PLANNING STRATEGY                        │
├──────────────────────────────────────────┤
│                                          │
│ 1. Goal Decomposition                    │
│    Request: "Research AAPL Q3"           │
│    Decompose into sub-goals:             │
│    ├─ GOAL 1: Fetch AAPL 10-K            │
│    ├─ GOAL 2: Extract key metrics        │
│    ├─ GOAL 3: Analyze risks              │
│    ├─ GOAL 4: Compare peers              │
│    └─ GOAL 5: Generate report            │
│                                          │
│ 2. Dependency Analysis                   │
│    ├─ Sequential: GOAL 1 → GOAL 2        │
│    │              GOAL 3 → GOAL 4        │
│    └─ Parallel: GOAL 2 and GOAL 3        │
│                 (both use fetched doc)   │
│                                          │
│ 3. Tool Selection                        │
│    ├─ GOAL 1: Use Tool "EDGAR_Fetcher"   │
│    ├─ GOAL 2: Use Tool "LLM_Extractor"   │
│    ├─ GOAL 3: Use Tool "RiskAnalyzer"    │
│    ├─ GOAL 4: Use Tool "PeerComparator"  │
│    └─ GOAL 5: Use Tool "ReportGenerator" │
│                                          │
│ 4. Context Propagation                   │
│    ├─ Pass user tier → different models  │
│    ├─ Pass portfolio → risk analysis     │
│    └─ Pass history → personalization     │
│                                          │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ DECISION MAKING (ReAct Pattern)          │
├──────────────────────────────────────────┤
│                                          │
│ LLM Generates:                           │
│ "I need to research AAPL Q3 10-K.        │
│  Step 1: Fetch the document from EDGAR   │
│  Step 2: Extract financial metrics       │
│  Step 3: Analyze leverage and risks      │
│  Step 4: Generate investment snapshot    │
│                                          │
│  Let me start with Step 1..."            │
│                                          │
│ ↓ Thought → Action → Observation Loop    │
│                                          │
│ ITERATION 1:                             │
│ [Thought]: "I should fetch 10-K first"   │
│ [Action]: Call Tool "EDGAR_Fetcher"      │
│           with param ticker="AAPL"       │
│ [Observation]: "Got 10-K PDF text (100K  │
│                 chars), FY ending 9/2025"│
│ [Next]: Continue to Step 2               │
│                                          │
│ ITERATION 2:                             │
│ [Thought]: "Extract key metrics"         │
│ [Action]: Call Tool "LLM_Extractor"      │
│           with 10-K text                 │
│ [Observation]: "Extracted: Revenue       │
│                 $383B, EBITDA $119B,     │
│                 Debt $107B"              │
│ [Next]: Continue to Step 3               │
│                                          │
│ ...continues until complete              │
│                                          │
└──────────────────────────────────────────┘

OUTPUT: Action Plan (Graph)
{
  goals: [
    {id: "goal_1", name: "Fetch Document", status: "PENDING"},
    {id: "goal_2", name: "Extract Metrics", status: "PENDING"},
    {id: "goal_3", name: "Analyze Risks", status: "PENDING"},
    {id: "goal_4", name: "Generate Report", status: "PENDING"}
  ],
  dependencies: [
    {from: "goal_1", to: "goal_2", type: "SEQUENTIAL"},
    {from: "goal_1", to: "goal_3", type: "PARALLEL_AFTER"}
  ],
  tools_needed: ["EDGAR_Fetcher", "LLM_Extractor", "RiskAnalyzer"]
}
```


***

### **LAYER 3: ACTION (Tool Execution)**

```
┌─────────────────────────────────────────────────────┐
│ ACTION LAYER: Execute Tools & Handle Execution      │
└─────────────────────────────────────────────────────┘

INPUT: Action Plan + Tool Selection

┌──────────────────────────────────────────┐
│ TOOL CALLING PATTERN                     │
├──────────────────────────────────────────┤
│                                          │
│ Tool Registry:                           │
│ {                                        │
│   "EDGAR_Fetcher": {                     │
│     description: "Fetch SEC filings",    │
│     params: {                            │
│       ticker: string,                    │
│       form_type: "10-K" | "10-Q",        │
│       fiscal_year: integer               │
│     },                                   │
│     return_type: {                       │
│       status: string,                    │
│       data: {content: string, url: str}, │
│       error: string | null               │
│     }                                    │
│   },                                     │
│   "LLM_Extractor": {...},                │
│   "RiskAnalyzer": {...}                  │
│ }                                        │
│                                          │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ EXECUTION PIPELINE                       │
├──────────────────────────────────────────┤
│                                          │
│ 1. Pre-Execution Checks                  │
│    ├─ Tool exists?                       │
│    ├─ Parameters valid?                  │
│    ├─ Rate limits OK?                    │
│    ├─ User has permission?               │
│    └─ Cost within budget?                │
│                                          │
│ 2. Execution Strategy                    │
│    ├─ Sequential: Tool A → Tool B        │
│    ├─ Parallel: Tool A & Tool B (async)  │
│    ├─ Conditional: IF (result A) THEN B  │
│    └─ Fallback: Try A, if fail try B     │
│                                          │
│ 3. Timeout Management                    │
│    ├─ Per tool: 30s timeout              │
│    ├─ Total request: 300s max            │
│    └─ Graceful degradation on timeout    │
│                                          │
│ 4. Result Processing                     │
│    ├─ Normalize output format            │
│    ├─ Extract key data                   │
│    ├─ Validate constraints               │
│    └─ Store for audit trail              │
│                                          │
└──────────────────────────────────────────┘

EXAMPLE EXECUTION:

Tool Call 1: EDGAR_Fetcher(ticker="AAPL")
  ↓
  [Execution: 8 sec]
  ✅ Result: 10-K PDF text (100K chars)
  ↓
  Store in State: documents.10k = "..."

Tool Call 2: LLM_Extractor(doc=documents.10k)
  ↓
  [Execution: 18 sec]
  ✅ Result: {revenue: 383B, ebitda: 119B, debt: 107B}
  ↓
  Store in State: metrics = {...}

Tool Call 3 & 4 (Parallel):
  ├─ RiskAnalyzer(metrics=metrics)
  │  [Execution: 12 sec]
  │  ✅ Result: {leverage_risk: "low", ...}
  │
  └─ PeerComparator(ticker="AAPL", metrics=metrics)
     [Execution: 8 sec]
     ✅ Result: {peers: [...], relative_valuation: {...}}

Tool Call 5: ReportGenerator(
  metrics=metrics,
  risks=risks,
  peers=peers
)
  ↓
  [Execution: 35 sec]
  ✅ Result: Snapshot PDF + Markdown

Total Latency: 8 + 18 + MAX(12, 8) + 35 = 73 sec
```


***

### **LAYER 4: LEARNING (Feedback Loop)**

```
┌─────────────────────────────────────────────────────┐
│ LEARNING LAYER: Improve from Feedback              │
└─────────────────────────────────────────────────────┘

INPUT: User Interactions & Outcomes

┌──────────────────────────────────────────┐
│ FEEDBACK COLLECTION                      │
├──────────────────────────────────────────┤
│                                          │
│ Signal Types:                            │
│ ├─ Explicit:                             │
│ │  ├─ "Report accuracy: 5/5" ⭐⭐⭐⭐⭐     │
│ │  ├─ "Risks flagged correctly? Yes"     │
│ │  └─ "Would you recommend?"             │
│ │                                        │
│ ├─ Implicit:                             │
│ │  ├─ Time spent reading report (30 min) │
│ │  ├─ Export action (PDF downloaded)     │
│ │  ├─ Share to team (reused)             │
│ │  └─ Follow-up research (high value)    │
│ │                                        │
│ └─ Outcome:                              │
│    ├─ Did user make investment? (Y/N)    │
│    ├─ Trade outcome: +5% gain            │
│    └─ Loss avoided?                      │
│                                          │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ MODEL IMPROVEMENT LOOP                    │
├──────────────────────────────────────────┤
│                                          │
│ CYCLE 1: Data Collection                 │
│ └─ After 100 reports generated:          │
│    • Collect 100 feedback scores         │
│    • Average accuracy rating: 4.2/5      │
│                                          │
│ CYCLE 2: Analysis                        │
│ └─ Identify patterns:                    │
│    • Metric extraction: 95% accuracy     │
│    • Risk flagging: 80% accuracy ← LOW   │
│    • Peer comparison: 88% accuracy       │
│                                          │
│ CYCLE 3: Intervention                    │
│ └─ Risk flagging scoring is too aggressive │
│    • Review 10 false positives           │
│    • Adjust risk thresholds              │
│    • Retrain model on flagged cases      │
│                                          │
│ CYCLE 4: Deployment                      │
│ └─ A/B test new model:                   │
│    • 50% users: old model (baseline)     │
│    • 50% users: new model (test)         │
│    • Track: accuracy improvement         │
│    • Rollout if +5% better               │
│                                          │
│ CYCLE 5: Monitoring                      │
│ └─ Continuous metrics:                   │
│    • Risk flagging accuracy: 87% → 90%   │
│    • User satisfaction: 4.2 → 4.5        │
│    • Time saved: 280 min/month/user      │
│                                          │
└──────────────────────────────────────────┘

FEEDBACK LOOP EXAMPLE:

Month 1:
  Report: "AAPL Debt/EBITDA = 0.9x ✅ Healthy"
  User feedback: ⭐⭐⭐⭐⭐ "Accurate"
  Action: Reward this extraction pattern

Month 2:
  Report: "XYZ Corp Leverage = 2.2x ⚠️ High Risk"
  User feedback: ⭐ "False alarm, leverage is healthy"
  Action: 
    • Flag as false positive
    • Review extraction logic
    • Adjust thresholds
    • Retrain on similar cases

Month 3:
  Report: "XYZ Corp Leverage = 1.8x ✅ Acceptable"
  User feedback: ⭐⭐⭐⭐⭐ "Much better!"
  Action: Model improved, continue monitoring
```


***

## II. AGENT TYPES \& PATTERNS

```
┌─────────────────────────────────────────────────────┐
│ AGENT TYPES: Choose Based on Use Case               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────┐
│ 1. REACTIVE AGENTS              │
│    (Simple, Rule-Based)          │
├─────────────────────────────────┤
│                                 │
│ Pattern: Input → Rules → Action │
│                                 │
│ Example: Price Alert Agent      │
│ Rule 1: IF price > $280 THEN    │
│         Send alert "High"       │
│ Rule 2: IF price < $200 THEN    │
│         Send alert "Low"        │
│                                 │
│ Pros: Fast, Predictable         │
│ Cons: Inflexible, Can't learn   │
│                                 │
│ Use for: Simple automation,     │
│          Rule-based workflows   │
│                                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 2. DELIBERATIVE AGENTS          │
│    (Planning + Reasoning)        │
├─────────────────────────────────┤
│                                 │
│ Pattern: Perception → Planning  │
│          → Action → Learning    │
│                                 │
│ Example: finAI Research Agent   │
│ 1. Perceive: "Research AAPL"    │
│ 2. Plan: Decompose into steps   │
│ 3. Act: Execute tools           │
│ 4. Learn: Feedback loop         │
│                                 │
│ Pros: Flexible, Can adapt       │
│ Cons: Slower, More complex      │
│                                 │
│ Use for: Complex tasks,         │
│          Multi-step workflows   │
│                                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 3. COLLABORATIVE AGENTS         │
│    (Multi-Agent Orchestration)   │
├─────────────────────────────────┤
│                                 │
│ Pattern: Agent 1 + Agent 2 +    │
│          Agent 3 → Coordinator  │
│                                 │
│ Example: finAI Multi-Agent      │
│ • Analyst Agent: Research       │
│ • Risk Agent: Analyze risks     │
│ • Portfolio Agent: Check impact │
│ • Coordinator: Orchestrate      │
│                                 │
│ Pros: Specialized, Scalable     │
│ Cons: Complex coordination      │
│                                 │
│ Use for: Large systems,         │
│          Multiple concerns      │
│                                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 4. HIERARCHICAL AGENTS          │
│    (Chain of Authority)          │
├─────────────────────────────────┤
│                                 │
│ Pattern: Master Agent           │
│          ├─ Sub-Agent 1         │
│          ├─ Sub-Agent 2         │
│          └─ Sub-Agent 3         │
│                                 │
│ Example:                        │
│ Master: "Research & report"     │
│ ├─ Sub 1: "Fetch docs"         │
│ ├─ Sub 2: "Extract metrics"    │
│ └─ Sub 3: "Analyze risks"      │
│                                 │
│ Pros: Clear structure           │
│ Cons: Less flexible             │
│                                 │
│ Use for: Well-defined workflows │
│                                 │
└─────────────────────────────────┘
```


***

## III. STATE MANAGEMENT PATTERNS

```
┌─────────────────────────────────────────────────────┐
│ STATE MACHINE: How State Flows Through Agent        │
└─────────────────────────────────────────────────────┘

State Definition (TypedDict):
{
  user_id: str,
  request_id: str,
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED",
  
  # Perception
  input_text: str,
  parsed_intent: dict,
  parameters: dict,
  
  # Reasoning
  action_plan: list,
  current_step: int,
  
  # Action
  tool_calls: list,
  tool_results: dict,
  
  # Output
  final_report: dict,
  
  # Metadata
  created_at: timestamp,
  updated_at: timestamp,
  processing_time_ms: int,
  error_message: str | None
}

STATE TRANSITIONS:

START
  ↓
PENDING (Validation)
  ├─ Valid? → RUNNING (Step 1)
  └─ Invalid? → FAILED (Error)
  
RUNNING (Step 1-N)
  ├─ Tool success? → Continue to Step N+1
  ├─ Tool timeout? → FALLBACK (retry)
  ├─ Tool failure? → ERROR_HANDLER
  │                   ├─ Retry? → Re-execute
  │                   └─ Skip? → Continue next step
  └─ All steps done? → COMPLETED
  
COMPLETED
  ├─ Send result to user
  ├─ Store audit trail
  └─ Trigger feedback loop
  
FAILED
  ├─ Log error
  ├─ Alert user
  └─ Enable retry

┌──────────────────────────────────────────┐
│ STATE PERSISTENCE (Checkpointing)        │
├──────────────────────────────────────────┤
│                                          │
│ LangGraph automatically saves state:     │
│ • After each node completion             │
│ • Before each tool call                  │
│ • On error (for debugging)               │
│                                          │
│ Benefits:                                │
│ ✓ Resume on failure (checkpoint + retry)│
│ ✓ Audit trail (what happened?)          │
│ ✓ Debugging (replay execution)          │
│ ✓ Parallel execution (state isolation)  │
│                                          │
└──────────────────────────────────────────┘
```


***

## IV. ERROR HANDLING STRATEGIES

```
┌─────────────────────────────────────────────────────┐
│ ERROR HIERARCHY & RECOVERY                          │
└─────────────────────────────────────────────────────┘

ERROR TYPES:

1. INPUT ERRORS (Validation Layer)
   ├─ Invalid format: ticker = "INVALID123"
   ├─ Missing params: no quarter specified
   └─ Recovery: Return 400 error + guidance
   
2. TOOL ERRORS (Execution Layer)
   ├─ API timeout: EDGAR takes >10s
   ├─ Rate limit: Hit API quota
   ├─ Not found: Ticker doesn't exist
   └─ Recovery: Retry, Fallback, or Skip
   
3. PROCESSING ERRORS (Reasoning Layer)
   ├─ Parsing failure: Can't extract metrics
   ├─ Reasoning failure: Plan doesn't make sense
   └─ Recovery: Alternative approach or escalate
   
4. OUTPUT ERRORS (Action Layer)
   ├─ Report generation failed
   ├─ File export failed
   └─ Recovery: Simplify output format

┌──────────────────────────────────────────┐
│ RETRY STRATEGIES                         │
├──────────────────────────────────────────┤
│                                          │
│ Strategy 1: Exponential Backoff          │
│ Attempt 1: Wait 1s → Retry ❌           │
│ Attempt 2: Wait 2s → Retry ❌           │
│ Attempt 3: Wait 4s → Retry ✅           │
│ Total: 3 attempts, max 8s               │
│                                          │
│ Strategy 2: Circuit Breaker              │
│ When: 5 consecutive failures             │
│ Action: Open circuit → Fast-fail         │
│ Recovery: Half-open after 60s            │
│                                          │
│ Strategy 3: Fallback                     │
│ If EDGAR fails → Use cached 10-K         │
│ If LLM extraction fails → Use regex      │
│ If both fail → Return error + options    │
│                                          │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ GRACEFUL DEGRADATION                     │
├──────────────────────────────────────────┤
│                                          │
│ Full Service:                            │
│ • Fetch 10-K + Earnings + News           │
│ • Extract metrics + risks + peers        │
│ • Generate PDF + Email + Dashboard       │
│ • Processing: 70 seconds                 │
│                                          │
│ Degraded (1 source unavailable):         │
│ • Fetch 10-K + Earnings (skip news)      │
│ • Extract metrics + risks (skip peers)   │
│ • Generate PDF only (skip email)         │
│ • Processing: 45 seconds                 │
│ • Output: "⚠️ Limited data due to API"   │
│                                          │
│ Minimal (only critical path):            │
│ • Fetch 10-K only                        │
│ • Extract metrics only                   │
│ • Generate markdown (skip PDF)           │
│ • Processing: 20 seconds                 │
│ • Output: "⚠️ Basic report, expanded     │
│            data unavailable"             │
│                                          │
└──────────────────────────────────────────┘
```


***

## V. TOOL INTERFACE DESIGN

```
┌─────────────────────────────────────────────────────┐
│ TOOL REGISTRY: Standardized Interface               │
└─────────────────────────────────────────────────────┘

Each tool must define:

1. Metadata
   {
     name: "EDGAR_Fetcher",
     category: "DATA_RETRIEVAL",
     description: "Fetch SEC filings from EDGAR",
     version: "1.0.0",
     author: "finAI",
     last_updated: "2025-12-12"
   }

2. Interface (Input/Output)
   {
     input_schema: {
       type: "object",
       properties: {
         ticker: {type: "string", description: "Stock ticker"},
         form_type: {type: "string", enum: ["10-K", "10-Q"]},
         fiscal_year: {type: "integer", min: 1990, max: 2030}
       },
       required: ["ticker", "form_type"]
     },
     
     output_schema: {
       type: "object",
       properties: {
         status: {type: "string", enum: ["success", "failure"]},
         data: {
           type: "object",
           properties: {
             content: {type: "string"},
             url: {type: "string"},
             filing_date: {type: "string"}
           }
         },
         error: {type: "string", nullable: true}
       }
     }
   }

3. Execution Config
   {
     timeout_seconds: 30,
     max_retries: 3,
     retry_delay_ms: 1000,
     cost_per_call: 0.001,
     rate_limit: "100 calls/hour",
     requires_auth: true
   }

4. Implementation
   {
     handler: async function(input) {
       // Validation
       if (!input.ticker) throw Error("Missing ticker")
       
       // Call EDGAR API
       const response = await fetch(
         `https://www.sec.gov/.../${input.ticker}`
       )
       
       // Parse response
       const content = await response.text()
       
       // Return standardized
       return {
         status: "success",
         data: {
           content: content,
           url: response.url,
           filing_date: extractDate(content)
         },
         error: null
       }
     }
   }

┌──────────────────────────────────────────┐
│ TOOL CALLING SYNTAX (LLM)                │
├──────────────────────────────────────────┤
│                                          │
│ LLM generates:                           │
│ "I need to fetch the 10-K for AAPL.      │
│  Let me call the EDGAR_Fetcher tool."    │
│                                          │
│ Structured call:                         │
│ {                                        │
│   tool_name: "EDGAR_Fetcher",            │
│   arguments: {                           │
│     ticker: "AAPL",                      │
│     form_type: "10-K",                   │
│     fiscal_year: 2025                    │
│   }                                      │
│ }                                        │
│                                          │
│ Agent executes and returns:              │
│ {                                        │
│   status: "success",                     │
│   data: {                                │
│     content: "UNITED STATES SECURITIES   │
│               AND EXCHANGE COMMISSION...",│
│     url: "https://www.sec.gov/...",      │
│     filing_date: "2025-11-30"            │
│   }                                      │
│ }                                        │
│                                          │
│ LLM processes:                           │
│ "Great! I got the 10-K. Now I should     │
│  extract key metrics from this document."│
│                                          │
└──────────────────────────────────────────┘
```


***

## VI. AGENT CONFIGURATION \& TUNING

```
┌─────────────────────────────────────────────────────┐
│ CONFIGURATION PARAMETERS: How to Tune Agent         │
└─────────────────────────────────────────────────────┘

```


# Agent Config

{
\# LLM Settings
"model": "gpt-4",
"temperature": 0.2,  \# Lower = deterministic
"max_tokens": 2000,
"top_p": 0.9,

    # Planning
    "planning_strategy": "hierarchical",  # vs "flat"
    "max_steps": 10,
    "enable_reflection": True,  # Think about decisions
    
    # Tool Calling
    "parallel_execution": True,
    "max_parallel_tools": 3,
    "timeout_per_tool_sec": 30,
    
    # Error Handling
    "retry_strategy": "exponential_backoff",
    "max_retries": 3,
    "fallback_enabled": True,
    
    # Memory
    "memory_type": "short_term",  # vs "long_term"
    "max_history_tokens": 5000,
    
    # Output
    "output_format": "json",
    "verbosity": "medium",  # low | medium | high
    
    # Monitoring
    "enable_logging": True,
    "enable_tracing": True,
    "sample_rate": 0.1  # Log 10% of requests
    }

```

**Tuning Guide:**

| Parameter | Effect | Tune When |
|-----------|--------|-----------|
| `temperature` | Creativity vs Consistency | Too random? ↓ Temp to 0.1 |
| `max_steps` | Max iterations | Taking too long? ↓ max_steps |
| `parallel_tools` | Concurrency | Slow overall? ↑ parallel |
| `retry_strategy` | Failure handling | Too many timeouts? ↑ backoff |
| `memory_tokens` | Context size | Losing important info? ↑ tokens |

---

## VII. MONITORING & OBSERVABILITY

```

┌─────────────────────────────────────────────────────┐
│ KEY METRICS TO TRACK                                │
└─────────────────────────────────────────────────────┘

Performance Metrics:
├─ Latency (end-to-end): 70 sec target
├─ Tool call latency: Per-tool breakdown
├─ Success rate: 99.5% target
└─ Error rate: <0.5%

Quality Metrics:
├─ Output accuracy: >90%
├─ Risk detection sensitivity: >85%
├─ User satisfaction: >4.2/5
└─ False positive rate: <5%

Cost Metrics:
├─ API cost per request: <\$0.05
├─ Compute cost per request: <\$0.01
├─ Total cost per user/month: <\$50
└─ Cost per happy user: <\$0.10

Reliability Metrics:
├─ Uptime: 99.95% target
├─ Availability: 99.9% target
├─ Mean time to recovery: <5 min
└─ Error budget: 22 minutes/month

┌──────────────────────────────────────────┐
│ TRACING (With LangSmith)                 │
├──────────────────────────────────────────┤
│                                          │
│ Enable trace for each request:           │
│ https://smith.langchain.com/...          │
│                                          │
│ View:                                    │
│ ✓ Execution timeline (each step)         │
│ ✓ Tool calls (what was called)           │
│ ✓ LLM prompts (what was asked)           │
│ ✓ Outputs (what was returned)            │
│ ✓ Costs (tokens used)                    │
│ ✓ Errors (what failed)                   │
│                                          │
│ Debug example:                           │
│ Step 1: Fetch 10-K (8s) ✅               │
│ Step 2: Extract metrics (18s) ✅         │
│ Step 3: Risk analysis (12s) ⚠️ SLOW      │
│   → RiskAnalyzer took too long           │
│   → Check: Too many rules? Too much data?│
│   → Fix: Optimize rule engine            │
│                                          │
└──────────────────────────────────────────┘

```

---

## VIII. COMPLETE AGENT TEMPLATE

```

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated

# ═══════════════════════════════════════════════════

# 1. DEFINE STATE (What flows through agent)

# ═══════════════════════════════════════════════════

class AgentState(TypedDict):
\# Perception
user_input: str
parsed_intent: dict

    # Reasoning
    action_plan: list
    current_step: int
    
    # Action
    tool_results: dict
    
    # Output
    final_output: dict
    
    # Metadata
    errors: list
    processing_log: list
    
# ═══════════════════════════════════════════════════

# 2. DEFINE TOOLS

# ═══════════════════════════════════════════════════

async def tool_fetch_data(ticker: str) -> dict:
"""Fetch data from API"""
return {"data": "..."}

async def tool_analyze(data: dict) -> dict:
"""Analyze data"""
return {"analysis": "..."}

async def tool_generate_report(analysis: dict) -> dict:
"""Generate report"""
return {"report": "..."}

# ═══════════════════════════════════════════════════

# 3. DEFINE NODES (Each step is a node)

# ═══════════════════════════════════════════════════

def node_perception(state: AgentState) -> AgentState:
"""Parse user input"""
intent = parse_intent(state["user_input"])
state["parsed_intent"] = intent
state["processing_log"].append("perception_ok")
return state

def node_reasoning(state: AgentState) -> AgentState:
"""Plan steps"""
plan = create_plan(state["parsed_intent"])
state["action_plan"] = plan
state["current_step"] = 0
state["processing_log"].append("reasoning_ok")
return state

def node_action_step_1(state: AgentState) -> AgentState:
"""Execute step 1"""
result = await tool_fetch_data(state["parsed_intent"]["ticker"])
state["tool_results"]["step_1"] = result
state["current_step"] += 1
return state

def node_action_step_2(state: AgentState) -> AgentState:
"""Execute step 2"""
result = await tool_analyze(state["tool_results"]["step_1"])
state["tool_results"]["step_2"] = result
state["current_step"] += 1
return state

def node_action_step_3(state: AgentState) -> AgentState:
"""Execute step 3"""
result = await tool_generate_report(state["tool_results"]["step_2"])
state["tool_results"]["step_3"] = result
state["current_step"] += 1
return state

def node_output(state: AgentState) -> AgentState:
"""Format output"""
state["final_output"] = format_output(state["tool_results"])
state["processing_log"].append("output_ready")
return state

# ═══════════════════════════════════════════════════

# 4. BUILD GRAPH

# ═══════════════════════════════════════════════════

workflow = StateGraph(AgentState)

workflow.add_node("perception", node_perception)
workflow.add_node("reasoning", node_reasoning)
workflow.add_node("action_1", node_action_step_1)
workflow.add_node("action_2", node_action_step_2)
workflow.add_node("action_3", node_action_step_3)
workflow.add_node("output", node_output)

# ═══════════════════════════════════════════════════

# 5. ADD EDGES (Flow control)

# ═══════════════════════════════════════════════════

workflow.add_edge(START, "perception")
workflow.add_edge("perception", "reasoning")
workflow.add_edge("reasoning", "action_1")
workflow.add_edge("action_1", "action_2")
workflow.add_edge("action_2", "action_3")
workflow.add_edge("action_3", "output")
workflow.add_edge("output", END)

# ═══════════════════════════════════════════════════

# 6. COMPILE (Add checkpointer for audit trail)

# ═══════════════════════════════════════════════════

agent = workflow.compile(checkpointer=MemorySaver())

# ═══════════════════════════════════════════════════

# 7. EXECUTE

# ═══════════════════════════════════════════════════

initial_state = {
"user_input": "Research AAPL Q3",
"parsed_intent": {},
"action_plan": [],
"current_step": 0,
"tool_results": {},
"final_output": {},
"errors": [],
"processing_log": []
}

result = agent.invoke(initial_state)

print(f"✅ Output: {result['final_output']}")
print(f"📊 Logs: {result['processing_log']}")

```

---

## IX. BEST PRACTICES CHECKLIST

```

┌─────────────────────────────────────────────────────┐
│ AGENT DESIGN BEST PRACTICES                         │
└─────────────────────────────────────────────────────┘

□ Perception Layer
✓ Validate all inputs before processing
✓ Normalize formats (datetime, currency, ticker)
✓ Extract context (user tier, permissions)
✓ Check rate limits early

□ Reasoning Layer
✓ Decompose goals into clear steps
✓ Identify dependencies (sequential vs parallel)
✓ Set realistic timeouts per step
✓ Plan fallback strategies before execution

□ Action Layer
✓ Define clear tool interfaces (input/output schema)
✓ Implement timeout handling
✓ Log all tool calls (audit trail)
✓ Validate tool outputs against schema
✓ Handle partial failures gracefully

□ Learning Layer
✓ Collect explicit feedback (user ratings)
✓ Track implicit signals (time spent, exports)
✓ Analyze failure patterns weekly
✓ A/B test improvements before rollout
✓ Monitor regressions post-deployment

□ General
✓ Keep state immutable (functional updates)
✓ Use checkpointing for audit trail
✓ Enable comprehensive logging
✓ Monitor latency + accuracy metrics
✓ Plan for graceful degradation
✓ Design for testability (mocks for tools)
✓ Document assumptions + constraints

```

---

## X. finAI Specific Design

```

finAI AGENT DESIGN (Specialized for Financial Research)

┌─────────────────────────────────────────┐
│ PERCEPTION                              │
├─────────────────────────────────────────┤
│ -  Parse ticker format (validate against  │
│   SEC CUSIP database)                    │
│ -  Extract research intent (research vs   │
│   monitoring vs portfolio analysis)      │
│ -  Detect user expertise (beginner vs     │
│   analyst) → adjust complexity           │
└─────────────────────────────────────────┘
↓
┌─────────────────────────────────────────┐
│ REASONING                               │
├─────────────────────────────────────────┤
│ -  Decompose: Research = Fetch + Extract │
│   + Analyze + Report                    │
│ -  Prioritize: Always fetch 10-K first   │
│   (most authoritative source)            │
│ -  Parallel: News + Peer analysis        │
│ -  Fallback: Use cache if API down       │
└─────────────────────────────────────────┘
↓
┌─────────────────────────────────────────┐
│ ACTION                                  │
├─────────────────────────────────────────┤
│ Tools: EDGAR + Yahoo + News API + LLM   │
│ Timeout: 30s per tool, 300s total       │
│ Retry: 3x exponential backoff           │
│ Error: Graceful degradation (partial    │
│        data better than error)          │
└─────────────────────────────────────────┘
↓
┌─────────────────────────────────────────┐
│ OUTPUT                                  │
├─────────────────────────────────────────┤
│ -  1-page snapshot (pdf + markdown)      │
│ -  Source attribution (every stat traced)│
│ -  Compliance ready (audit trail full)   │
│ -  Exportable (email, share, Slack)      │
└─────────────────────────────────────────┘
↓
┌─────────────────────────────────────────┐
│ LEARNING                                │
├─────────────────────────────────────────┤
│ -  Track: Extraction accuracy, risk flag │
│   correctness, user actions             │
│ -  Feedback: "Helpful?", outcome tracking│
│ -  Improve: Fine-tune risk thresholds,   │
│   prompt engineering, tool selection    │
└─────────────────────────────────────────┘

```

---

**Tóm tắt: Agent Design System là blueprint hoàn chỉnh để build production-grade agents. 4 lớp (Perception → Reasoning → Action → Learning) cộng với pattern rõ ràng = **hệ thống mạnh mẽ, flexible, scalable, และ maintainable**. Ready to implement! 🚀**```

