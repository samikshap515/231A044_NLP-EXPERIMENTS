# Experiment No. 4: Morphological Analysis and Word Generation

## Aim

To perform morphological analysis for given words in a corpus and generate different word forms to understand word morphology in detail.

## Problem Statement

Develop a Python program that performs morphological analysis on input text by tokenizing the text, identifying base or root forms using lemmatization, and analyzing morphological changes such as inflectional and derivational forms.

## Brief Theory

Morphology is the study of the structure and formation of words in a language. A **morpheme** is the smallest grammatical unit that carries meaning. Morphemes can be free morphemes, which can stand alone as words, or bound morphemes, such as prefixes and suffixes.

Inflectional morphology modifies a word to express grammatical information without changing its basic meaning or part of speech, such as `run → running` or `cat → cats`. Derivational morphology creates new words by adding prefixes or suffixes, such as `happy → unhappy` or `happy → happiness`.

Morphological analysis helps NLP systems identify relationships between different word forms and improves language understanding and text processing.

## Implementation Explanation

1. Import the required NLP libraries such as NLTK, `word_tokenize`, `WordNetLemmatizer`, and `string`.
2. Define the input text: `"I was computing."`
3. Convert the input text to lowercase.
4. Tokenize the text into individual words using NLTK.
5. Remove punctuation from the generated tokens.
6. Apply WordNet Lemmatizer to identify the base or root forms of the words.
7. Compare each token with its corresponding lemma.
8. Identify morphological changes and classify them as base/root, inflectional, or irregular forms.
9. Perform additional lemmatization on example words such as `playing`, `played`, `studies`, `running`, `better`, and `cars`.

## Results

The program successfully performed morphological analysis on the input sentence.

**Input:**
```text
I was computing.
```

**Tokens:**
```text
['i', 'was', 'computing', '.']
```

**After punctuation removal:**
```text
['i', 'was', 'computing']
```

**Lemmatized output:**
```text
['i', 'be', 'compute']
```

The morphological analysis identified:
- `i` → Base/root form
- `was` → Inflectional or irregular form of `be`
- `computing` → Inflectional present participle/continuous form of `compute`

## Conclusion

The experiment successfully demonstrated morphological analysis and word-form processing using Python and NLTK. Tokenization, punctuation removal, and lemmatization were used to identify meaningful base forms and analyze morphological changes. The experiment helped in understanding how morphology contributes to better text representation and language understanding in NLP.

## References

1. NLTK Documentation -- https://www.nltk.org/
2. Python Documentation -- https://docs.python.org/3/
3. Rizvi College of Engineering -- Natural Language Processing Lab Manual.

## Requirements

Install the required library:

```bash
pip install -r requirements.txt
nltk
```

The following NLTK resources are required and are downloaded in the notebook:

```text
punkt
punkt_tab
wordnet
omw-1.4
```

---

## Student

**Name:** Samiksha Patil  
**Course:** B.E. Artificial Intelligence & Data Science Engineering  
**Subject:** Natural Language Processing Lab  
**Experiment No.:** 4
