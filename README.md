# Hebrew Social Text Analysis

This project focuses on analyzing Hebrew text collected from social media platforms to identify commonly used vocabulary and expressions.

It was created primarily for **personal and educational purposes**, as a way to better understand real, informal Hebrew usage online. By analyzing frequently used words and expressions, the project supports Hebrew language learning and familiarity with everyday vocabulary found on social networks.

In addition to the linguistic aspect, this project serves as **hands-on practice with data analysis using Python**, including handling non-English, real-world text data.

## Dataset

The dataset consists of **manually selected YouTube comments** collected on January 17th. Comments were chosen from different videos/topics to reflect a broad range of everyday Hebrew usage.

The data was manually collected to avoid reliance on external APIs and to ensure direct interaction with raw text.

## What This Project Does

- Loads raw Hebrew text data
- Performs basic preprocessing (cleaning, counting words)
- Identifies the most frequent words
- Builds contingency tables and applies Chi-Square tests to detect potential associations between words and topics
- Outputs basic statistics highlighting commonly used vocabulary

## Limitations

- **Small dataset**: results are illustrative and may not generalize
- **No advanced preprocessing**: stopwords, lemmatization, or token normalization are not applied
- **Chi-Square analysis** is limited to the top 10 most common words
- **No interactive visualization** yet (heatmaps or graphs will be added in the future)

## Future Improvements

- Expand dataset for more robust analysis
- Implement stopwords removal and lemmatization for Hebrew
- Add visualizations such as heatmaps for word-topic associations
- Explore phrase/expression analysis, not just single words
- Potential integration into Jupyter Notebook for interactive exploration

## Tech Stack

- Python 3.13
- Pandas
- Collections (`Counter`)
- SciPy (`chi2_contingency`)
- Python-Bidi (for correct display of Hebrew in terminals)

## How to Run

1. Clone the repository:

```bash
git clone <your-repo-url>
cd hebrew-social-text-analysis
