# Hebrew Social Text Analysis

Analyze Hebrew text from YouTube comments to identify commonly used words and basic word–topic associations.

This project was created for personal and educational purposes, combining Hebrew language learning with hands-on Python data analysis on real, informal social media text.

---

## What this project does

- Collects Hebrew YouTube comments from selected videos
- Cleans and preprocesses raw text
- Counts word frequencies (excluding stopwords)
- Analyzes topic distribution
- Applies Chi-Square tests to the 10 most frequent words
- Generates a plain-text summary report

---

## Scripts

- scripts/youtube_fetch.py  
  Collects comments using the YouTube API.  
  Filters comments to keep only those containing Hebrew letters.  
  Output: data/raw/comments.json

- scripts/preprocess.py  
  Cleans raw comments and removes non-Hebrew characters.  
  Converts JSON to CSV.  
  Output: data/processed/comments.csv

- scripts/text_analysis.py  
  Performs word counts, topic distribution and Chi-Square analysis.  
  Output: data/processed/summary.txt

---

## How to run (local)

1. (Optional) Set your YouTube API key:

    export YT_API_KEY="YOUR_API_KEY"

2. (Optional) Fetch comments:

    python scripts/youtube_fetch.py

3. (Optional) Preprocess data:

    python scripts/preprocess.py

4. Run analysis:

    python scripts/text_analysis.py

The summary will be saved to:

    data/processed/summary.txt

---

## Docker

The Docker image is configured to run only the analysis script by default.

Build the image:

    docker build -t hebrew-analysis .

Run the container:
    
    docker run --rm hebrew-analysis
    
                      or 
                      
    docker run --rm -e YT_API_KEY=$YT_API_KEY hebrew-analysis

Inside the container, the summary is located at:

    /app/data/processed/summary.txt

---

## Limitations

- Small dataset (illustrative results only)
- No lemmatization or advanced normalization
- Chi-Square limited to top 10 words
- No visualizations yet

---

## Stopwords

Stopwords are based on:

NNLP-IL Stop Words Hebrew  
https://github.com/NNLP-IL/Stop-Words-Hebrew

All credit to the original authors.

---


## Project structure

```HEBREW-SOCIAL-TEXT-ANALYSIS/
├── data/
│   ├── processed/
│   │   └── comments.csv
│   └── raw/
│       ├── comments.json
│       ├── comments_raw.csv
│       ├── stopwords.txt
│       └── videolist.csv
├── scripts/
│   ├── preprocess.py
│   ├── text_analysis.py
│   └── youtube_fetch.py
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt```
