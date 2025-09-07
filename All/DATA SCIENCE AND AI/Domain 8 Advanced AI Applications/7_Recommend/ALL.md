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



```
IE architecture

IE problems

NER: CRF, LSTM

Relation extraction - Snowball --- Distant supervision

Coreperence resolution
```

Snowball: 

### Giải Thích Phương Pháp Snowball Đơn Giản cho Học Sinh Cấp 2

**Phương pháp Snowball** là một cách mà máy tính sử dụng để tìm hiểu và nhận diện các mối quan hệ giữa các từ hoặc cụm từ trong văn bản. Hãy tưởng tượng bạn đang xây dựng một **cái vòng tuyết** (snowball) từ những hạt tuyết nhỏ. Mỗi hạt tuyết thêm vào sẽ làm cho vòng tuyết trở nên lớn hơn và mạnh mẽ hơn. Tương tự, phương pháp Snowball bắt đầu từ một vài ví dụ nhỏ và dần dần mở rộng để nhận diện nhiều mối quan hệ hơn.

#### **Ví dụ Minh Họa:**

Giả sử bạn muốn dạy máy tính nhận biết mối quan hệ "tác giả viết sách".

1. **Bước 1: Bắt Đầu với Ví Dụ Ban Đầu (Seed Words)**
    
    - Bạn cung cấp cho máy tính một vài câu mẫu chứa mối quan hệ này, chẳng hạn:
        - "J.K. Rowling viết Harry Potter."
        - "George Orwell viết 1984."
2. **Bước 2: Tìm Các Mẫu Câu (Pattern)**
    
    - Máy tính sẽ nhận ra rằng trong các câu trên, từ "viết" thường xuất hiện giữa tên tác giả và tên sách.
    - Như vậy, mẫu câu có thể là: "**[Tên Tác Giả] viết [Tên Sách]**".
3. **Bước 3: Mở Rộng Tìm Kiếm**
    
    - Dựa vào mẫu câu này, máy tính sẽ quét toàn bộ văn bản để tìm thêm các câu có cấu trúc tương tự.
    - Ví dụ:
        - "Agatha Christie viết Mật Mã Da Vinci."
        - "Haruki Murakami viết Kafka bên bờ biển."
4. **Bước 4: Xác Nhận và Mở Rộng Mối Quan Hệ**
    
    - Khi máy tính tìm thấy nhiều ví dụ hơn, nó sẽ hiểu rõ hơn về mối quan hệ "tác giả viết sách" và có thể nhận diện được nhiều câu hơn mà không chỉ giới hạn trong những ví dụ ban đầu.

#### **Ưu Điểm của Phương Pháp Snowball:**

- **Đơn Giản:** Dễ hiểu và dễ triển khai.
- **Tự Động Mở Rộng:** Có khả năng tìm kiếm và nhận diện nhiều mối quan hệ mới dựa trên những gì đã học.

#### **Hạn Chế:**

- **Phụ Thuộc Vào Ví Dụ Ban Đầu:** Nếu các ví dụ ban đầu không đủ đa dạng, máy tính có thể bỏ sót nhiều mối quan hệ quan trọng.
- **Dễ Bị Lạc Đường:** Có thể tìm thấy các mối quan hệ không chính xác nếu không kiểm soát chặt chẽ.

#### **Tóm Lại:**

Phương pháp Snowball giống như việc bạn bắt đầu từ một hạt tuyết nhỏ và dần dần xây dựng thành một vòng tuyết lớn hơn. Bằng cách bắt đầu với một vài ví dụ, máy tính có thể tự động tìm kiếm và nhận diện nhiều mối quan hệ hơn trong văn bản. Đây là một công cụ hữu ích giúp máy tính hiểu ngôn ngữ tự nhiên và trích xuất thông tin quan trọng từ các đoạn văn bản lớn.


### Understanding the Snowball Method in Information Extraction

