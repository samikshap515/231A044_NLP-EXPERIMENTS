# NLP Experiment No. 5 – N-Gram Language Model

## Aim

To implement an **N-Gram Language Model** using Python and NLTK for text processing, generate bigrams and trigrams, calculate their frequencies, predict the next word, generate a sequence of words, and evaluate the language model using perplexity.

## Problem Statement

Natural Language Processing applications often need to understand the relationship between words in a sentence and predict the next possible word based on previously observed words.

The objective of this experiment is to develop a simple statistical language model using **N-Grams**. The experiment uses a sample text corpus and the **Reuters corpus provided by NLTK** to:

- Preprocess textual data.
- Generate bigrams and trigrams.
- Calculate N-Gram frequencies.
- Predict the next word based on previously observed words.
- Generate a sequence of words.
- Build a trigram-based language model.
- Calculate the perplexity of the model.

## Brief Theory

### 1. Natural Language Processing

Natural Language Processing (NLP) is a branch of Artificial Intelligence that enables computers to process, analyze, and understand human language.

### 2. Tokenization

Tokenization is the process of dividing text into smaller units called tokens, usually words or sentences. In this experiment, NLTK's `word_tokenize()` function is used.

### 3. Text Preprocessing

The sample corpus is preprocessed by:
1. Converting text to lowercase.
2. Tokenizing the text.
3. Removing punctuation.
4. Removing English stopwords.

For the given sample corpus, the resulting tokens are:

```text
['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog', 'fox', 'quick', 'dog', 'lazy']
```

### 4. N-Gram

An N-Gram is a sequence of N consecutive words from a text.

**Bigram:** contains two consecutive words.

Example:
```text
('quick', 'brown')
('brown', 'fox')
('fox', 'jumps')
```

**Trigram:** contains three consecutive words.

Example:
```text
('quick', 'brown', 'fox')
('brown', 'fox', 'jumps')
('fox', 'jumps', 'lazy')
```

N-Grams are useful for estimating the probability of a word based on the words that occur before it.

### 5. Frequency Distribution

`FreqDist` from NLTK is used to count how frequently N-Grams occur in the corpus.

### 6. Conditional Frequency Distribution

`ConditionalFreqDist` is used to determine which words occur after a particular word. For example, in the sample corpus:

```text
fox → jumps, quick
dog → fox, lazy
```

### 7. Next-Word Prediction

The experiment predicts the most likely word following a given word using the conditional frequency distribution.

For example:

```text
Input: fox
Output: jumps
```

### 8. Trigram Language Model

A trigram language model predicts the next word using the previous two words.

The model represents:

```text
(w1, w2) → w3
```

The probability can be estimated as:

\[
P(w_3|w_1,w_2) =
\frac{Count(w_1,w_2,w_3)}
{Count(w_1,w_2)}
\]

### 9. Perplexity

Perplexity is a measure used to evaluate language models. A lower perplexity generally indicates that the model is better at predicting a test sequence.

## Implementation Explanation

### Step 1: Import Required Libraries

The experiment uses NLTK and Python libraries including:

- `nltk`
- `word_tokenize`
- `bigrams`
- `trigrams`
- `FreqDist`
- `ConditionalFreqDist`
- `reuters`
- `defaultdict`

### Step 2: Preprocess the Sample Corpus

The following sample corpus is used:

```text
The quick brown fox jumps over the lazy dog.
The fox is quick and the dog is lazy.
```

After preprocessing:

```text
['quick', 'brown', 'fox', 'jumps', 'lazy',
 'dog', 'fox', 'quick', 'dog', 'lazy']
```

### Step 3: Generate Bigrams

The experiment generates bigrams such as:

```text
('quick', 'brown')
('brown', 'fox')
('fox', 'jumps')
('jumps', 'lazy')
('lazy', 'dog')
('dog', 'fox')
('fox', 'quick')
('quick', 'dog')
('dog', 'lazy')
```

### Step 4: Calculate Bigram Frequency

`FreqDist` is used to calculate bigram frequencies. Each of the nine generated bigrams occurs once in the sample corpus.

### Step 5: Create Conditional Frequency Distribution

