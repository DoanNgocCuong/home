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


![[Pasted image 20250729210524.png]]


![[Pasted image 20250729211025.png]]


![[Pasted image 20250729212049.png]]


![[Pasted image 20250729212440.png]]


Các sếp cho em hỏi  
  
Trong ví dụ vừa rồi,  

- nếu user search tiếng anh 'noodles' thì xử lý như nào ạ  
    
- nếu user search sai chính tả 'mua'

---
```
[Bài toán Search trong DB cố định]
Các sếp ơi, em đang tìm lời giải cho bài này
---
Cục DB cố định chẳng hạn có: keyword: Project Manager.  Search mục tiêu là tìm được data 'Project Manager'
+, Case 1: user search có kí tự: Pro, ... => DB hỗ trợ, em đã triển xong 
+, Case 2: user search: PM, quản lý dự án, ... => Sử dụng 1 bảng mapping các từ thường gặp với cụm => Khổ cái là cần define làm sao để nó cover được hết các cases. 
+, Case 3: User search linh tinh: quản lý quản các dự án, manager Product, ... manager dự án, ... Rồi thì sai chính tả: quản dự án, Prod Mager, ... => thì trường hợp này mn thường xử lý  như nào ạ. 

-------
Em xin phép tag nhẹ nhờ sếp @q… , sếp @x…  ạ :3
```

```
Em vẫn câu hỏi ban nãy ạ :D  
--  
  
[Bài toán Search trong DB cố định]  
Các sếp ơi, em được giao bài toán sau.  
---  
Cục DB cố định chẳng hạn có: keyword: Project Manager  
- Search mục tiêu là tìm được data 'Project Manager'  
  
+, Case 1: user search có kí tự: Pro, ... => DB hỗ trợ, em đã triển xong  
+, Case 2: user search: PM, quản lý dự án, ... => Sử dụng 1 bảng mapping các từ thường gặp với cụm => Khổ cái là cần define làm sao để nó cover được hết các cases.  
+, Case 3: User search linh tinh: quản lý quản các dự án, manager Product, ... manager dự án, ... Rồi thì sai chính tả: quản dự án, Prod Mager, ... => thì trường hợp này mn thường xử lý  như nào ạ.
```


```
Em chào các sếp và các ace ạ. Em đang tìm cách giải bài này (được sếp giao mấy hôm nay chuẩn bị cho con sản phẩm lên Product thật ạ).  
Xin tham vấn từ các sếp và ace cùng thảo luận ạ.  
  
[Bài toán Search trong DB cố định]  
Cục DB cố định chẳng hạn có: keyword: Project Manager  
- Search mục tiêu là tìm được data 'Project Manager'  
  
+, Case 1: user search có kí tự: Pro, ... => DB hỗ trợ, em đã triển xong  
+, Case 2: user search: PM, quản lý dự án, ... => Sử dụng 1 bảng mapping các từ thường gặp với cụm => Khổ cái là cần define làm sao để nó cover được hết các cases.  
+, Case 3: User search linh tinh: quản lý quản các dự án, manager Product, ... manager dự án, ... Rồi thì sai chính tả: quản dự án, Prod Mager, ... => thì trường hợp này mn thường xử lý  như nào ạ. Em tính đưa con AI vào mà nó làm tốc độ search bị giảm đi.  
  
Em xin phép tag các sếp ạ. sếp , sếp , sếp  
Anh anh :D  
Em cảm ơn mn ạ :D  
  
#cung_giai_bai_tap :D
```