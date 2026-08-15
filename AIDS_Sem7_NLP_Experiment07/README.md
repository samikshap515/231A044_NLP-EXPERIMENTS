# Experiment No. 7: Chunking and Named Entity Recognition (NER)

## Aim

To perform chunking to extract meaningful phrases from a text and develop a named entity recognizer to classify entities such as names, places, organizations, and other relevant entities.

## Problem Statement

Develop a Python program using NLP techniques to identify meaningful phrases from a text corpus through chunking and recognize named entities using Named Entity Recognition (NER). The experiment also demonstrates POS tagging as a preprocessing step for chunking.

## Brief Theory

**Chunking**, also known as shallow parsing, is the process of grouping words into meaningful phrases such as noun phrases (NP) and verb phrases (VP). It uses POS tags and grammatical patterns to identify groups of related words without performing complete syntactic parsing.

**Named Entity Recognition (NER)** is an NLP task used to identify and classify named entities in text. Common entity categories include persons, organizations, locations, dates, and monetary values.

Chunking and NER are useful in information extraction, information retrieval, question answering, content recommendation, sentiment analysis, chatbots, and other NLP applications.

## Implementation Explanation

1. Import the required NLTK libraries and download the required NLP resources.
2. Define the sample text:
   ```text
   Microsoft is looking at buying U.K. startup for $1 billion.
   Bill Gates founded Google.
   ```
3. Tokenize the text using NLTK's `word_tokenize()`.
4. Apply POS tagging using NLTK's `pos_tag()` to assign grammatical tags to each token.
5. Perform Named Entity Recognition using NLTK's `ne_chunk()`.
6. Extract entities and their labels from the NER tree.
7. Use spaCy's `en_core_web_sm` model to perform NER and compare the extracted entities.
8. Define a chunk grammar using a regular expression:
   ```python
   NP: {<DT>?<JJ>*<NN>}
   ```
9. Use NLTK's `RegexpParser` to identify noun phrase chunks.
10. Display the chunked sentence and NER results as tree structures.

## Results

The program successfully performed POS tagging, Named Entity Recognition, and chunking on the given text.

### POS Tagging

The program generated POS tags such as:

```text
Microsoft → NNP
is → VBZ
looking → VBG
buying → VBG
U.K. → NNP
startup → NN
Bill → NNP
Gates → NNP
founded → VBD
Google → NNP
```

### NLTK Named Entity Recognition

The NLTK NER output identified entities including:

```text
Microsoft → GPE
Bill Gates → PERSON
Google → PERSON
```

### spaCy Named Entity Recognition

The spaCy model identified:

```text
Microsoft → ORG
U.K. → GPE
$1 billion → MONEY
Bill Gates → PERSON
Google → ORG
```

### Chunking

The defined noun phrase grammar:

```text
NP: {<DT>?<JJ>*<NN>}
```

was applied using `RegexpParser`. The program successfully generated a chunked tree and identified `startup` as an NP chunk.

The notebook also demonstrates a VP grammar and displays the resulting parse tree.

## Conclusion

The experiment successfully demonstrated chunking and Named Entity Recognition using NLTK and spaCy. POS tagging was used as a basis for extracting meaningful phrases through regular-expression-based chunking, while NER identified and classified entities from the text. The experiment shows how these techniques can convert unstructured text into structured linguistic information for NLP applications.

## References

1. NLTK Documentation -- https://www.nltk.org/
2. spaCy Documentation -- https://spacy.io/
3. Python Documentation -- https://docs.python.org/3/
4. Rizvi College of Engineering -- Natural Language Processing Lab Manual.

## Requirements

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

For the spaCy English model, run:

```bash
python -m spacy download en_core_web_sm
```

Required NLTK resources are downloaded in the notebook, including:

```text
punkt
punkt_tab
averaged_perceptron_tagger
averaged_perceptron_tagger_eng
maxent_ne_chunker
maxent_ne_chunker_tab
words
tagsets_json
```

---

## Student

**Name:** Samiksha Patil  
**Course:** B.E. Artificial Intelligence & Data Science Engineering  
**Subject:** Natural Language Processing Lab  
**Experiment No.:** 7
