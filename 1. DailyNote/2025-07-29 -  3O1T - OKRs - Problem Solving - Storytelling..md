# 1. [CHẠY BỘ LÀM FRONTEND KỶ LUẬT + REPORT CHUẨN CẤU TRÚC ĐƯỢC MANAGER CÓ LỜI KHEN (Đấy là em còn chưa xài công thức 1, 2, 3, 4 của sếp Huy) :D](https://primecircle.wecommit.com.vn/c/win-learn/ch-y-b-lam-frontend-k-lu-t-report-chu-n-c-u-truc-d-c-manager-co-l-i-khen-d-y-la-em-con-ch-a-xai-cong-th-c-1-2-3-4-c-a-s-p-huy-d)



![[Pasted image 20250729072711.png]]


```
[Report Chạy Luồng API Agent}

  

+, Vấn đề em gặp phải: Kết quả không đồng nhất giữa các lần chạy, đổi nhẹ Prompt có trường hợp không trả ra file .csv

=> RỦI RO TIỀM ẨN: VỚI CÙNG 1 PROMPT => KẾT QUẢ GIỮA CÁC LẦN CHẠY CÓ THỂ KHÁC NHAU và THẬM CHÍ LÀ KO TRẢ RA FILE output.csv như mong đợi.

+, Nguyên nhân - Giải pháp: ??

1. Do sự khác nhau giữa các lần AI trả ra kết quả (ảnh hưởng bởi tham số temperature) => thử fix cứng temperature = 0 để test thử.

2. Có thể có nhiều nguyên nhân khác, em đang hỏi thêm a Tuấn Anh ạ.

  

---

Dẫn chứng các lần chạy:

1. Chạy 10 dòng input cùng lúc dễ gặp lỗi, recommend 5 dòng input

https://pikasaia.stepup.edu.vn/?id=f9fc5448-fadc-4aa8-b6f8-179d1cf80f8b

https://pikasaia.stepup.edu.vn/?id=b4c54d29-de1c-4618-9e8a-4c0a834b0e1a

---

> 1. https://pikasaia.stepup.edu.vn/?id=f9fc5448-fadc-4aa8-b6f8-179d1cf80f8b

Chạy full 12 dòng input, ko add todo,

=> Output trả ra 1 loạt tầm 50 dòng đầu bị fail.

Tổng trả 600 dòng. - (12 dòng input * 10 topics (10 JTBD) * 5 scenario (Steps) )

=> Kết quả ko xài được

  

2. b4c54d29-de1c-4618-9e8a-4c0a834b0e1a

Chạy full 12 dòng input  + File Todo

=> Output chỉ trả ra 150 dòng.

  
  

2. Kết quả khá ngon khi chạy 5 dòng: https://pikasaia.stepup.edu.vn/?id=19806337-b265-482d-9bee-b321db65deb7

  

3. Đổi 1 xíu Prompt => Kết quả ko trả ra file output

Chạy y nguyên lại luồng trên đổi mỗi: An CSV file titled Workflow - Job role - (domain name). trong Prompt sang output.csv => kết quả là output ko trả ra file gì cả.

Dẫn chứng: <e để mất link>

  

4. Chạy 1 lúc 2 threads giống y nhau, kết quả khác nhau: (2 luồng này thì oke ạ)

- https://pikasaia.stepup.edu.vn/?id=58dddfed-f23a-4aad-bec7-a3b624e39c8e

_ https://pikasaia.stepup.edu.vn/?id=dbeeb1ff-0866-48dd-9f90-916295a398e4

  

---

  

Comment thêm:

-Hiện đã Key limit exceeded khả năng cao hết tiền ạ.  

- Phía anh Tuấn Anh vẫn có bug: Không trả ra được trực tiếp folder output(thời gian check bug) + cần lấy sessionID trong output để lắp tay vào UI để xem + thời gian chạy 1 lần 10 mins +  chỉnh config để auto continue
```


```
[Kết quả Super Agent bị thay đổi khi chạy cùng 1 Prompt với cùng 1 Input]

---

- Vấn đề: Việc cùng 1 Prompt + Cùng 1 Input => dẫn đến kết quả các lần chạy khác nhau, thậm chí có trường hợp không trả ra file output.csv anh ​@Tuan Anh Nguyen Dang​ ạ.
- Em muốn hỏi là: Có những tham số nào ảnh hưởng đến việc các lần chạy ra khác nhau ạ

(Ngoài temperature của model ra thì còn gì nữa không ạ, các tham số của các tool mình có kiểm soát được luôn không ạ)

anh ​@Tuan Anh Nguyen Dang​
```



---
# 2. Cách report theo framework: vấn đề - nguyên nhân - giải pháp - 
1. Vấn đề + Giá trị khi giải quyết
    
2. Nguyên nhân + Dẫn chứng
    
3. Giải pháp + Dẫn chứng
    
4. Người khác comment, xác nhận  
      
    —-  
    Vấn đề khác:

