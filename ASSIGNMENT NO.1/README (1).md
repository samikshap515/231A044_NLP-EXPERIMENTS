# Resume Screening using NLP

## Assignment Overview

This project studies the application of Natural Language Processing (NLP) in **Resume Screening**.

Resume screening systems process resumes and compare candidate information with job descriptions to identify relevant skills, qualifications, and experience.

The assignment evaluates existing resume-screening tools and studies how the application can be adapted for the Marathi language.

## NLP Application

**Application:** Resume Screening / Applicant Tracking System (ATS)

The objective of resume screening is to automatically process resumes, extract relevant information, match candidates with job requirements, and assist recruiters in shortlisting candidates.

## Tools Evaluated

The following tools were explored:

1. **Zoho Recruit**
2. **Jobscan**
3. **HyreTech**

### Zoho Recruit

Zoho Recruit was used to test resume parsing.

Observed result:

- Resume parsing accuracy: **100%**

The tool successfully extracted structured information such as occupation/title, company, summary, and work duration from the uploaded resume.

### Jobscan

Jobscan was tested using a Junior Data Analyst job description.

Observed result:

- Match Rate: **67%**

The tool evaluated ATS compatibility, searchability, hard skills, and other resume-related factors.

### HyreTech

HyreTech was tested using a Backend Developer job description.

Observed result:

- Overall Score: **71/100**
- Verdict: **Consider**
- Technical Qualifications: **78**
- Work Experience: **64**

The tool also identified matching skills and missing qualifications.

## Comparison

| Tool | Main Purpose | Observed Result |
|---|---|---|
| Zoho Recruit | Resume parsing | 100% parsing accuracy |
| Jobscan | ATS and job-description matching | 67% match |
| HyreTech | Candidate scoring and reasoning | 71/100 - Consider |

## Error Analysis

The experiments showed that automated resume-screening systems can process resumes quickly, but their results may be affected by keyword matching, resume structure, missing context, and interpretation of experience.

### False Positives

A false positive occurs when the system considers a candidate suitable because relevant keywords or information are present, even though the candidate may not fully satisfy the job requirement.

In the HyreTech experiment, several backend technologies such as Python, Flask, FastAPI, PostgreSQL, Docker, Celery, and Redis were identified as matching skills. However, the tool also identified that the resume did not clearly demonstrate three or more years of specific backend-service development.

This shows that the presence of relevant technical skills does not necessarily mean that the candidate has sufficient practical experience for the position.

### False Negatives

A false negative can occur when a candidate possesses relevant knowledge or experience, but the system fails to recognize it because it is written differently in the resume.

ATS-oriented systems may depend heavily on keywords. A candidate may describe a skill using a related term or different wording, causing the system to assign a lower match score even when the underlying skill is relevant.

This is especially important for multilingual resumes, where a candidate may describe a skill in Marathi while the job description uses the corresponding English term.

### Keyword Matching Limitations

Jobscan reported a **67% match rate** for the Junior Data Analyst resume. The tool also identified ATS-related issues involving searchability and section headings.

This demonstrates that resume screening can be influenced by how information is written and organized rather than only by the candidate's actual capabilities.

Using the exact job title, standard section headings, and relevant skill names can improve machine readability.

### Context and Experience Limitations

A resume may mention a technology without providing enough information about how extensively it was used.

For example:

> "Python, Docker and PostgreSQL"

does not indicate whether the candidate used these technologies in a major production system, an academic project, or a small personal project.

HyreTech partially addressed this issue by distinguishing between listed skills and evidence of professional backend experience. It identified the lack of clearly documented backend-specific experience as a gap.

### Resume Parsing Limitations

Zoho Recruit reported **100% parsing accuracy** for the tested resume. However, successful extraction does not necessarily mean that the system has understood the complete meaning of the resume.

Resume parsing mainly converts unstructured information into structured fields. A separate matching or semantic-analysis process is required to determine whether the extracted information satisfies a specific job requirement.

### Overall Error Analysis

The experiments demonstrate that automated resume screening should be treated as a decision-support system rather than a complete replacement for human recruiters.

Different tools identify different aspects of a candidate:

- Zoho Recruit focuses on structured resume parsing.
- Jobscan emphasizes ATS compatibility and job-description matching.
- HyreTech provides candidate scoring and explanations of matching and missing qualifications.

Combining structured parsing, semantic skill matching, experience analysis, and human review can produce a more reliable recruitment process.

## Marathi Language Adaptation

### Indian Language Selected

The selected Indian language is **Marathi**.

The objective is to adapt an automated resume-screening system so that it can understand Marathi resumes and Marathi-English mixed resumes and match them with relevant job descriptions.

### Required Linguistic Resources

#### 1. Marathi Resume Corpus

A Marathi resume corpus would be required for training and testing. It should contain education, skills, work experience, job titles, projects, and certifications.

