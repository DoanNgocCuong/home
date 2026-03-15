Tab "Chat" hiển thị: 

- **"Create a graph with a messages key to chat with."**

Để tạo graph có `messages` key trong state và cấu hình các node xử lý messages trong LangGraph, bạn cần làm theo các bước sau:

## 1. Định nghĩa State với Messages Key

```python
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# Định nghĩa State với messages key
class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Có thể thêm các key khác nếu cần
    # user_info: dict
    # context: str
```

## 2. Tạo các Node xử lý Messages

```python
from langchain_core.messages import HumanMessage, AIMessage

def chatbot_node(state: GraphState):
    """Node chính xử lý chat"""
    messages = state["messages"]
  
    # Lấy message cuối cùng từ user
    last_message = messages[-1]
  
    # Xử lý logic chatbot ở đây
    # Ví dụ: gọi LLM, xử lý task, etc.
    response_text = f"Tôi đã nhận được: {last_message.content}"
  
    # Trả về AIMessage
    return {
        "messages": [AIMessage(content=response_text)]
    }

def analyze_input_node(state: GraphState):
    """Node phân tích input từ user"""
    messages = state["messages"]
    last_message = messages[-1]
  
    # Phân tích intent, extract thông tin
    analysis_result = f"Phân tích: {last_message.content}"
  
    return {
        "messages": [AIMessage(content=analysis_result)]
    }

def task_processor_node(state: GraphState):
    """Node xử lý task cụ thể"""
    messages = state["messages"]
  
    # Logic xử lý task
    task_result = "Task đã được xử lý thành công"
  
    return {
        "messages": [AIMessage(content=task_result)]
    }
```

## 3. Xây dựng Graph với Messages Flow

```python
from langgraph.graph import StateGraph, END, START

# Tạo graph builder
workflow = StateGraph(GraphState)

# Thêm các node
workflow.add_node("analyze_input", analyze_input_node)
workflow.add_node("process_task", task_processor_node)
workflow.add_node("chatbot", chatbot_node)

# Định nghĩa flow
workflow.add_edge(START, "analyze_input")
workflow.add_edge("analyze_input", "process_task")
workflow.add_edge("process_task", "chatbot")
workflow.add_edge("chatbot", END)

# Compile graph
app = workflow.compile()
```

## 4. Sử dụng Graph với Messages

```python
from langchain_core.messages import HumanMessage

# Test graph
initial_state = {
    "messages": [HumanMessage(content="Xin chào, tôi cần giúp đỡ")]
}

# Chạy graph
result = app.invoke(initial_state)
print(result["messages"])
```

## 5. Cấu hình nâng cao cho Chat

```python
def should_continue(state: GraphState):
    """Điều kiện để tiếp tục hoặc kết thúc"""
    messages = state["messages"]
    last_message = messages[-1]
  
    # Logic quyết định flow tiếp theo
    if "goodbye" in last_message.content.lower():
        return "END"
    else:
        return "continue"

# Thêm conditional edge
workflow.add_conditional_edges(
    "chatbot",
    should_continue,
    {
        "continue": "analyze_input",
        "END": END
    }
)
```

## 6. Cấu hình Memory/Persistence (Tùy chọn)

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Thêm memory để lưu conversation
memory = SqliteSaver.from_conn_string(":memory:")
app = workflow.compile(checkpointer=memory)

# Sử dụng với thread_id để track conversation
config = {"configurable": {"thread_id": "conversation_1"}}
result = app.invoke(initial_state, config)
```

## 7. Các Best Practices:

### Xử lý Messages đúng cách:

```python
def node_with_proper_message_handling(state: GraphState):
    messages = state["messages"]
  
    # Luôn kiểm tra messages tồn tại
    if not messages:
        return {"messages": [AIMessage(content="No messages found")]}
  
    # Xử lý last message
    last_message = messages[-1]
  
    # Tạo response message
    response = AIMessage(content="Response content")
  
    # Trả về trong format đúng
    return {"messages": [response]}
```

### Error Handling:

```python
def robust_node(state: GraphState):
    try:
        messages = state["messages"]
        # Processing logic
        return {"messages": [AIMessage(content="Success")]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Error: {str(e)}")]}
```

## 8. Deploy và Test

Sau khi tạo graph với cấu hình trên:

1. **Save file** với tên như `todo_agent.py`
2. **Import vào LangGraph Studio**
3. **Tab Chat sẽ active** và có thể sử dụng
4. **Test conversation flow** qua UI

**Lưu ý quan trọng**:

- `messages` key phải có type `Annotated[Sequence[BaseMessage], add_messages]`
- Mỗi node phải return messages trong đúng format
- Sử dụng `add_messages` reducer để merge messages properly

Với cấu hình này, bạn sẽ có thể sử dụng chế độ Chat trong LangGraph Studio!
