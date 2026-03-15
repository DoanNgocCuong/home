https://adityamangal98.medium.com/solving-memory-leaks-in-python-applications-debugging-with-tracemalloc-and-heapy-7887ea4d6173

  
## Nguyên nhân gốc rễ: HTTP Client Session Leak  
  
### Phân tích  
  
Mỗi webhook call tạo nhiều HTTP requests:  

1 webhook call =   
  ├── InitConversation → callAPIInitConversation (1 HTTP request)  
  ├── GenMaterialNode → call_api_get_user_profile (1 HTTP request)    
  ├── WebhookNode → callAPIWebhook (1 HTTP request)  
  └── ExtractFacts/Summary → call_api_extract_facts (1 HTTP request)  
  
= 3-4 HTTP requests per webhook call  

  
Mỗi HTTP request tạo `ClientSession` mới:  

python  
# bot.py:163, 171 - Mỗi request tạo session mới  
async with aiohttp.ClientSession() as session:  
    async with session.post(...) as response:  
        ...  

  
### Tại sao đây là root cause  
  
1. Tác động lớn:  
   - Mỗi `ClientSession` = ~500KB-1MB (SSL context + TCP connections)  
   - Với 1000 webhook calls = 3000-4000 sessions = 1.5-4GB RAM  
   - Với 10,000 webhook calls = 30,000-40,000 sessions = 15-40GB RAM  
  
2. Giữ memory lâu:  
   - Mỗi session mở TCP connections đến remote servers  
   - Nếu exception/timeout → connections không được đóng ngay  
   - OS giữ TCP connections trong TIME_WAIT → memory không được release  
   - Python GC không thể release connections đang được OS giữ  
  
3. Tăng theo traffic (exponential):  
     

   Traffic tăng → Sessions tăng → Connections tăng → Memory tăng exponential  
     

  
4. Pattern phù hợp với memory spike:  
   - Ổn định → tăng đột ngột → exponential  
   - Phù hợp với pattern connection leak  
  
---