# 6. OPINION WEBMING: 
Opinion mining is about understanding what people think about products, services, or anything else. Here’s a simple explanation for each problem:

1. **Sentiment Analysis**: This is figuring out if a comment or review is saying something good, bad, or just neutral (neither good nor bad). For example, “BPhone 3, chất đến từng chi tiết” is a positive comment.

2. **Opinion Summarization**: This is about summarizing reviews by identifying what people are talking about (the “aspect”) and whether they feel positive, negative, or neutral about each part of the product.

3. **Comparative Opinions**: Sometimes people compare two or more things, like saying “Object A is better than Object B” or “I like object A more than others.”

4. **Opinions Searching**: This is about finding what people are saying about a certain object or product when we search online (group or forum, ...).

5. **Opinions Filtering**: This is sorting out fake or misleading comments, like some people writing fake good reviews (hype spam) or fake bad reviews (defaming spam).

## 6.1 Methods of Sentiment Analysis 
![[Pasted image 20241022112012.png]]

### IMPORTANCE UNSUPERVISED:  Phân tích Cảm xúc Không Giám sát - Giải thích cho Học sinh Lớp 3

Bài toán này giống như việc chúng ta muốn biết một bài viết nói về một món đồ chơi là tốt hay xấu mà không cần ai nói trước cho chúng ta biết.

- Bước 1: Tìm Cụm Từ Biểu Lộ Ý Kiến
	- Use : Identify language patterns with potential for opinion expression) 
	- Ví dụ: "xe đẹp", "đồ chơi bền", "rất vui".
- Bước 2: Xác Định Hướng Cảm Xúc
	-  Compare whether that phrase often appears with the word "good" or "bad" in many other articles. (For example: "nice car" is more likely to go with "good" than "bad"). 
	- Sso sánh xem cụm từ đó thường xuất hiện cùng với từ "tốt" hay "xấu" hơn trong rất nhiều bài viết khác. (Ví dụ: "xe đẹp" thường đi với "tốt" hơn là "xấu", nên "xe đẹp" là ý kiến ​​tốt).
	- Step by Step: 
		1. **Đếm:** Đếm xem câu nói đó xuất hiện bao nhiêu lần trên mạng Internet.
		2. **Đếm cặp:** Đếm xem câu nói đó và từ "tốt" (hoặc "kém") xuất hiện **cùng nhau** bao nhiêu lần.
		3. **So sánh:** Nếu câu nói đó xuất hiện cùng "tốt" nhiều hơn "kém", thì câu nói đó là lời khen. Ngược lại, nếu câu nói đó xuất hiện cùng "kém" nhiều hơn "tốt", thì câu nói đó là lời chê.
- Bước 3: Từ đó đưa ra kết luận. 
	- **Ví dụ:** Câu nói: "Phim này hay quá!"
	- PMI("Phim này hay quá!"; "tốt") cao.
	- PMI("Phim này hay quá!"; "kém") thấp.

VỀ TOÁN: 
- Step by Step 'HOW TO CALCULATE PMI':

	1. Determine the similarity of two phrases based on the likelihood of co-occurrence on a large corpus: 
		- Large Text Set: Web Text
		- Possibility co-occurrence: Pointwise Mutual Information (PMI)
		- SO(t) = PMI(t; ‘tốt’) - PMI(t; ‘kém’)
	
	2. Then, VẬY THÌ CÔNG THỨC PMI() tính như nào? 
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
	


- **Tại sao tính PMI lại là công thức kia, tại sao lại là P(t) * P(?) và tại sao lúc tính P lại phải count + 1/ tổng số lần xuất hiện + V, V là gì ? **   => GPT for detail. 
	- **P(t)⋅P(?)P(t) \cdot P(?)P(t)⋅P(?)** chính là cách đo **mức độ ngẫu nhiên**: Nếu từ ttt và từ ??? xuất hiện ngẫu nhiên, không liên quan đến nhau, thì xác suất chúng xuất hiện cùng nhau chỉ đơn giản là tích của xác suất từng từ xuất hiện riêng lẻ.
	- P(t,?), tức là xác suất đồng xuất hiện thực tế,

## 6.2 SOT - Sentinment Ontology Tree

1. explain for child: 
- Hãy nghĩ về SOT như một **cây gia đình** cho ý kiến về sản phẩm.
- **Gốc cây** là sản phẩm bạn quan tâm, ví dụ như điện thoại.
- **Các nhánh cây** là các đặc điểm của sản phẩm, ví dụ như màn hình, pin, camera.
- **Lá cây** là ý kiến ​​của mọi người về những đặc điểm đó.
    - **Lá xanh:** Ý kiến ​​tích cực, ví dụ như "màn hình đẹp", "pin lâu".
    - **Lá đỏ:** Ý kiến ​​tiêu cực, ví dụ như "camera mờ", "giá cao".
2. While SOT offers a robust solution for fine-grained sentiment analysis and is well-regarded for certain research purposes, its broader adoption is limited by its complexity and lack of widespread tool support.