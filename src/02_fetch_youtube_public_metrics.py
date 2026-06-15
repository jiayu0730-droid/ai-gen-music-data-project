import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


DATA_DIR = Path("data")
QUERY_FILE = DATA_DIR / "youtube_market_queries.csv"
OUTPUT_RAW = DATA_DIR / "youtube_public_video_metrics.csv"
OUTPUT_SUMMARY = DATA_DIR / "youtube_public_market_summary.csv"


def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing YOUTUBE_API_KEY. Please check your .env file."
        )

    return api_key


def search_youtube_videos(api_key: str, query: str, region_code: str, max_results: int = 25):
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    video_ids = []
    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        if video_id:
            video_ids.append(video_id)

    return video_ids


def fetch_video_metrics(api_key: str, video_ids: list[str]):
    if not video_ids:
        return []

    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,statistics",
        "id": ",".join(video_ids),
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    rows = []

    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})

        view_count = int(stats.get("viewCount", 0))
        like_count = int(stats.get("likeCount", 0))
        comment_count = int(stats.get("commentCount", 0))

        rows.append(
            {
                "video_id": item.get("id"),
                "title": snippet.get("title"),
                "channel_title": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt"),
                "view_count": view_count,
                "like_count": like_count,
                "comment_count": comment_count,
                "youtube_url": f"https://www.youtube.com/watch?v={item.get('id')}",
            }
        )

    return rows


def build_youtube_dataset():
    api_key = load_api_key()

    if not QUERY_FILE.exists():
        raise FileNotFoundError(f"Missing query file: {QUERY_FILE}")

    queries = pd.read_csv(QUERY_FILE)
    all_rows = []

    for _, query_row in queries.iterrows():
        country_code = query_row["country_code"]
        query = query_row["query"]

        print(f"Fetching YouTube data: {country_code} | {query}")

        video_ids = search_youtube_videos(
            api_key=api_key,
            query=query,
            region_code=country_code,
            max_results=25,
        )

        metric_rows = fetch_video_metrics(api_key, video_ids)

        for metric_row in metric_rows:
            combined_row = {
                **query_row.to_dict(),
                **metric_row,
            }
            all_rows.append(combined_row)

        time.sleep(0.3)

    df = pd.DataFrame(all_rows)

    if df.empty:
        raise ValueError("No YouTube results returned. Check your API key or query terms.")

    df["engagement_total"] = df["like_count"] + df["comment_count"]
    df["like_rate"] = df["like_count"] / df["view_count"].replace(0, pd.NA)
    df["comment_rate"] = df["comment_count"] / df["view_count"].replace(0, pd.NA)

    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_RAW, index=False)

    summary = (
        df.groupby(
            [
                "country_code",
                "country_name",
                "genre",
                "content_type",
                "lyric_style",
                "language",
                "query",
            ]
        )
        .agg(
            video_count=("video_id", "count"),
            total_views=("view_count", "sum"),
            median_views=("view_count", "median"),
            total_likes=("like_count", "sum"),
            total_comments=("comment_count", "sum"),
            avg_like_rate=("like_rate", "mean"),
            avg_comment_rate=("comment_rate", "mean"),
        )
        .reset_index()
        .sort_values("total_views", ascending=False)
    )

    summary.to_csv(OUTPUT_SUMMARY, index=False)

    print("\nSaved:")
    print(OUTPUT_RAW)
    print(OUTPUT_SUMMARY)

    print("\nTop results:")
    print(summary.head(10).to_string(index=False))


if __name__ == "__main__":
    build_youtube_dataset()
    