Example:

"मला Python, SQL आणि Data Analysis मध्ये अनुभव आहे."

The system should identify Python, SQL, and Data Analysis as relevant skills.

#### 2. Marathi Job Description Corpus

A collection of Marathi job descriptions would help the system learn how requirements are expressed in Marathi.

Example:

"उमेदवाराला Python आणि SQL चे ज्ञान असणे आवश्यक आहे."

The system should associate this requirement with the corresponding skills in a candidate's resume.

#### 3. Marathi POS Tagger

A Part-of-Speech (POS) tagger can help identify the grammatical role of words in Marathi sentences and help distinguish important information from general text.

#### 4. Named Entity Recognition (NER)

A Marathi NER system can identify:

- Candidate names
- Organizations
- Colleges and universities
- Locations
- Job titles
- Educational qualifications
- Skills

This helps convert an unstructured Marathi resume into structured candidate information.

#### 5. Marathi Language Model

A Marathi language model can help understand the context and meaning of resume statements instead of relying only on exact keyword matching.

For example:

"डेटा विश्लेषणाचा अनुभव आहे."

should be recognized as related to:

"Experience in Data Analysis."

#### 6. Marathi-English Lexicon and Parallel Data

A Marathi-English vocabulary and parallel dataset can map Marathi expressions to their English equivalents. This is important because many technical resumes use English terminology within Marathi text.

### Socio-Linguistic Challenges

#### 1. Code-Switching

Candidates may use Marathi and English in the same sentence.

Example:

"मी Python आणि SQL वापरून data analysis projects केले आहेत."

The system should still identify Python, SQL, and Data Analysis as relevant skills.

#### 2. Dialect Variations

Marathi is used across different regions and may contain variations in vocabulary and expressions.

The system should avoid treating regional differences in wording as missing skills or qualifications and should be evaluated using text from different Marathi-speaking regions.

#### 3. Script Variations

Marathi is normally written using Devanagari, but it may also be typed using Roman/Latin script.

Devanagari:
"मला Python मध्ये अनुभव आहे."

Roman Marathi:
"Mala Python madhye anubhav aahe."

The adapted system should ideally recognize that both sentences express the same meaning.

#### 4. English Technical Terms

Technical resumes frequently contain English terminology even when the surrounding text is Marathi.

Example:

"मला Machine Learning, Python आणि Data Visualization मध्ये experience आहे."

The system should identify Machine Learning, Python, and Data Visualization as technical skills.

## Proposed Marathi Resume-Screening Pipeline

```text
Marathi / Marathi-English Resume
          ↓
Text Extraction
          ↓
Language and Script Identification
          ↓
Marathi Tokenization
          ↓
Code-Switch Detection
          ↓
NER and POS Tagging
          ↓
Skill and Qualification Extraction
          ↓
Semantic Matching with Job Description
          ↓
Candidate Match Score
          ↓
Candidate Ranking
```

## Concrete Steps for Adaptation

1. Collect Marathi resumes and Marathi job descriptions.
2. Annotate skills, education, organizations, job titles, projects, and experience.
3. Add Marathi language-processing resources such as POS tagging, NER, and language models.
4. Build a Marathi-English skill vocabulary.
5. Add code-switching detection for Marathi-English resumes.
6. Support both Devanagari and Roman Marathi text.
7. Train the matching system using Marathi and Marathi-English examples.
8. Test the system using resumes from different regions and writing styles.
9. Compare Marathi system results with the original English resume-screening system.
10. Use human recruiter evaluation to identify incorrect matches and improve the model.

## Expected Benefits

A Marathi-enabled resume-screening system would make automated recruitment more accessible to candidates who prefer writing resumes in Marathi. It could reduce dependence on exact English keywords and improve recognition of skills and qualifications expressed using Marathi or Marathi-English mixed language.

However, human review would still be important because automated systems may misunderstand regional language variations, mixed-language expressions, or context-specific descriptions.

## Conclusion

The experiments demonstrate that NLP can support different stages of recruitment, including resume parsing, ATS matching, skill extraction, and candidate evaluation.

Zoho Recruit demonstrated effective resume parsing, Jobscan provided ATS-oriented matching, and HyreTech provided detailed candidate scoring and gap analysis.

For Marathi resume screening, the system would need to address multilingual text, code-switching, dialect variation, script variation, and Marathi-English technical terminology. Combining linguistic resources, semantic matching, and human review would make the system more reliable and inclusive.

## Repository Structure

```text
Resume-Screening-NLP/
│
├── screenshots/
│   ├── zoho-parsing.png
│   ├── jobscan-result.png
│   ├── jobscan-job-description.png
│   ├── hyretech-score.png
│   └── hyretech-analysis.png
│
├── report/
│   └── resume-screening-report.pdf
│
└── README.md
```
