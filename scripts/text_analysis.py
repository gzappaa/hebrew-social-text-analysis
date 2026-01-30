from pathlib import Path
import pandas as pd
from collections import Counter
from scipy.stats import chi2_contingency
from bidi.algorithm import get_display  # For proper Hebrew display
import re


script_dir = Path(__file__).parent  # pasta onde o script está
DATA_PATH = script_dir.parent / "data/processed/comments.csv"
STOPWORDS_PATH = script_dir.parent / "data/stopwords.txt"
# ------------------------------
# 1. Load CSV and stopwords
# ------------------------------
def load_data(csv_path: Path, stopwords_path: Path):
    """
    Load comments CSV and stopwords file.
    Returns dataframe and set of stopwords.
    """
    df = pd.read_csv(csv_path)
    with open(stopwords_path, "r", encoding="utf-8") as f:
        stopwords = set(line.strip() for line in f if line.strip())
    return df, stopwords

# ------------------------------
# 2. Clean the dataframe
# ------------------------------
def clean_data(df: pd.DataFrame):
    """
    Drop missing Topic or Comment, convert types,
    and compute word count per comment.
    """
    df = df.dropna(subset=["Topic", "Comment"])
    df["Topic"] = df["Topic"].astype(str)
    df["Comment"] = df["Comment"].astype(str)
    df['Word_Count'] = df['Comment'].apply(lambda x: len(re.findall(r'\w+', x)))
    return df

# ------------------------------
# 3. Topic distribution
# ------------------------------
def get_topic_counts(df: pd.DataFrame):
    """
    Count number of comments per topic.
    """
    return df['Topic'].value_counts()

# ------------------------------
# 4. Count words excluding stopwords
# ------------------------------
def get_word_counts(df: pd.DataFrame, stopwords: set):
    """
    Count all words across comments, excluding stopwords.
    Returns a Counter object.
    """
    all_words = ' '.join(df['Comment']).split()
    filtered = [w for w in all_words if w not in stopwords]
    return Counter(filtered)

# ------------------------------
# 5. Compute Chi-Square tables for top words
# ------------------------------
def compute_chi2_tables(df: pd.DataFrame, words: list):
    """
    Compute chi-square contingency tables for a list of words.
    
    Returns a dictionary:
        {word: (table, chi2, p-value, dof, expected)}
    """
    results = {}
    for word in words:
        # Binary presence column for the word
        df[word] = df['Comment'].apply(lambda x: int(word in x))
        
        # Contingency table
        table = pd.crosstab(df['Topic'], df[word])
        
        # Chi-square test
        chi2, p, dof, expected = chi2_contingency(table)
        results[word] = (table, chi2, p, dof, expected)
    return results

# ------------------------------
# 6. Save summary to text file
# ------------------------------
def save_summary(df: pd.DataFrame, topic_counts: pd.Series, word_counts: Counter,
                 chi2_results: dict, output_path: Path):
    """
    Save all analysis results into a text file.
    """
    with output_path.open("w", encoding="utf-8") as f:
        # Topic distribution
        f.write("Topic Distribution:\n\n")
        f.write(str(topic_counts) + "\n\n\n")

        # Word counts of first 5 comments
        f.write("Word counts for first 5 comments:\n\n")
        f.write(str(df[['Comment', 'Word_Count']].head()) + "\n\n\n")

        # Top10 words
        f.write("10 most common words:\n\n")
        for word, count in word_counts.most_common(10):
            f.write(f"{word} : {count}\n")

        f.write("\n")

        # Chi-square tables for top words
        for word, (table, chi2, p, dof, expected) in chi2_results.items():
            f.write(f"Word: '{word}'\n")
            f.write("Contingency Table:\n")
            f.write(str(table) + "\n")
            f.write(f"Chi2 = {chi2:.2f}, p-value = {p:.4f}, dof = {dof}\n\n")
    print(f"Summary saved to {output_path}")

# ------------------------------
# 7. Main script
# ------------------------------
if __name__ == "__main__":
    OUTPUT_SUMMARY = script_dir.parent / "data/processed/summary.txt"

    # Load and clean data
    df, stopwords = load_data(DATA_PATH, STOPWORDS_PATH)
    df = clean_data(df)

    # Topic counts and word counts
    topic_counts = get_topic_counts(df)
    word_counts = get_word_counts(df, stopwords)

    # Top 10 words for chi-square
    top_words = [word for word, _ in word_counts.most_common(10)]
    chi2_results = compute_chi2_tables(df, top_words)

    # Print terminal output
    print("Topic Distribution:\n")
    print(topic_counts)
    print("\nWord counts for first 5 comments:\n")
    print(df[['Comment', 'Word_Count']].head())
    print("\n10 most common words:\n")
    for word, count in word_counts.most_common(10):
        print(f"{get_display(word)} : {count}")

    for word, (table, chi2, p, dof, expected) in chi2_results.items():
        print(f"\nWord: '{get_display(word)}'")
        print("Contingency Table:\n", table)
        print(f"Chi2 = {chi2:.2f}, p-value = {p:.4f}, dof = {dof}")

    # Save summary to file
    save_summary(df, topic_counts, word_counts, chi2_results, OUTPUT_SUMMARY)