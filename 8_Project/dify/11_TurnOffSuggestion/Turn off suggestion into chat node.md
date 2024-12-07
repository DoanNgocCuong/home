
http://localhost:5011/console/api/mindpal/app/7368471d-77ae-4d6b-8987-2821a6515797/provider/d22767ad-677a-4520-9bf7-8111dde7a303/node/1733498679897/node-execution/0902744e-55d4-4aba-adb1-52e4337b8951/variable/chat_user_input_a1/chat


Muốn chỉ khi nào người dùng chat trong INPUT-CHAT thì mới cập nhật suggest question.  
Còn khi click vào suggestion thì suggest question chỉ gửi đến chatbot. (Không tác động gì đến INPUT-CHAT


Ah, bạn nói đúng! Khi click vào suggestion, nó thực sự gọi API endpoint này thông qua hàm `mindpalChatUserInputNodeExecution`:

```typescript:web/app/components/mindpal/workflow/visualizer/item/collapse-children-user-input/chat/chat-model/suggestions.tsx
const onSend = async (suggestion: string) => {
  setSuggestions([...[]])
  setIsResponding(true)

  // Update node executions
  setNodeExecutions((pre) => {
    return pre.map((ne) => {
      if (ne.node_id === nodeExecution.node_id) {
        return {
          ...ne,
          execution_metadata: {
            ...nodeExecution.execution_metadata,
            [variable]: [
              ...nodeExecution.execution_metadata[variable],
              { role: 'user', text: suggestion },  // Add suggestion to chat history
              { role: 'assistant', text: '' },
            ],
          },
        }
      }
      return ne
    })
  })

  // Call API to process suggestion
  const response = await mindpalChatUserInputNodeExecution(
    appId,
    treeNodes?.data?.provider_id as string, 
    treeNodes?.id,
    nodeExecution?.id,
    variable,
    { query: suggestion, inputs }  // Send suggestion as query
  )
}
```

Luồng xử lý khi click suggestion:
1. Gửi đến chatbot qua `window.chatbot?.sendMessageWindow`
2. Cập nhật chat history trong state
3. Gọi API endpoint `/chat` với suggestion như một query thông thường
4. API này xử lý giống như khi người dùng nhập message qua ChatInput

Vì vậy, suggestion được xử lý như một message bình thường, đi qua cùng một endpoint API như ChatInput, chỉ khác là không hiển thị trong input box.