The **Snowball method** is a technique used in **Relation Extraction**, a subfield of **Information Extraction (IE)** in Natural Language Processing (NLP). Its primary goal is to identify and classify relationships between entities (like people, organizations, locations) within large volumes of text. Here's a breakdown of what the Snowball method does and how it operates:

#### **1. Purpose of the Snowball Method**

- **Identify Relationships:** The Snowball method is designed to discover and extract specific types of relationships between entities in text. For example, identifying that "Albert Einstein **developed** the theory of relativity" establishes a "developer-of" relationship between "Albert Einstein" and "the theory of relativity."
    
- **Expand Knowledge Bases:** By extracting relationships from vast amounts of text, the Snowball method helps in building and enriching structured databases or knowledge graphs, which can be used for various applications like search engines, recommendation systems, and question-answering systems.
    

#### **2. How the Snowball Method Works**

The Snowball method is primarily **rule-based** and operates through iterative pattern matching and expansion. Here's a step-by-step overview:

##### **a. Start with Seed Patterns and Examples**

- **Seed Patterns:** Begin with a few predefined patterns that represent the relationship you're interested in extracting. For instance, to extract "author-of" relationships, seed patterns might include:
    - "[Author] **wrote** [Book]"
    - "[Author] **authored** [Novel]"
- **Seed Examples:** Provide initial examples that fit these patterns:
    - "J.K. Rowling **wrote** Harry Potter."
    - "George Orwell **authored** 1984."

##### **b. Pattern Matching and Extraction**

- **Scan Text:** Use the seed patterns to scan large corpora (collections of text) and identify sentences that match these patterns.
    
- **Extract Relationships:** When a sentence matches a pattern, extract the entities and their relationship. From "J.K. Rowling wrote Harry Potter," extract ("J.K. Rowling", "wrote", "Harry Potter").
    

##### **c. Expand Patterns and Examples**

- **Iterative Expansion:** Use the newly extracted examples to discover new patterns or refine existing ones. For example, if the method frequently encounters variations like "J.K. Rowling **authored** Harry Potter," it can add "**authored**" as another pattern synonym for "wrote."
    
- **Generalization:** Broaden the patterns to capture more diverse expressions of the same relationship. This helps in identifying relationships expressed in different linguistic forms.
    

##### **d. Repeat the Process**

- **Snowball Effect:** As more patterns and examples are discovered, the method can uncover increasingly diverse and numerous instances of the target relationship, much like a snowball growing larger as it rolls.

##### **e. Filter and Validate**

- **Remove Noise:** Not all extracted relationships will be correct. Implement filtering mechanisms to eliminate false positives, ensuring the accuracy of the extracted data.
    
- **Refinement:** Continuously refine patterns based on feedback and validation to improve precision and recall.
    

#### **3. Advantages of the Snowball Method**

- **Scalability:** Capable of processing large volumes of text to extract a wide range of relationships without requiring extensive manual annotation.
    
- **Flexibility:** Can be adapted to extract different types of relationships by modifying seed patterns and examples.
    
- **Efficiency:** Automates the discovery of relationships, reducing the need for manual intervention.
    

#### **4. Limitations of the Snowball Method**

- **Dependency on Seed Patterns:** The quality and diversity of seed patterns significantly influence the method's effectiveness. Poorly chosen seeds can lead to limited or biased extraction.
    
- **Pattern Maintenance:** As language evolves or varies across different domains, maintaining and updating patterns can become challenging.
    
- **Noise and Precision:** Rule-based methods can generate false positives, especially in complex or ambiguous linguistic contexts. Ensuring high precision often requires additional filtering steps.
    

#### **5. Practical Example**

Imagine you're using the Snowball method to extract "parent-of" relationships from a collection of biographies:

1. **Seed Patterns:**
    
    - "[Parent] **is the parent of** [Child]"
    - "[Parent] **has a child named** [Child]"
2. **Initial Extraction:**
    
    - "Maria **is the parent of** Sophia."
    - "John **has a child named** Michael."
