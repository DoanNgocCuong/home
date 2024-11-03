
1. example using spaCy for sample sentence and for 1 sample paragraph using sends property
Here's an example of how to use spaCy to process a sample sentence and a sample paragraph, focusing on the `sents` property to extract sentences.

### Sample Sentence

```python
import spacy

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Sample sentence
sentence = "SpaCy is an open-source library for advanced NLP tasks."
doc = nlp(sentence)

# Extract sentences using the sents property
print([(t.text, t.i) for t in doc])
```

### Sample Paragraph

```python
# Sample paragraph
paragraph = (
    "SpaCy is designed specifically for production use. "
    "It is fast, efficient, and easy to use. "
    "The library supports multiple languages and provides pre-trained models."
)

# Process the paragraph
doc_paragraph = nlp(paragraph)

# Extract sentences using the sents property
for sent in doc_paragraph.sents:
    print(sent.text)
```
