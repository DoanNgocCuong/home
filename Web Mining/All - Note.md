# OPINION WEBMING: 
Opinion mining is about understanding what people think about products, services, or anything else. Here’s a simple explanation for each problem:

1. **Sentiment Analysis**: This is figuring out if a comment or review is saying something good, bad, or just neutral (neither good nor bad). For example, “BPhone 3, chất đến từng chi tiết” is a positive comment.

2. **Opinion Summarization**: This is about summarizing reviews by identifying what people are talking about (the “aspect”) and whether they feel positive, negative, or neutral about each part of the product.

3. **Comparative Opinions**: Sometimes people compare two or more things, like saying “Object A is better than Object B” or “I like object A more than others.”

4. **Opinions Searching**: This is about finding what people are saying about a certain object or product when we search online (group or forum, ...).

5. **Opinions Filtering**: This is sorting out fake or misleading comments, like some people writing fake good reviews (hype spam) or fake bad reviews (defaming spam).

## Methods of Sentiment Analysis 
![[Pasted image 20241022112012.png]]

 ### UNSUPERVISED:  Phân tích Cảm xúc Không Giám sát - Giải thích cho Học sinh Lớp 3

Bài toán này giống như việc chúng ta muốn biết một bài viết nói về một món đồ chơi là tốt hay xấu mà không cần ai nói trước cho chúng ta biết.

### Bước 1: Tìm Cụm Từ Biểu Lộ Ý Kiến

- Đầu tiên, chúng ta tìm những cụm từ trong bài viết thể hiện ý kiến về món đồ chơi đó.
- Ví dụ: "xe đẹp", "đồ chơi bền", "rất vui".

### Bước 2: Xác Định Hướng Cảm Xúc

- Tiếp theo, chúng ta cần biết mỗi cụm từ đó là tốt hay xấu.
- Chúng ta so sánh xem cụm từ đó thường xuất hiện cùng với từ "tốt" hay "xấu" trong rất nhiều bài viết khác.
- Ví dụ: "xe đẹp" thường đi với "tốt" hơn là "xấu", nên "xe đẹp" là ý kiến ​​tốt.

	Để hiểu cảm xúc của một câu nói, chúng ta cần biết người nói đang khen hay chê.
	
	**Giả sử:**
	- "Tốt" là lời khen.
	- "Kém" là lời chê.
	
	Bây giờ, muốn biết một câu nói là khen hay chê, ta làm như sau:
	
	1. **Đếm:** Đếm xem câu nói đó xuất hiện bao nhiêu lần trên mạng Internet.
	2. **Đếm cặp:** Đếm xem câu nói đó và từ "tốt" (hoặc "kém") xuất hiện **cùng nhau** bao nhiêu lần.
	3. **So sánh:** Nếu câu nói đó xuất hiện cùng "tốt" nhiều hơn "kém", thì câu nói đó là lời khen. Ngược lại, nếu câu nói đó xuất hiện cùng "kém" nhiều hơn "tốt", thì câu nói đó là lời chê.
		
	**Công thức Toán:**
	
	PMI(t1; t2) = log2(P(t1, t2) / (P(t1) * P(t2)))
	
	Trong đó:
	
	- t1: Câu nói cần xác định cảm xúc.
	- t2: Từ "tốt" hoặc "kém".
	- PMI: Điểm đo lường sự liên quan giữa t1 và t2.
	- P(t1, t2): Xác suất t1 và t2 xuất hiện cùng nhau.
	- P(t1): Xác suất t1 xuất hiện.
	- P(t2): Xác suất t2 xuất hiện.
	
	**Ví dụ:**
	
	- Câu nói: "Phim này hay quá!"
	- PMI("Phim này hay quá!"; "tốt") cao.
	- PMI("Phim này hay quá!"; "kém") thấp.
	- Kết luận: Câu nói mang cảm xúc tích cực (khen).
### Bước 3: Kết Luận Cảm Xúc Chung

- Cuối cùng, chúng ta cộng tất cả các ý kiến ​​tốt và xấu lại.
- Nếu ý kiến ​​tốt nhiều hơn, bài viết có cảm xúc tích cực, nghĩa là món đồ chơi được đánh giá tốt.
- Ngược lại, nếu ý kiến ​​xấu nhiều hơn, bài viết có ​​cảm xúc tiêu cực, nghĩa là món đồ chơi bị đánh giá xấu.

### Áp dụng cho Tiếng Việt

- Các bước này cũng áp dụng được cho tiếng Việt.
- Chúng ta chỉ cần thay đổi từ "tốt" và "xấu" bằng các từ tương ứng trong tiếng Việt, ví dụ: "hay", "dở", "tệ".

**Tóm lại:** Phương pháp này giúp chúng ta tự động hiểu được cảm xúc của một bài viết về món đồ chơi mà không cần phải đọc và đánh giá từng ý kiến ​​một. [1-5]