3. **Pattern Expansion:**
    
    - Discover sentences like "Maria **raised** Sophia," leading to adding "**raised**" as a new pattern.
4. **Further Extraction:**
    
    - "Carlos **brought up** Elena," extracting ("Carlos", "brought up", "Elena").
5. **Final Output:**
    
    - A comprehensive list of parent-child relationships extracted from the text.

#### **6. Comparison with Other Methods**

- **Rule-Based vs. Machine Learning:**
    
    - **Snowball (Rule-Based):** Relies on predefined linguistic patterns and iterative expansion. It's transparent and easier to control but may lack flexibility and require significant manual effort for pattern creation.
    - **Machine Learning-Based Methods:** Utilize statistical models or deep learning to learn patterns from data automatically. They can capture more nuanced relationships but often require large annotated datasets and can be less interpretable.
- **Snowball vs. Distant Supervision:**
    
    - **Snowball:** Begins with seed patterns and expands through pattern matching, focusing on rule-based extraction.
    - **Distant Supervision:** Uses existing databases to automatically label training data, assuming that sentences mentioning entity pairs express their relationship, which can introduce noise but leverages large datasets for training machine learning models.

#### **7. Modern Enhancements**

While the traditional Snowball method is purely rule-based, modern approaches often integrate it with machine learning to improve accuracy and scalability:

- **Hybrid Models:** Combine rule-based pattern matching with statistical models to validate and refine extracted relationships.
    
- **Natural Language Processing Tools:** Utilize advanced NLP techniques like dependency parsing to enhance pattern matching accuracy.
    
- **Feedback Loops:** Implement mechanisms where extracted data is reviewed and used to update and improve patterns continuously.
    

### **Conclusion**

The Snowball method is a foundational technique in Relation Extraction, leveraging iterative pattern matching to discover and extract meaningful relationships between entities in text. Its simplicity and scalability make it a valuable tool, especially when combined with other methods to enhance precision and adaptability. Understanding the Snowball method provides a stepping stone towards more advanced information extraction techniques used in modern NLP applications.



### Giải Thích Đoạn Công Thức Snowball Đơn Giản Cho Học Sinh Cấp 2

Hãy tưởng tượng bạn đang chơi trò tìm kiếm kho báu với những manh mối xung quanh. Đoạn công thức dưới đây giống như hướng dẫn cách bạn tìm kho báu đó một cách thông minh và hiệu quả. Dưới đây là cách giải thích từng bước một cách dễ hiểu:

#### **Đoạn Công Thức:**

```plaintext
1) {< o, ` >,< ls, t1, ms, t2, rs >} = = CreateOccurrence(text segment);
   TC = < o, ` >; SimBest = 0;
   foreach p in Patterns
2)    sim = Match(< ls, t1, ms, t2, rs >, p);
       if ( sim ≥ τsim )
3)          UpdatePatternSelectivity( p, TC );
           if( sim ≥ SimBest )
               SimBest = sim;
               PBest = p;
   if( SimBest ≥ τsim )
       CandidateTuples [TC].Patterns [PBest] = SimBest;
   return CandidateTuples;
```

#### **Giải Thích Bước Qua Bước:**

##### **Bước 1: Tạo Xuất Hiện (CreateOccurrence)**

- **Điều Gì Xảy Ra:**
    
    - Máy tính đọc một đoạn văn bản và tìm thấy hai thực thể (ví dụ: một công ty và một địa điểm).
    - Nó tạo ra một **5-tuple** gồm các phần thông tin xung quanh hai thực thể này: bên trái, giữa và bên phải.
- **Ví Dụ:**
    
    - Giả sử trong câu "Microsoft, Redmond, đã ra mắt sản phẩm mới," "Microsoft" là ORGANIZATION (công ty) và "Redmond" là LOCATION (địa điểm).
    - Máy tính sẽ lưu lại thông tin xung quanh hai từ này để so sánh với các mẫu đã biết.