---



1. Sắp xếp các đầu việc bên task 
2. Chọn việc khó nhất làm trước, ưa thích giải quyết việc khó, đặc biệt là càng khó càng thích 
3. Tinh thần phụng sự tất cả ace, mindset lãnh đạo, thất bại của đồng đội là thất bại của tôi 

---
# 3. Lên task theo 3O1T - OKRs - Problem Solving - Storytelling. 

| **3O1T**                                                                                                                                                                    | **OKRs**                                     | 20250729                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅ **Objective**                                                                                                                                                             | Objective cảm hứng và hướng mục tiêu dài hạn | Đâu là mục tiêu quan trọng nhất trong ngày mà khi đạt được nó tôi woa vãi chưởng. <br>Thông được luồng chạy consistence từ Input chị Thủy -> qua bước a Vũ -> qua bước mình và đến được QC<br><br>và chạy thành công cho 5-10 groups khác nhau <br>---<br>Thông được luồng thì | **Thông luồng pipeline từ Input (chị Thủy) → a Vũ → Cường → QC** - 1 luồng Consistent 1 cách tối đa, và **chạy thành công cho 5–10 nhóm ngành khác nhau**. <br><br><br>Mindset: <br>- Phân biệt thành công với hạnh phúc. Thất bại với hạnh phúc là 2 thứ hoàn toàn độc lập với nhau. Thành công là đạt hơn 100% mục tiêu. <br>- Chơi để không thua hay chơi để thắng. <br>Với bên trong: mindset top trên, kẻ chiến thắng.<br>- Với bên ngoài: nhìn vào túi tiền của người khác là cảm xúc chi |
| 🎯 **Outcome**: Là _tác động_, _giá trị_ hoặc _thay đổi_ tạo ra nhờ các output.<br>- 📊 **Metrics**: tập trung đo **outcome** để đảm bảo nỗ lực của bạn thực sự có giá trị. | Why?                                         | 1. Thông được pipeline giúp đánh giá chất lượng của content gen build bài nhờ AI để sớm có những đánh giá về mặt content. <br>?? tại sao phải đánh giá chất lượng content sớm? Để có những phương án chính xác cho build bài hàng loạt về sau. <br>2. <br>                     | 1. Cho phép **đánh giá chất lượng content** được AI tạo ra ở bước đầu – từ đó đưa ra điều chỉnh kịp thời trước khi build hàng loạt.  <br>2. Giảm thiểu rủi ro QC về sau, đảm bảo luồng sản xuất trơn tru và có thể nhân rộng trên nhiều nhóm ngành nghề.                                                                                                                                                                                                                                        |
| 📦 **Output**: Là _sản phẩm_, _kết quả trực tiếp_ của công việc,<br>- ✔ **Define to Done**: checklist                                                                       | Key Results 1, 2, 3 cụ thể, đo lường được    | Sản phẩm bàn giao: <br>1. Kết quả sau khi đã được chạy qua toàn bộ pipeline.                                                                                                                                                                                                   | 1. Danh sách 5–10 nhóm bài mẫu đã chạy hoàn chỉnh qua luồng AI gen → a Vũ xử lý → mình xử lý → QC review.  <br>2. Tài liệu ghi lại quy trình rõ ràng để nhân rộng. <br>=> Mọi tài liệu cần được take note để dùng lại về sau. Dễ dàng hỏi AI và lên plan, lên outcome, output<br>3. Feedback chất lượng từ nhóm QC (tự mình QC, chị Thủy, a Vũ, ...)<br>                                                                                                                                        |
| 🧩 **Tasks**                                                                                                                                                                | 🧩Actions                                    |                                                                                                                                                                                                                                                                                | 1. Thêm phần down session vào code hiện tại để thực hiện việc ghép luồng. <br>(Check phần anh Tuấn Anh vẫn chưa được, đang phải xài cách thủ công quét UI)<br> <br>2. Còn gì nữa không: <br>- Phải đợi anh Tuấn Anh update về độ consisten số thứ => Trong thời gian này ghép xong luồng trước đi???<br><br>3. Chạy đánh giá thêm 3-5 nhóm nữa để test Prompt thêm. <br>4.                                                                                                                      |
| 1. Vấn đề + Giá trị khi giải quyết<br>    <br>                                                                                                                              |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 2. Nguyên nhân + Dẫn chứng<br>    <br>                                                                                                                                      |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 3. Giải pháp + Dẫn chứng                                                                                                                                                    |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 4. Người khác recommend                                                                                                                                                     |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|                                                                                                                                                                             |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Result (Hook: ở đây có ai muốn đạt được điều gì đó)                                                                                                                         |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Situation                                                                                                                                                                   |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Think (nghĩ, cảm thấy Feel, <br>vì sao đặt câu hỏi phản biện Nếu ) - 80-20                                                                                                  |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Action                                                                                                                                                                      |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Results                                                                                                                                                                     |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Call to action                                                                                                                                                              |                                              |                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
