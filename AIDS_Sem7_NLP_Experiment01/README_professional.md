## Meeting Action Item Extractor using NLP

An NLP-based application that automatically extracts action items, assignees, and deadlines from meeting transcripts, along with a short auto-generated meeting summary. The tool converts unstructured meeting notes into a clear, trackable task list.

---

# Problem Statement

In most organizations, meetings generate long, unstructured discussions where important tasks, owners, and deadlines get buried in conversation. Manually reviewing transcripts to identify who needs to do what, and by when, is time-consuming and prone to errors or omissions. This project uses core NLP techniques, including tokenization, part-of-speech tagging, named entity recognition, and rule-based extraction, to automate this process and reduce manual effort.

---

# Features

- Accepts a pasted or uploaded meeting transcript as input
- Identifies sentences that represent action items
- Extracts the person responsible for each task
- Detects and normalizes deadlines, including both absolute dates and relative expressions
- Generates a short summary of the overall meeting discussion
- Allows extracted results to be downloaded as a CSV file

---

# NLP Concepts Used

- Text preprocessing: cleaning and normalizing the raw transcript text
- Sentence tokenization: splitting the transcript into individual sentences
- Part-of-speech tagging: identifying verbs and nouns that indicate an action
- Named entity recognition: extracting person names from the text
- Regex-based date extraction: capturing deadline expressions in different formats
- Rule-based information extraction: linking each task to the correct person and deadline
- Summarization: generating a concise overview of the meeting

---

# Technology Stack

- Programming language: Python
- NLP libraries: spaCy, NLTK
- Data handling: Pandas
- User interface: Streamlit
- Pattern matching: Regex
- Optional extension: Hugging Face Transformers for abstractive summarization

---

# Folder Structure

```
Meeting-Action-Item-Extractor/
    data/
        sample_meeting.txt
    app.py
    extractor.py
    requirements.txt
    README.md
    screenshots/
```

Description of key files:
- app.py: the Streamlit front-end that handles user input and displays results
- extractor.py: the core NLP logic used to identify action items, assignees, and deadlines
- data/sample_meeting.txt: a sample transcript used for testing and demonstration
- requirements.txt: list of Python packages required to run the project

---

# Sample Input

The following is an example meeting transcript that can be used as input:

Manager: Alice, please prepare the sales report by Friday.
Bob, schedule a client meeting next Monday.
Charlie will update the website before 20th August.
Today's discussion focused on increasing customer engagement.

---

# Sample Output

Extracted action items:

| Assigned To | Action Item | Deadline |
|-------------|-------------------------|-------------|
| Alice | Prepare sales report | Friday |
| Bob | Schedule client meeting | Next Monday |
| Charlie | Update website | 20 August |

Generated meeting summary:
- The discussion focused on increasing customer engagement.
- Three action items were assigned during the meeting.

---

# Scope

Included in this version of the project:
- English-language meeting transcripts
- Explicit, action-oriented sentences such as "X will do Y by Z"
- Transcripts formatted with one speaker or statement per line

Not included in this version:
- Audio-to-text transcription of live meetings
- Support for multiple languages
- Detection of implicit or indirect commitments
- Real-time integration with meeting platforms such as Zoom or Teams

---

# Data Requirements

- No pre-existing labeled dataset is required to begin development
- A small set of manually written sample transcripts, covering common phrasing patterns, is sufficient for initial testing
- Publicly available meeting minutes or synthetic transcripts can be used later to test the system on more varied and complex sentence structures

---

# Challenges

- Distinguishing genuine action items from general statements. For example, "Alice presented the report" is a statement, while "Alice will prepare the report" is an action item.
- Handling the variety of ways deadlines are expressed, including absolute dates such as "20th August," relative expressions such as "next Monday," and vague terms such as "as soon as possible."
- Correctly attributing a task to the right person when the transcript does not include clear speaker labels.

---

# Evaluation Approach

- Precision and recall of action-item detection, measured against a manually labeled test set
- Accuracy of person and deadline extraction for each identified task
- Manual review of generated summaries to assess clarity and relevance

---

# Future Improvements

- Support for uploading meeting transcripts in PDF format
- Use of a transformer-based model for more natural, abstractive summaries
- Automatic priority classification of tasks, such as high, medium, or low
- Direct export of extracted tasks to external tools such as Excel or Google Calendar

---

# Conclusion

This project addresses a common and practical workplace problem using an achievable combination of core NLP techniques. It is scoped to be completed within two to three days while still demonstrating a broad range of NLP concepts, including preprocessing, named entity recognition, part-of-speech tagging, and rule-based extraction. This makes it a suitable and easy-to-explain project for a resume, portfolio, or technical interview.

---

# Author

Name: Samiksha Patil
UIN number: 231A044
Department: Artificial Intelligence and Data Science
