# Exploratory Data Analysis (EDA) on a Text Corpus

## Aim
To perform exploratory data analysis on a text corpus and visualize important insights using word clouds, word-frequency plots, review-length distribution plots, and bigram analysis.

## Problem Statement
Text reviews contain useful information, but raw text is unstructured and difficult to analyze directly. The aim of this experiment is to explore a large collection of movie reviews, examine text characteristics, identify frequent words and word combinations, and visualize patterns that can help in later Natural Language Processing (NLP) tasks.

## Brief Theory
Exploratory Data Analysis (EDA) is the process of understanding a dataset through descriptive statistics and visualizations. For text data, EDA can reveal common terms, text lengths, repeated patterns, and possible data-quality issues.

The experiment uses text preprocessing and visualization techniques:
- **Tokenization and word counting:** split reviews into words and calculate text statistics.
- **Text cleaning:** convert text to lowercase, remove HTML tags and non-alphabetic characters, and normalize whitespace.
- **Stop-word removal:** filter common English words so that more meaningful terms stand out in frequency analysis.
- **Word-frequency plot:** display the most frequent words.
- **Word cloud:** show frequent terms, with larger words representing higher frequencies.
- **Distribution plot:** show how review word counts are distributed.
- **Bigram analysis:** identify common two-word combinations.

## Implementation Explanation
The experiment is implemented in the Jupyter Notebook `NLP_EXP_NO_10.ipynb`.

1. **Load the dataset:** The IMDB movie-review dataset is loaded using the Hugging Face `datasets` library (`stanfordnlp/imdb`).
2. **Combine the data:** The training and testing splits are converted to Pandas DataFrames and combined. The resulting dataset contains 50,000 reviews with `text` and `label` columns.
3. **Check data quality:** Count missing values and duplicate rows.
4. **Calculate text statistics:** Calculate character count, word count, unique word count, and average word length for each review.
5. **Clean the reviews:** Convert text to lowercase, remove HTML tags, remove characters other than English letters and whitespace, and replace repeated whitespace with a single space.
6. **Plot review-length distribution:** Use a histogram to examine the number of words per review.
7. **Plot frequent words:** Count words with Python's `Counter` and display the 20 most frequent words in a horizontal bar chart.
8. **Remove stop words for frequency analysis:** Use scikit-learn's English stop-word list and plot the 20 most frequent remaining words.
9. **Generate a word cloud:** Combine the cleaned reviews and visualize frequent terms using the `WordCloud` library.
10. **Analyze bigrams:** Use `CountVectorizer` with `ngram_range=(2, 2)` and English stop-word removal to count common two-word combinations.

## Results
The notebook's recorded outputs show:
- **Dataset size:** 50,000 reviews and 2 columns (`text`, `label`).
- **Missing values:** 0 missing values in both columns.
- **Duplicate rows:** 418.
- **Average review length:** approximately 231 words.
- **Average character count:** approximately 1,309 characters.
- **Average unique word count:** approximately 148 words per review.
- **Average word length:** approximately 4.64 characters.
- **Total words after cleaning:** 11,259,489.
- **Vocabulary size after cleaning:** 214,620 unique words.
- Visualizations produced include a review-length histogram, top-word frequency charts, a word cloud, and a table of the top 20 bigrams. The notebook output includes frequent bigrams such as `ive seen`, `dont know`, and `special effects`.

The exact top-word rankings and chart appearance depend on the dataset and preprocessing used. The word cloud is generated from cleaned text before stop-word removal, while the stop-word-filtered frequency plot removes common English words.

## Conclusion
Exploratory Data Analysis helps summarize and understand a text corpus using statistics and visualizations. In this experiment, movie reviews were cleaned and analyzed using text statistics, word-frequency plots, a word cloud, review-length distribution, and bigram analysis. These methods reveal frequent terms and recurring phrases, and help identify patterns that can guide later NLP tasks such as sentiment analysis and classification.

## References
1. Rizvi College of Engineering, **CSDOL7011: Natural Language Processing — Experiment No. 10: Exploratory Data Analysis (EDA)**, supplied lab manual.
2. Hugging Face Datasets, **IMDB dataset (`stanfordnlp/imdb`)**: https://huggingface.co/datasets/stanfordnlp/imdb
3. Pandas documentation: https://pandas.pydata.org/docs/
4. Matplotlib documentation: https://matplotlib.org/stable/
5. scikit-learn `CountVectorizer` documentation: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
6. WordCloud documentation: https://amueller.github.io/word_cloud/

## Requirements
Install the Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Then open and run `NLP_EXP_NO_10.ipynb` in Jupyter Notebook or Google Colab. The dataset is downloaded from Hugging Face, so an internet connection is needed for the initial download.
