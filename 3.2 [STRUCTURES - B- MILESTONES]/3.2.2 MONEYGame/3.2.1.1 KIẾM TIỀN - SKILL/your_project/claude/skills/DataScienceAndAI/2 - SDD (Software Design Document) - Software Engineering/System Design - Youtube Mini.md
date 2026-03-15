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


```
Có nên “clone” lại các SaaS product của nước ngoài?

--

ĐÔI KHI BẠN CẦN HỌC CÁCH “THIẾT KẾ BÁNH XE”

Hầu hết các bậc đàn anh đàn chị (seniors) đều có 1 lời khuyên đại loại như “đừng bao giờ thiết kế lại bánh xe” (Do not reinvent the wheel), ý nói cái nào người ta làm rồi thì mình mang về tìm cách dùng thôi, ngồi làm lại làm cái gì cho mất thời gian công sức, mà chắc gì ngon được như mấy cái ngoài kia.

Điều này đúng, nhưng chưa đủ...

Bạn còn chưa biết cách làm ra cái bánh xe như thế nào, thì làm sao ráp nó vào cả một bộ khung bộ máy được?

Khi bạn “thiết kế lại bánh xe”, 99% cái bánh xe của bạn sẽ không ngon như những cái có trên thị trường. Nhưng bạn cần phải làm điều đó, vì điểm mấu chốt ở đây ko phải là cái bánh xe, nó là kiến thức lẫn kinh nghiệm bạn có được sau khi làm điều này.

--

XÁC NHẬN Ý TƯỞNG ĐÃ ĐƯỢC KIỂM CHỨNG

Đây thường là phần khó nhất của một indie maker giai đoạn đầu.

Nếu bạn đang tham gia vào một thị trường lớn với nhiều sản phẩm hiện có, nếu chọn phương án "copy", điều này (idea validation) về cơ bản đã được thực hiện cho bạn. Bạn có thể bỏ qua một bước rất tốn thời gian.

Một phần nhỏ của một thị trường lớn có thể là tất cả những gì bạn cần - và thường thì nó có thể lớn hơn nhiều so với thị trường mà bạn đã cố gắng tự tạo ra.

Thị trường VN còn mới, SaaS chỉ đang trong giai đoạn đầu, chỗ trống sẽ còn rất nhiều cho bạn lấp đầy.

Tuy nhiên, cũng cần lưu ý rằng: MỚI chứ không hề DỄ nhé! Vì mindset người Việt chưa quen với việc mua phần mềm dịch vụ như bên nước ngoài, trong một vài năm gần đây thì mình thấy việc này đang bắt đầu thay đổi dần rồi.

--

LÀM THẾ NÀO CẠNH TRANH VỚI CÁC “ĐỐI THỦ” LỚN?

Các đối thủ cạnh tranh lớn không có bất kỳ lợi thế công nghệ nào - ngày nay tất cả chúng ta đều đang sử dụng cùng một công nghệ như các công ty lớn.

Cuộc đua không còn bất kỳ lợi thế kỹ thuật cụ thể nào nữa.

Các sản phẩm của họ rồi sẽ trở nên cồng kềnh, hoặc họ tiến lên thị trường lớn hơn, xa rời các khách hàng SME (doanh nghiệp vừa & nhỏ).

Hơn nữa, hầu hết bọn họ đều ko xem bạn là “đối thủ” đâu.

--

“SAO CHÉP SAU ĐÓ BÁN GIÁ RẺ HƠN! EZVL”

Đừng. Xin đừng làm điều đó đối với sản phẩm của indie maker VN ![🥺](https://static.xx.fbcdn.net/images/emoji.php/v9/t9b/1/16/1f97a.png)

Điều này sẽ để lại hệ quả rất tệ cho chính bạn & cả cho cộng đồng indie maker VN.

Bạn nghĩ bạn copy lại sản phẩm của người khác và bán giá rẻ hơn thì ngay lập tức bạn sẽ chiếm lĩnh được thị trường sao? Trên thực tế, có rất nhiều người/tập thể/thậm chí doanh nghiệp đã áp dụng chiến lược này. Hầu hết đều không thành công như mong đợi.

Cạnh tranh về giá chỉ đưa đến kết cục tệ hại mà thôi. Đấy là chưa nói đến việc bạn đang đi sao chép người khác.

Thử tưởng tượng “lỡ may” bạn thực sự kiếm được nhiều khách hàng bằng cách này, bạn sẽ tạo được sự chú ý trên thị trường, liệu có ai trong số đó không phát hiện ra sản phẩm của bạn là sao chép? Tất cả mọi thứ sẽ đổ sông đổ bể khi có crisis xảy ra, bạn có sẵn sàng chấp nhận điều này?

Nếu bạn làm như vậy, bạn đang đi ngược lại với ý nghĩa của việc trở thành một indie maker.

Indie maker không cạnh tranh lẫn nhau, mà cùng hỗ trợ nhau trong quá trình “build in public”.

VÌ MỘT CỘNG ĐỒNG PHẦN MỀM VIỆT NAM KHÔNG CÒN MANH MÚN & XÉ LẺ NỮA!

(Thế nhưng, việc copy sản phẩm nước ngoài để bán "rẻ hơn" tại thị trường VN thì theo mình là một ý không tồi, rõ ràng mức sống tại VN thấp hơn nhiều so với nước ngoài, làm lương VN thì phải dùng dịch vụ giá VN chứ đúng không nè?)

Thay vào đó…

--

HÃY TẠO RA CÁC “BIẾN THỂ”

Cuốn sách Nghệ thuật "đánh cắp" ý tưởng (tác giả Austin Kleon) - là một cuốn sách rất hay nói về chủ để này mà mình nghĩ các bạn nên tìm đọc, sách ngắn gọn có hình minh họa dễ hiểu (đọc nhanh lắm đừng có lườiiii), link sách mình để ở cuối bài (tui không có PR cho nhà sách đâu à nha).

“Nguyên bản là gì? Đạo nhái không bị phát hiện” - William Ralph Inge

(What is originality? Undetected plagiarism.)

Trên đời này không có gì là nguyên bản, hầu hết ý tưởng đều được “truyền cảm hứng” và “biến tấu” lại để trở thành một phiên bản mới phù hợp với một mục đích khác - một “biến thể”.

Bạn có quyền sao chép, nhưng đừng sao chép 100%, hãy biến tấu nó bằng cách thêm những “gia vị” của riêng bạn, để tạo thành một món mới và sẵn sàng nói về chúng một cách tự hào.

Ví dụ hen:

• Ứng dụng todo → nếu bạn tạo 1 ứng dụng Todo nữa và ko có gì đặc biệt → không cần nói nhiều, 99% bạn sẽ fail!

• Thử cách này nhé: tạo ra ứng dụng Todo dành riêng cho cộng đồng “wibu” → cho phép cá nhân hóa với hình nền hay icon anime, sound effect ứ ứ é é như anime các thứ → bán các option premium cho customize cao cấp hơn như mỗi lần remind thì nhân vật đặc biệt nào đó xuất hiện + effect nổ đùng đùng chẳng hạn!

Bạn nghĩ ý tưởng này như thế nào?

Đó là lý do cụm từ “niche market” (thị trường ngách) ra đời.

Tạm quên cái bánh lớn đi, ai cũng muốn tranh giành miếng bánh đó, để họ đánh nhau, hãy tìm ra miếng bánh nhỏ của riêng bạn & ăn một mình!

--

“ÔNG GOON ĐI XÚI BÀ CON ĐI SAO CHÉP NGƯỜI KHÁC”

Haha, mình còn tệ hơn nữa ấy chứ. Biết tại sao ko?

Khi copy sản phẩm của người khác, khả năng cao bạn sẽ thất bại, bởi vì bạn ko phải là người đó, người xây dựng nên sản phẩm đó.

Nhưng theo mình, đây là 1 kiểu thất bại tích cực, cứ thử rồi sai rồi lại thử, bạn sẽ thấy mình tiến bộ hơn qua mỗi lần như thế. Cuối cùng bạn sẽ tạo ra được chất riêng của mình.

Mình muốn các bạn trải qua việc thất bại này, để hiểu được ý nghĩa thực sự của việc “build in public”:

“It will never about your product. It’s all about the process.”

Chúc các bạn một tuần mới tràn đầy năng lượng!

--

Các bài viết liên quan:

1. Thời điểm nào thì nên khởi nghiệp?

[https://www.facebook.com/story.php?id=1010276030&story_fbid=10228638758606468](https://www.facebook.com/mrgoonie/posts/pfbid02awnffqNBebiQLn5JeUEUErKPBPq4ANiL2Uv9fnXkHZLMELkiuAKkPNZc8Gxo4Qcdl?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

2. INDIE MAKER - Lối thoát cho lập trình viên?

[https://www.facebook.com/story.php?story_fbid=10228736204482554&id=1010276030](https://www.facebook.com/mrgoonie/posts/pfbid0kfy8i3E5372hPZ3CfsrJF47A29Cnh7YQVa8jSYZgPhNYFwKZPiVZeuwDcthg3GVwl?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

3. Những kỹ năng cầng có của INDIE MAKER

[https://www.facebook.com/story.php?id=1010276030&story_fbid=10228785219827907](https://www.facebook.com/mrgoonie/posts/pfbid02ZuHZ2nt9ArWRJCFNEr9zFUgQvmwsu79A1K7qdofxgm8i3NNVAC8eQ9qHDJJEUemyl?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

4. Danh sách những INDIE MAKER truyền cảm hứng

[https://www.facebook.com/story.php?id=1569314343856132&story_fbid=1569421353845431](https://www.facebook.com/groups/indiehackervn/posts/1569421353845431/?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

5. Cải thiện kỹ năng giao tiếp để trở thành INDIE MAKER

[https://www.facebook.com/story.php?id=1010276030&story_fbid=10228795277919353](https://www.facebook.com/mrgoonie/posts/pfbid0mMB8a2pGASvV8aRg8GUUoLTB2yDxeRJgE6Ziw35gvW1etUCnskkvRjwnMEHuQX59l?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

6. OVER-ENGINEER: Gốc rễ của mọi tội lỗi

[https://www.facebook.com/mrgoonie/posts/10228920865218957](https://www.facebook.com/mrgoonie/posts/pfbid0DnGVrJge3avXZtCkarEoxXxs6jDEqTjM6EvtpmTtMHZBwgCzWqRKg4Sv4uwcSX4Ql?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

7. Mẹo để tìm kiếm và validate ý tưởng phần mềm

[https://www.facebook.com/story.php?id=1010276030&story_fbid=10228963532125603](https://www.facebook.com/mrgoonie/posts/pfbid0WztJDVyq4LJZg1G2rj7Qoy7aUDewjwqFGU3BWuPZuuTCndn67U4CJFcukzaWiwoxl?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R)

![🌟](https://static.xx.fbcdn.net/images/emoji.php/v9/te0/1/16/1f31f.png) Follow [Duy Nguyen](https://www.facebook.com/mrgoonie?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-]K-y-R) hoặc tham gia group [Build in public VN](https://www.facebook.com/groups/indiehackervn/?__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=-UK-y-R) để cùng thảo luận thêm nhé.

—

![👉](https://static.xx.fbcdn.net/images/emoji.php/v9/t51/1/16/1f449.png) Link sách: [https://tiki.vn/product-p77109209.html?spid=77109210](https://tiki.vn/product-p77109209.html?spid=77109210&fbclid=IwZXh0bgNhZW0CMTAAYnJpZBExb2Q4ajJiMDFUaTRwS3Y3NAEe6W3gnGHLQMWSFvjNDeTOrUVbms6CNflj15M1xpmq2pO2aS8tBEMmOFHrCAc_aem_zRIT1wtx71tD_8hIrZW4mw)

[#buildinpublicvn](https://www.facebook.com/hashtag/buildinpublicvn?__eep__=6&__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=*NK-y-R) [#indiehackervn](https://www.facebook.com/hashtag/indiehackervn?__eep__=6&__cft__[0]=AZW-oADntvmmxU5rOVk7ivyV2qe1XY868qt8r5NAgo66H69HP1Ld9Th3SCcTdK5gTl-V1whEKeTW6WCR5Vi1Wrp7f4BgyFIbeS--7gncd3RM_Ba2xJ_msP4rzLN5sI_Bf7dkDcl0j-hRHKPYjjMHpWW8wuQHM-gBbF5KsJENyWRPyQZXF18QskSuhzDFie2sbv2K1RmPGDXfV2XcYCOuBgnDnamCQ3h0Gtuu71poBYzPQn1CvSJPm3xCuXrtxjNXpG4&__tn__=*NK-y-R)
```