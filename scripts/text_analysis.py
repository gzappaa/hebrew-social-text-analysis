from pathlib import Path
import pandas as pd
from collections import Counter
from scipy.stats import chi2_contingency
from bidi.algorithm import get_display  # For proper Hebrew text display in terminal

# ------------------------------
# 1. Load the CSV
# ------------------------------
DATA_PATH = Path("data/comments_raw.csv")
df = pd.read_csv(DATA_PATH)

# ------------------------------
# 2. Clean the data
# ------------------------------
# Remove rows where Topic or Tweet is missing
df = df.dropna(subset=["Topic", "Tweet"])

# Ensure the columns are strings
df["Topic"] = df["Topic"].astype(str)
df["Tweet"] = df["Tweet"].astype(str)

# ------------------------------
# 3. Show the distribution of topics
# ------------------------------
topic_counts = df['Topic'].value_counts()
print("Topic Distribution:")
print(topic_counts)
print("\n")  # empty line for readability

# ------------------------------
# 4. Count words in each comment
# ------------------------------
# Create a new column with the number of words per comment
df['Word_Count'] = df['Tweet'].apply(lambda x: len(x.split()))
print("Word counts for first 5 comments:")
print(df[['Tweet', 'Word_Count']].head())
print("\n")

# ------------------------------
# 5. Show most common words across all comments
# ------------------------------
all_words = ' '.join(df['Tweet']).split()
word_counts = Counter(all_words)

print("\n10 most common words:")
for word, count in word_counts.most_common(10):
    # Use get_display to correctly show Hebrew words in terminal
    print(f"{get_display(word)} : {count}")

# ------------------------------
# 6. Contingency Table and Chi-Square Test
# ------------------------------
# Loop over the top 10 words and run chi-square test
for word, count in word_counts.most_common(10):
    # Create a binary column: 1 if the word appears in the comment, 0 if not
    df[word] = df['Tweet'].apply(lambda x: int(word in x))
    
    # Build a contingency table for Topic vs. word presence
    table = pd.crosstab(df['Topic'], df[word])
    
    # Run Chi-Square test
    chi2, p, dof, expected = chi2_contingency(table)
    
    print(f"\nWord: '{get_display(word)}'")
    print("Contingency Table:\n", table)
    print(f"Chi2 = {chi2:.2f}, p-value = {p:.4f}, dof = {dof}")
