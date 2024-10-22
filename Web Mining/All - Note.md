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
- Use : Identify language patterns with potential for opinion expression) 
- Ví dụ: "xe đẹp", "đồ chơi bền", "rất vui".

### Bước 2: Xác Định Hướng Cảm Xúc

-  Compare whether that phrase often appears with the word "good" or "bad" in many other articles. (For example: "nice car" is more likely to go with "good" than "bad"). 
- Sso sánh xem cụm từ đó thường xuất hiện cùng với từ "tốt" hay "xấu" hơn trong rất nhiều bài viết khác. (Ví dụ: "xe đẹp" thường đi với "tốt" hơn là "xấu", nên "xe đẹp" là ý kiến ​​tốt).

### Bước 3: Kết Luận Cảm Xúc Chung

- Cuối cùng, chúng ta cộng tất cả các ý kiến ​​tốt và xấu lại.
- Nếu ý kiến ​​tốt nhiều hơn, bài viết có cảm xúc tích cực, nghĩa là món đồ chơi được đánh giá tốt.
- Ngược lại, nếu ý kiến ​​xấu nhiều hơn, bài viết có ​​cảm xúc tiêu cực, nghĩa là món đồ chơi bị đánh giá xấu.

### Áp dụng cho Tiếng Việt

- Các bước này cũng áp dụng được cho tiếng Việt.
- Chúng ta chỉ cần thay đổi từ "tốt" và "xấu" bằng các từ tương ứng trong tiếng Việt, ví dụ: "hay", "dở", "tệ".

**Tóm lại:** Phương pháp này giúp chúng ta tự động hiểu được cảm xúc của một bài viết về món đồ chơi mà không cần phải đọc và đánh giá từng ý kiến ​​một. [1-5]


Bổ sung về Toán: 
- Step by Step 'HOW TO CALCULATE PMI':
		1. **Đếm:** Đếm xem câu nói đó xuất hiện bao nhiêu lần trên mạng Internet.
		2. **Đếm cặp:** Đếm xem câu nói đó và từ "tốt" (hoặc "kém") xuất hiện **cùng nhau** bao nhiêu lần.
		3. **So sánh:** Nếu câu nói đó xuất hiện cùng "tốt" nhiều hơn "kém", thì câu nói đó là lời khen. Ngược lại, nếu câu nói đó xuất hiện cùng "kém" nhiều hơn "tốt", thì câu nói đó là lời chê.
	- Determine the similarity of two phrases based on the likelihood of co-occurrence on a large corpus: 
		- Large Text Set: Web Text
		- Possibility co-occurrence: Pointwise Mutual Information (PMI)
		- SO(t) = PMI(t; ‘tốt’) - PMI(t; ‘kém’)
	

		Then, VẬY THÌ CÔNG THỨC PMI() tính như nào? 
		Cách tính **PMI (Pointwise Mutual Information)** cho một từ t và một từ khác (ví dụ: từ "tốt" hoặc "kém") dựa trên xác suất của chúng trong tập văn bản lớn (corpus).

		Công thức PMI được tính như sau:
		$PMI(t, \text{"?"}) = \log \frac{P(t, \text{"?"})}{P(t) \cdot P(\text{"?"})}$

		Trong đó:
		- **P(t, "?"**) là xác suất của từ t và từ "?" cùng xuất hiện trong văn bản (xác suất đồng xuất hiện).
		- **P(t)** là xác suất xuất hiện của từ t.
		- **P("?")** là xác suất xuất hiện của từ "?" (ví dụ: từ "tốt" hoặc "kém").
		
		### Chi tiết tính toán:
		
		1. **Xác suất P(t)**:
		   $P(t) = \frac{\text{count}(t) + 1}{\sum_{t’} \text{count}(t’) + V}$
		   - **count(t)**: Số lần xuất hiện của từ t trong tập văn bản.
		   - **V**: Kích thước từ vựng (số từ khác nhau trong tập văn bản).
		
		2. **Xác suất đồng xuất hiện P(t, "?")**:
		  P(t, \text{"?"}) = $\frac{\text{count}(t, \text{"?"}) + 1}{\text{Tổng số lần xuất hiện của tất cả các cặp từ trong văn bản} + V}$
		   - **count(t, "?"**): Số lần t và "?" xuất hiện cùng nhau trong một câu hoặc đoạn văn.

	**Ví dụ:**
	- Câu nói: "Phim này hay quá!"
	- PMI("Phim này hay quá!"; "tốt") cao.
	- PMI("Phim này hay quá!"; "kém") thấp.
	- Kết luận: Câu nói mang cảm xúc tích cực (khen).
- tại sao tính PMI lại là công thức kia 
- và tại sao lúc tính P lại phải count + 1/ tổng số lần xuất hiện + V, V là gì ? 