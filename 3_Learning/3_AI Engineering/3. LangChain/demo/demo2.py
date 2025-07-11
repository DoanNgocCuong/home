# simple_complete_example.py
import os
from dotenv import load_dotenv
from typing import TypedDict, List

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# LangSmith imports
from langsmith import Client
from langchain.callbacks.tracers import LangChainTracer

# LangGraph imports
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# =============================================================================
# PART 1: LANGCHAIN BASIC CHAIN
# =============================================================================
class SimpleLangChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def create_simple_chain(self):
        """Tạo chain đơn giản"""
        template = """
        Bạn là trợ lý AI thông minh.
        
        Câu hỏi: {question}
        Trả lời ngắn gọn:
        """
        
        prompt = PromptTemplate(
            input_variables=["question"],
            template=template
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain
    
    def run_chain(self, question):
        """Chạy chain"""
        chain = self.create_simple_chain()
        result = chain.run(question)
        return result

# =============================================================================
# PART 2: LANGSMITH MONITORING
# =============================================================================
class SimpleLangSmith:
    def __init__(self):
        # Setup LangSmith (nếu có API key)
        if os.getenv("LANGSMITH_API_KEY"):
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
            os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
            os.environ["LANGCHAIN_PROJECT"] = "simple-practice"
            
            self.client = Client()
            self.tracer = LangChainTracer(project_name="simple-practice")
            self.monitoring_enabled = True
        else:
            self.monitoring_enabled = False
            print("LangSmith monitoring disabled (no API key)")
    
    def create_monitored_chain(self):
        """Tạo chain có monitoring"""
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        template = """
        Trả lời câu hỏi: {question}
        
        Câu trả lời:
        """
        
        prompt = PromptTemplate(
            input_variables=["question"],
            template=template
        )
        
        # Thêm callback nếu monitoring enabled
        callbacks = [self.tracer] if self.monitoring_enabled else []
        
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callbacks=callbacks
        )
        
        return chain
    
    def run_with_monitoring(self, question):
        """Chạy với monitoring"""
        chain = self.create_monitored_chain()
        result = chain.run(question)
        
        if self.monitoring_enabled:
            print("✅ Đã ghi log vào LangSmith")
        
        return result

# =============================================================================
# PART 3: LANGGRAPH MULTI-AGENT
# =============================================================================
class AgentState(TypedDict):
    """State cho LangGraph"""
    messages: List[str]
    current_task: str
    result: str

class SimpleLangGraph:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    
    def thinking_agent(self, state: AgentState):
        """Agent suy nghĩ"""
        task = state["current_task"]
        
        # Simulate thinking
        thinking_result = f"Đang suy nghĩ về: {task}"
        
        return {
            "messages": state["messages"] + [thinking_result],
            "current_task": task,
            "result": thinking_result
        }
    
    def answering_agent(self, state: AgentState):
        """Agent trả lời"""
        task = state["current_task"]
        
        # Simple answering logic
        if "langchain" in task.lower():
            answer = "LangChain là framework để xây dựng ứng dụng LLM"
        elif "langsmith" in task.lower():
            answer = "LangSmith là công cụ monitoring cho LangChain"
        elif "langgraph" in task.lower():
            answer = "LangGraph là framework để xây dựng multi-agent workflows"
        else:
            answer = f"Tôi hiểu bạn hỏi về: {task}"
        
        return {
            "messages": state["messages"] + [answer],
            "current_task": task,
            "result": answer
        }
    
    def create_simple_workflow(self):
        """Tạo workflow đơn giản"""
        # Tạo graph
        workflow = StateGraph(AgentState)
        
        # Thêm nodes
        workflow.add_node("thinking", self.thinking_agent)
        workflow.add_node("answering", self.answering_agent)
        
        # Thêm edges
        workflow.add_edge("thinking", "answering")
        workflow.add_edge("answering", END)
        
        # Set entry point
        workflow.set_entry_point("thinking")
        
        # Compile
        app = workflow.compile()
        return app
    
    def run_workflow(self, question):
        """Chạy workflow"""
        app = self.create_simple_workflow()
        
        initial_state = {
            "messages": [],
            "current_task": question,
            "result": ""
        }
        
        result = app.invoke(initial_state)
        return result

# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    print("🚀 SIMPLE LANGCHAIN → LANGSMITH → LANGGRAPH EXAMPLE")
    print("=" * 60)
    
    # Test questions
    questions = [
        "LangChain là gì?",
        "LangSmith có tác dụng gì?", 
        "LangGraph hoạt động như thế nào?"
    ]
    
    # =============================================================================
    # PART 1: Test LangChain
    # =============================================================================
    print("\n📝 PART 1: LANGCHAIN BASIC CHAIN")
    print("-" * 30)
    
    langchain_app = SimpleLangChain()
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = langchain_app.run_chain(question)
        print(f"A: {answer}")
    
    # =============================================================================
    # PART 2: Test LangSmith
    # =============================================================================
    print("\n📊 PART 2: LANGSMITH MONITORING")
    print("-" * 30)
    
    langsmith_app = SimpleLangSmith()
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = langsmith_app.run_with_monitoring(question)
        print(f"A: {answer}")
    
    # =============================================================================
    # PART 3: Test LangGraph
    # =============================================================================
    print("\n🔄 PART 3: LANGGRAPH MULTI-AGENT")
    print("-" * 30)
    
    langgraph_app = SimpleLangGraph()
    
    for question in questions:
        print(f"\nQ: {question}")
        result = langgraph_app.run_workflow(question)
        print(f"Messages: {result['messages']}")
        print(f"Final Result: {result['result']}")

if __name__ == "__main__":
    main()
