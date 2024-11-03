
1. example using spaCy for 1 sample sentence and for 1 sample paragraph using sends property


| Method   | Purpose                                                                                | Example Output                             |
| -------- | -------------------------------------------------------------------------------------- | ------------------------------------------ |
| `t.text` | Provides the text of each token                                                        | `"SpaCy", "is", "an", "open-source", ...`  |
| `t.i`    | Provides the index of each token in the doc                                            | `0, 1, 2, 3, ...`                          |
| `sents`  | we retrieve each complete sentence from the paragraph, separated based on punctuation. | `"SpaCy is designed specifically...", ...` |
