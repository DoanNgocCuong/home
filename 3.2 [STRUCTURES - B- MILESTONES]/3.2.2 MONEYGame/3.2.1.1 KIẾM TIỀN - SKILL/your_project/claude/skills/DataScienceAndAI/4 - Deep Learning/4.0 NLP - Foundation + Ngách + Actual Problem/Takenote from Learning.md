
## 1. example using spaCy 
for 1 sample sentence and for 1 sample paragraph using sends property

| Method   | Purpose                                                                                | Example Output                             |
| -------- | -------------------------------------------------------------------------------------- | ------------------------------------------ |
| `t.text` | Provides the text of each token                                                        | `"SpaCy", "is", "an", "open-source", ...`  |
| `t.i`    | Provides the index of each token in the doc                                            | `0, 1, 2, 3, ...`                          |
| `sents`  | we retrieve each complete sentence from the paragraph, separated based on punctuation. | `"SpaCy is designed specifically...", ...` |


## 2. Bag of words: 

- Bag of Words is just the first step. Although it doesn’t understand word meanings, it’s helpful when combined with other techniques to let computers "understand" text better.

- Example: Imagine we have a sentence:
	
> 	"Con mèo thích ăn cá và con mèo thích ngủ."
	
	With the Bag of Words method, we would:
	
	1. **List the words**: First, we list all the words without repeating any:
	   - Words: "Con," "mèo," "thích," "ăn," "cá," "và," "ngủ."
	
	2. **Count the occurrences of each word**:
	   - "Con" appears 2 times.
	   - "Mèo" appears 2 times.
	   - "Thích" appears 2 times.
	   - "Ăn" appears 1 time.
	   - "Cá" appears 1 time.
	   - "Và" appears 1 time.
	   - "Ngủ" appears 1 time.
	
	3. **Result**: We turn the sentence into a table of counts:
	
	| Con | Mèo | Thích | Ăn | Cá | Và | Ngủ |
	|-----|-----|-------|----|----|----|-----|
	| 2   | 2   | 2     | 1  | 1  | 1  | 1   |

| **Application**           | **Description**                                               | **Example**                                                                                   |
| ------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Text Classification**   | Helps computers classify text based on content.               | If words like "mèo" and "chó" appear a lot, the system might guess the text is about animals. |
| **Sentiment Analysis**    | Identifies the sentiment in text by analyzing word frequency. | Words like "vui" or "tuyệt vời" suggest positivity, while "buồn" hints at negativity.         |
| **Information Retrieval** | Improves search results by recognizing important words.       | In search engines, frequent keywords help identify relevant webpages.                         |
| **Topic Analysis**        | Detects main topics in large collections of texts.            | Words like "y tế" or "bệnh viện" in a document might indicate the topic is healthcare.        |


## 3. Training Model: 
Here’s an overview of how you can use some of these frameworks—spaCy, NLTK, and Hugging Face's Transformers—to train models on a corpus.

 Comparison of Frameworks

| Framework    | Best for                          | Pros                                        | Cons                                |
|--------------|-----------------------------------|---------------------------------------------|-------------------------------------|
| **spaCy**    | NLP tasks (NER, POS, classification) | Fast, efficient, easy for production       | Limited pre-trained deep models    |
| **NLTK**     | Basic NLP and education           | Great for beginners, simple preprocessing   | Not optimized for deep learning    |
| **Transformers** | Fine-tuning large models        | Supports many state-of-the-art models       | Requires GPU for efficient training |

Each framework serves different needs, so the choice depends on the complexity of the task and available computational resources. Let me know if you’d like help with any specific part!