A `ConditionalFreqDist` is created from the bigrams to associate each word with words that follow it.

Examples:

```text
quick → brown, dog
fox → jumps, quick
dog → fox, lazy
```

### Step 6: Generate Trigrams

The experiment generates trigrams from the processed tokens.

Examples:

```text
('quick', 'brown', 'fox')
('brown', 'fox', 'jumps')
('fox', 'jumps', 'lazy')
('jumps', 'lazy', 'dog')
```

### Step 7: Predict the Next Word

A `predict_next_word()` function is used to predict the most likely word after a given word.

For the input:

```text
fox
```

the notebook produces:

```text
Next word after 'fox': 'jumps'
```

### Step 8: Generate a Word Sequence

The experiment repeatedly predicts the next word to generate a sequence.

Starting with `jumps`, the notebook produces:

```text
jumps lazy dog fox jumps lazy dog fox jumps
```

### Step 9: Use the Reuters Corpus

The experiment then uses the Reuters corpus available through NLTK.

The notebook reports:
- Number of Reuters file IDs: **10,788**
- Words obtained from the Reuters file IDs: **1,720,901**

### Step 10: Build the Trigram Model

Trigrams are generated from the tokenized Reuters corpus. A nested `defaultdict` is used to store trigram counts and the counts are normalized into probabilities.

### Step 11: Predict Using the Trigram Model

The trigram model is used for next-word prediction. For the input pair:

```text
NET Shr
```

the notebook produces:

```text
Next Word: profit
```

### Step 12: Calculate Perplexity

The notebook evaluates the model using the test text:

```text
asian exporters fear damage
```

The calculated perplexity is approximately:

```text
4.923882631706739
```

## Results

The experiment successfully implemented an N-Gram based language model using NLTK.

### Sample Corpus Results

| Operation | Result |
|---|---|
| Preprocessed tokens | 10 tokens |
| Bigrams generated | 9 |
| Trigrams generated | 8 |
| Next word after `fox` | `jumps` |
| Generated sequence | `jumps lazy dog fox jumps lazy dog fox jumps` |

### Reuters Corpus Results

| Parameter | Result |
|---|---:|
| Number of Reuters file IDs | 10,788 |
| Words obtained from Reuters file IDs | 1,720,901 |
| Tokenized words used for trigram generation | 1,728,932 |
| Prediction for `NET Shr` | `profit` |
| Calculated perplexity | 4.923882631706739 |

## Conclusion

The experiment successfully demonstrated the implementation of an **N-Gram Language Model using Python and NLTK**. Text preprocessing, bigram and trigram generation, frequency analysis, conditional frequency distribution, and next-word prediction were implemented successfully.

The Reuters corpus was further used to build a trigram-based language model and predict the next word. The model predicted **`profit`** for the word pair **`NET Shr`** and produced a perplexity value of approximately **4.92** for the given test sequence.

This experiment provides a basic understanding of how statistical language models learn word relationships and can be used for applications such as **text prediction, autocomplete, and text generation**.

## References

1. NLTK Documentation – Natural Language Toolkit  
   https://www.nltk.org/

2. Bird, S., Klein, E., & Loper, E. – *Natural Language Processing with Python*, O'Reilly Media.

3. NLTK Reuters Corpus – Reuters Corpus Reader documentation  
   https://www.nltk.org/api/nltk.corpus.reader.reuters.html

4. Python Documentation  
   https://docs.python.org/3/

## Requirements

The experiment requires **Python 3** and the following package:

```text
nltk
```

### requirements.txt

Create a file named `requirements.txt` containing:

```text
nltk
```

Install it using:

```bash
pip install -r requirements.txt
```

The notebook downloads the required NLTK resources during execution:

```python
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('reuters')
```

## Project Structure

```text
NLP-Experiment-5/
│
├── NLP_EXP_NO_5.ipynb
├── README.md
└── requirements.txt
```

## Technologies Used

- Python 3
- NLTK
- N-Gram Language Modeling
- Bigram and Trigram Analysis
- Reuters Corpus
- Statistical Text Prediction
- Perplexity Evaluation
