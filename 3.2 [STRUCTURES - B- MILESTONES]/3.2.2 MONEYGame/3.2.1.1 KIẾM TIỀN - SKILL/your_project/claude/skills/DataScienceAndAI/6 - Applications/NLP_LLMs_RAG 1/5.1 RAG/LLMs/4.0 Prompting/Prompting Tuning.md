khá chuẩn ạ.  
Trong thực tế các bài Prompting phải tuning khá nhiều.  
Mục tiêu là đảm bảo:  
1. độ chính xác (đúng luồng, chính xác, không bịa) (model to thì chính xác cao nhưng tốc độ gen lại chậm, model bé thì độ thông minh không cao)  
2. tốc độ phản hồi (nhiều bài đòi hỏi <50-100ms, 500ms, 1s), (với agent điều hướng thì đòi hỏi vừa chính xác cao nhưng vừa phải nhanh siêu nhanh, …)  
3. chi phí (model to như gpt4.1, claude thì ngon nhưng đắt gấp 3-10 lần model nhỏ như 4o-mini)  
  
Nhiều khi 1 prompt cả đội phải tối ưu cả ngày/ cả tuần xoay nhiều cách.  
(Công ty em có con Robot, ae tối ưu Prompt sao cho  
4. Nhét được cả memory, thông tin cá nhân của trẻ, …  
5. Vào luồng bài học sao cho đi đúng luồng mà vẫn phải đảm bảo response time <500ms-1s , … +  
6. chưa kể đến bài toán chi phí)  
=> Riêng bài này ông Prompt Engineering ở công ty em ngồi với ae Content, PM, CEO ngồi cả tuần.