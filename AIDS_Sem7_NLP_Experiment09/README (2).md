# NLP Experiment No. 9 — Word Sense Disambiguation using Lesk Algorithm

## Aim

To implement **Word Sense Disambiguation (WSD)** using the **Lesk algorithm** and the NLTK WordNet lexical database. The experiment identifies the most appropriate meaning (sense) of an ambiguous word based on the context in which it appears.

## Problem Statement

Words in natural language can have multiple meanings depending on their surrounding context. For example, the word **"bank"** can refer to a financial institution or another meaning such as a bank/stock of something. The objective of this experiment is to determine the appropriate WordNet sense of an ambiguous word by comparing the words in its context with the definitions and example sentences associated with each possible sense.

## Brief Theory

### Word Sense Disambiguation

Word Sense Disambiguation is an NLP task that determines which meaning of a word is intended in a particular sentence.

For example:

- *"I went to the bank to deposit some money."* → financial institution
- *"He has a bank of knowledge."* → a collection/store

### Lesk Algorithm

The Lesk algorithm is a knowledge-based WSD technique. It selects the sense whose **dictionary definition (gloss) and example sentences have the greatest overlap with the words in the given context**.

The basic process is:

1. Tokenize the input sentence.
2. Obtain all WordNet synsets (senses) for the ambiguous word.
3. Extract the definition and examples for every candidate sense.
4. Tokenize these definitions and examples.
5. Compare them with the tokens in the input sentence.
6. Calculate the overlap for every candidate sense.
7. Select the sense with the highest overlap.

In the notebook, the overlap is calculated as:

`overlap = definition overlap + example overlap`

## Implementation Explanation

The implementation is written in Python using **NLTK** and **WordNet**.

### 1. Importing libraries and resources

The notebook imports NLTK and WordNet and downloads the required NLTK resources:

- `wordnet`
- `punkt`
- `punkt_tab`

### 2. Defining the Lesk function

A custom `lesk(word, sentence)` function is implemented. It:

- Tokenizes the input sentence using `nltk.word_tokenize()`.
- Retrieves all synsets of the ambiguous word using `wn.synsets(word)`.
- Gets each synset's definition using `sense.definition()`.
- Gets example sentences using `sense.examples()`.
- Calculates word overlap between the sentence and each sense's definition/examples.
- Stores the sense with the maximum overlap.
- Returns the selected WordNet synset.

### 3. Testing with the word "book"

The notebook uses:

`sentence = "i book a ticket for my movie"`

with:

`ambiguous_word = "book"`

The recorded output was:

`book.n.11 - a number of sheets (ticket or stamps etc.) bound together on one edge`

This demonstrates that the custom implementation selects a WordNet sense based on contextual word overlap. The selected sense is dependent on the available WordNet glosses/examples and the simple overlap-based scoring used in the experiment.

### 4. Testing overlap

The notebook also calculates token overlap for example sentences involving the word "bank". The demonstrated overlap calculation returned:

`5`

### 5. Accuracy experiment

A small manually annotated dataset containing two examples for the word "bank" was tested:

- `"I went to the bank to deposit some money."` → `bank.n.01`
- `"He has a bank of knowledge."` → `bank.n.02`

The recorded result was:

`Accuracy: 0.00`

Therefore, for this specific two-example dataset and the exact implementation/WordNet sense labels used in the notebook, the measured accuracy was **0%**.

This result should be interpreted as an observation of the experiment rather than a general measure of the Lesk algorithm. The implementation uses a very small dataset and simple lexical overlap, and WordNet sense selection can differ from manually assigned labels.

### 6. Additional notebook observation

One notebook cell attempts to call `wordnet.synset("bank")` without defining/importing `wordnet` under that name, which produced:

`NameError: name 'wordnet' is not defined`

This cell is separate from the main custom Lesk implementation.

## Results

The experiment successfully demonstrates the basic working of a knowledge-based Word Sense Disambiguation approach using NLTK WordNet.

Observed results:

| Test | Result |
|---|---|
| Token overlap example | `5` |
| Ambiguous word | `book` |
| Test sentence | `i book a ticket for my movie` |
| Selected sense | `book.n.11` |
| Selected definition | `a number of sheets (ticket or stamps etc.) bound together on one edge` |
| Small bank dataset accuracy | `0.00` / `0%` |
| NLTK resources | WordNet, Punkt, Punkt Tab |

The notebook therefore demonstrates the complete flow from sentence tokenization to candidate sense generation, overlap calculation, and final sense selection.

## Conclusion

The experiment demonstrates how the **Lesk algorithm** can be used for Word Sense Disambiguation with the help of **NLTK WordNet**. The implementation compares the context of an ambiguous word with the definitions and examples of its possible WordNet senses and selects the sense having the highest lexical overlap.

The experiment also shows an important limitation of the basic Lesk approach: performance depends strongly on the quality of the context, WordNet glosses/examples, sense labels, and the size and quality of the evaluation dataset. In the notebook's small evaluation dataset, the recorded accuracy was 0%, showing that simple lexical overlap does not always match manually assigned senses.

## References

1. Lesk, M. (1986). *Automatic Sense Disambiguation Using Machine Readable Dictionaries*. Proceedings of the 5th Annual International Conference on Systems Documentation.
2. NLTK Documentation — Natural Language Toolkit: https://www.nltk.org/
3. Princeton WordNet — lexical database for English: https://wordnet.princeton.edu/
4. NLTK WordNet Interface Documentation: https://www.nltk.org/howto/wordnet.html

## Requirements

The experiment requires Python 3 and the NLTK library.

Install the dependency using:

```bash
pip install -r requirements.txt
```

After installation, the notebook downloads the required NLTK data automatically using:

```python
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('punkt_tab')
```

## Files

```text
NLP_EXP_NO_9.ipynb
README.md
requirements.txt
```
