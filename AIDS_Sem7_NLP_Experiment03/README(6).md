# Experiment No. 3: Stop Word Removal, Lemmatization, and Stemming

## Aim

To apply stop word removal followed by lemmatization and stemming on
preprocessed text and observe their effects on text representation.

## Problem Statement

Develop a Python program that removes stop words from a text corpus,
applies stemming and lemmatization, and compares the transformed text to
understand the impact of each preprocessing technique on NLP tasks.

## Brief Theory

Text preprocessing improves the quality of textual data before applying
NLP algorithms. Stop word removal eliminates frequently occurring words
with little semantic value. Stemming reduces words to their root form by
removing prefixes or suffixes, while lemmatization converts words to
their dictionary (base) form using vocabulary and grammatical analysis.
These techniques reduce noise and improve the efficiency of NLP models.

## Implementation Explanation

1.  Import the required NLP libraries.
2.  Load and preprocess the input text.
3.  Tokenize the text into words.
4.  Remove stop words using the predefined stop word list.
5.  Apply Porter Stemmer to obtain stemmed words.
6.  Apply WordNet Lemmatizer to obtain meaningful base forms.
7.  Compare the original, stop-word removed, stemmed, and lemmatized
    outputs.

## Results

The program successfully removed stop words, generated stemmed tokens,
and produced lemmatized words. The comparison demonstrated that
lemmatization preserves meaningful words better than stemming while
reducing vocabulary size.

## Conclusion

The experiment demonstrated the importance of stop word removal,
stemming, and lemmatization in NLP preprocessing. These techniques
improve text representation, reduce redundancy, and enhance the
performance of machine learning and information retrieval systems.

## References

1.  NLTK Documentation -- https://www.nltk.org/
2.  Python Documentation -- https://docs.python.org/3/
3.  Rizvi College of Engineering -- Natural Language Processing Lab
    Manual.

## Requirements

Install the required libraries:

``` bash
pip install -r requirements.txt
nltk
pandas
matplotlib
```

---

## Student

**Name:** Samiksha Patil  
**Course:** B.E. Artificial Intelligence & Data Science Engineering  
**Subject:** Natural Language Processing Lab  
**Experiment No.:** 3


