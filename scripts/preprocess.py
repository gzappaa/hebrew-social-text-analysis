import json
import pandas as pd
from pathlib import Path
import re

# ===== INPUT/OUTPUT FILES =====
script_dir = Path(__file__).parent
input_file = script_dir.parent / "data/raw/comments.json"
output_file = script_dir.parent / "data/processed/comments.csv"

# ===== READ JSON =====
with input_file.open("r", encoding="utf-8") as f:
    comments = json.load(f)

# ===== CREATE DATAFRAME =====
df = pd.DataFrame(comments)

# ===== RENAME COLUMNS =====
df.rename(columns={"text": "Comment", "author": "Author"}, inplace=True)

# ===== GET ACTUAL TOPIC =====
df["Topic"] = df["topic"]        # use topic from JSON
df.drop(columns=["topic"], inplace=True)  # remove the old column


# ===== CLEAN COMMENTS =====
df["Comment"] = df["Comment"].apply(
    lambda text: ' '.join(re.findall(r'[\u0590-\u05FF]+', text))
)

# ===== SAVE CSV =====
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Saved {len(df)} comments to {output_file}")