##### **Bước 2: So Sánh Với Các Mẫu (Match)**

- **Điều Gì Xảy Ra:**
    
    - Máy tính sẽ kiểm tra xem đoạn văn bản vừa tìm thấy có phù hợp với bất kỳ mẫu nào trong danh sách các **Patterns** (mẫu trích xuất) hay không.
    - **sim** là mức độ tương đồng giữa đoạn văn bản và mẫu.
- **Điều Kiện Kiểm Tra:**
    
    - Nếu mức độ tương đồng **sim** lớn hơn hoặc bằng một ngưỡng đã định **τsim**, máy tính sẽ xem xét mẫu đó là phù hợp.

##### **Bước 3: Cập Nhật Độ Chọn Lọc và Chọn Mẫu Tốt Nhất**

- **Cập Nhật Độ Chọn Lọc (UpdatePatternSelectivity):**
    
    - Máy tính cập nhật thông tin về mức độ tin cậy của mẫu **p** dựa trên việc nó vừa trùng khớp với đoạn văn bản này hay không.
- **Chọn Mẫu Tốt Nhất:**
    
    - Nếu **sim** hiện tại lớn hơn hoặc bằng **SimBest** (mức độ tương đồng tốt nhất hiện tại), máy tính sẽ cập nhật **SimBest** và lưu lại mẫu **PBest** là mẫu có độ tương đồng cao nhất.
- **Lưu Kết Quả:**
    
    - Nếu **SimBest** vẫn lớn hơn hoặc bằng **τsim**, máy tính sẽ lưu lại rằng cặp thực thể **TC** (ví dụ: Microsoft và Redmond) được hỗ trợ bởi mẫu **PBest** với mức độ tương đồng **SimBest**.

##### **Trả Về Kết Quả (Return CandidateTuples):**

- **Điều Gì Xảy Ra:**
    - Máy tính trả về danh sách các cặp thực thể cùng với các mẫu đã hỗ trợ chúng. Đây chính là những mối quan hệ mà máy tính đã xác định được từ đoạn văn bản.

#### **Tóm Tắt Bằng Ví Dụ:**

1. **Tìm Xuất Hiện:**
    
    - Máy tính đọc câu "Microsoft, Redmond, đã ra mắt sản phẩm mới" và xác định "Microsoft" là công ty và "Redmond" là địa điểm. Nó cũng ghi nhớ các từ xung quanh hai từ này như "Microsoft, Redmond, đã ra mắt".
2. **So Sánh Với Mẫu:**
    
    - Máy tính so sánh đoạn "Microsoft, Redmond, đã ra mắt" với các mẫu đã biết như "<từ bên trái>, LOCATION, <từ giữa>, ORGANIZATION, <từ bên phải>".
    - Nếu mức độ tương đồng cao (ví dụ: **sim = 0.8** và **τsim = 0.7**), nó sẽ tiếp tục xử lý.
3. **Cập Nhật và Lưu Kết Quả:**
    
    - Máy tính cập nhật độ tin cậy của mẫu và lưu lại rằng cặp "Microsoft - Redmond" phù hợp với mẫu này với mức độ tin cậy là 0.8.
4. **Hoàn Thành:**
    
    - Cuối cùng, máy tính trả về danh sách các cặp thực thể và mẫu đã hỗ trợ chúng, ví dụ: ("Microsoft", "Redmond") được hỗ trợ bởi mẫu với **sim = 0.8**.

#### **Kết Luận:**

Đoạn công thức này giúp máy tính tự động tìm kiếm và xác định các mối quan hệ giữa các thực thể trong văn bản bằng cách so sánh các đoạn văn bản với các mẫu đã biết. Quá trình này giống như việc bạn sử dụng các manh mối để tìm kho báu, nơi máy tính sử dụng các mẫu và mức độ tương đồng để xác định các mối quan hệ một cách chính xác và hiệu quả.