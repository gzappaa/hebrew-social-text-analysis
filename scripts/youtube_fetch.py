import json
import pandas as pd
from googleapiclient.discovery import build
from pathlib import Path
import os

# ===== YOUTUBE API KEY =====
API_KEY = os.getenv("YT_API_KEY")
if not API_KEY:
    raise ValueError("YT_API_KEY environment variable is not set!")

# ===== CONFIGURATION =====
MAX_COMMENTS_PER_VIDEO = 10

# ===== PATHS =====
script_dir = Path(__file__).parent
video_csv = script_dir.parent / "data/videolist.csv"       # CSV with video IDs and topics
output_file = script_dir.parent / "data/raw/comments.json"  # where to save JSON

# ===== HEBREW LETTERS =====
hebrew_letters = list("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")

# ===== LOAD VIDEO LIST =====
video_df = pd.read_csv(video_csv)

# ===== INITIALIZE YOUTUBE API =====
youtube = build("youtube", "v3", developerKey=API_KEY)

all_comments = []

for _, row in video_df.iterrows():
    video_id = row['video_id']
    topic = row['topic']
    comments_list = []
    next_page_token = None

    while len(comments_list) < MAX_COMMENTS_PER_VIDEO:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]

            # filter comment if it contains at least one Hebrew letter
            if any(l in comment for l in hebrew_letters):
                comments_list.append({
                    "video_id": video_id,
                    "topic": topic,
                    "author": author,
                    "text": comment,
                    "published_at": published_at,
                    "likes": likes
                })

            if len(comments_list) >= MAX_COMMENTS_PER_VIDEO:
                break

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    all_comments.extend(comments_list)
    print(f"{len(comments_list)} comments collected for video {video_id} ({topic})")

# ===== SAVE JSON =====
output_file.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
with output_file.open("w", encoding="utf-8") as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=2)

print(f"Total comments saved: {len(all_comments)} in {output_file}")
