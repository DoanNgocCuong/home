![[Pasted image 20250729200756.png]]


![[Pasted image 20250729202531.png]]


![[Pasted image 20250729202912.png]]


---
1. Video được chunk nhỏ ra và upload từng đoạn => Youtube có, bảo sao up đến 1 đoạn mà gãy thì nó vẫn upload được. 
2. Video được upload lên bằng Pre-signed URLs Approach 


![[Pasted image 20250729203938.png]]


```
Em có câu hỏi:  
Em đang được giao 1 bài search DB.  

- case dễ nhất: search theo từ khóa -> e triển rồi  
    
- case khó hơn sếp đang muốn:  
    

+, là search các từ khác nó vẫn recommend đúng  
(chẳng hạn: trong DB ghi Project Manager -> user search PM, search quarn lý dự án, ... vẫn ra, ...) càng nhanh càng tốt ạ  
  
+, Em phân vân đoạn này thường các anh và mn thường xử lý như nào ạ.  
(AI là 1 cách cơ mà em thấy nó hơi chậm,  
còn 1 cách mapping sẵn các từ khóa thì cần define đủ còn lệch thì lại chịu ạ)
```