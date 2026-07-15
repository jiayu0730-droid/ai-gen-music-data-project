"""
01_collect_data.py

User-facing stage 1:
- Build platform evidence table
- Fetch YouTube public metrics
- Fetch iTunes catalog-supply data

Run examples:
    python src/01_collect_data.py --platform-evidence
    python src/01_collect_data.py --youtube
    python src/01_collect_data.py --itunes
    python src/01_collect_data.py --all
"""

from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


DATA_DIR = Path("data")
REPORT_DIR = Path("reports")

YOUTUBE_QUERY_FILE = DATA_DIR / "youtube_market_queries.csv"
YOUTUBE_RAW_FILE = DATA_DIR / "youtube_public_video_metrics.csv"
YOUTUBE_SUMMARY_FILE = DATA_DIR / "youtube_public_market_summary.csv"

ITUNES_RAW_FILE = DATA_DIR / "itunes_market_supply_raw.csv"
ITUNES_SUMMARY_FILE = DATA_DIR / "itunes_market_supply_summary.csv"


def ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)


def build_platform_evidence_table() -> None:
    sources_path = DATA_DIR / "platform_data_sources_step1.csv"
    observations_path = DATA_DIR / "platform_observation_seed.csv"

    if not sources_path.exists() or not observations_path.exists():
        raise FileNotFoundError(
            "Missing platform evidence input files in data/: "
            "platform_data_sources_step1.csv and/or platform_observation_seed.csv"
        )

    sources = pd.read_csv(sources_path)
    observations = pd.read_csv(observations_path)

    priority_map = {"high": 3, "medium": 2, "low": 1}
    observations["confidence_score"] = (
        observations["confidence_level"].astype(str).str.lower().map(priority_map).fillna(1)
    )

    actionable_keywords = ["export", "collect", "api", "manual"]
    observations["actionable"] = observations["next_action"].fillna("").astype(str).str.lower().apply(
        lambda x: any(k in x for k in actionable_keywords)
    )
    observations["data_collection_priority"] = (
        observations["confidence_score"] + observations["actionable"].astype(int)
    )

    priority = observations.sort_values(
        ["data_collection_priority", "confidence_score"], ascending=False
    )

    source_cols = [
        "platform",
        "platform_group",
        "public_data_available",
        "actual_method",
        "metrics_available_or_needed",
        "how_to_use_in_project",
    ]
    missing_source_cols = [c for c in source_cols if c not in sources.columns]
    if missing_source_cols:
        raise ValueError(f"Missing source columns: {missing_source_cols}")

    merged = priority.merge(sources[source_cols], on="platform", how="left")
    merged.to_csv(DATA_DIR / "platform_evidence_priority.csv", index=False)

    platform_summary = (
        merged.groupby(
            ["platform", "platform_group", "public_data_available", "actual_method"],
            dropna=False,
        )
        .agg(
            num_observations=("claim_or_observation", "count"),
            avg_priority=("data_collection_priority", "mean"),
            key_metrics=("metrics_available_or_needed", "first"),
            project_use=("how_to_use_in_project", "first"),
        )
        .reset_index()
        .sort_values("avg_priority", ascending=False)
    )
    platform_summary.to_csv(DATA_DIR / "platform_evidence_summary.csv", index=False)

    md_lines = [
        "# Platform Streaming Data Evidence Plan",
        "",
        "## Key idea",
        "",
        "Separate public engagement data from private royalty/dashboard data.",
        "The current objective is to validate audience demand and market fit before optimizing for revenue.",
        "",
        "## Prioritized platforms",
        "",
    ]

    for _, row in platform_summary.iterrows():
        md_lines.append(
            f"- **{row['platform']}**: method = {row['actual_method']}; "
            f"metrics = {row['key_metrics']}; use = {row['project_use']}"
        )

    md_lines.extend(["", "## Next data to collect", ""])
    for _, row in priority.head(10).iterrows():
        md_lines.append(
            f"- **{row['platform']}** — {row['claim_or_observation']} → {row['next_action']}"
        )

    (REPORT_DIR / "platform_streaming_evidence_plan.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )
    print("Platform evidence outputs generated.")


def load_youtube_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("Missing YOUTUBE_API_KEY in .env")
    return api_key


def search_youtube_videos(
    api_key: str,
    query: str,
    region_code: str,
    max_results: int = 25,
) -> list[str]:
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params={
            "part": "snippet",
            "q": query,
            "type": "video",
            "videoCategoryId": "10",
            "regionCode": region_code,
            "maxResults": max_results,
            "key": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    return [
        item.get("id", {}).get("videoId")
        for item in response.json().get("items", [])
        if item.get("id", {}).get("videoId")
    ]


def fetch_youtube_video_metrics(api_key: str, video_ids: list[str]) -> list[dict]:
    if not video_ids:
        return []

    response = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
            "key": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()

    rows = []
    for item in response.json().get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        video_id = item.get("id")
        rows.append(
            {
                "video_id": video_id,
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "channel_title": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt"),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
            }
        )
    return rows


def fetch_youtube_public_metrics(max_results: int = 25) -> None:
    if not YOUTUBE_QUERY_FILE.exists():
        raise FileNotFoundError(f"Missing query file: {YOUTUBE_QUERY_FILE}")

    api_key = load_youtube_api_key()
    queries = pd.read_csv(YOUTUBE_QUERY_FILE)
    all_rows: list[dict] = []

    for _, query_row in queries.iterrows():
        country_code = str(query_row["country_code"])
        query = str(query_row["query"])
        print(f"YouTube: {country_code} | {query}")

        video_ids = search_youtube_videos(
            api_key=api_key,
            query=query,
            region_code=country_code,
            max_results=max_results,
        )
        metric_rows = fetch_youtube_video_metrics(api_key, video_ids)

        for metric_row in metric_rows:
            all_rows.append({**query_row.to_dict(), **metric_row})

        time.sleep(0.3)

    df = pd.DataFrame(all_rows)
    if df.empty:
        raise ValueError("No YouTube results returned.")

    for col in ["view_count", "like_count", "comment_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["engagement_total"] = df["like_count"] + df["comment_count"]
    safe_views = df["view_count"].replace(0, pd.NA)
    df["like_rate"] = df["like_count"] / safe_views
    df["comment_rate"] = df["comment_count"] / safe_views

    df.to_csv(YOUTUBE_RAW_FILE, index=False)

    group_cols = [
        "country_code",
        "country_name",
        "genre",
        "content_type",
        "lyric_style",
        "language",
        "query",
    ]
    summary = (
        df.groupby(group_cols)
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
    summary.to_csv(YOUTUBE_SUMMARY_FILE, index=False)
    print("YouTube outputs generated.")


def clean_query_for_itunes(query: str) -> str:
    query = re.sub(r"\bshorts\b", "", str(query), flags=re.IGNORECASE)
    query = re.sub(r"\bmusic video\b", "music", query, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", query).strip()


def fetch_itunes_results(country_code: str, query: str, limit: int = 50) -> list[dict]:
    response = requests.get(
        "https://itunes.apple.com/search",
        params={
            "term": query,
            "country": country_code,
            "media": "music",
            "entity": "song",
            "limit": limit,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("results", [])


def fetch_itunes_market_supply(limit: int = 50) -> None:
    if not YOUTUBE_QUERY_FILE.exists():
        raise FileNotFoundError(f"Missing query file: {YOUTUBE_QUERY_FILE}")

    queries = pd.read_csv(YOUTUBE_QUERY_FILE)
    all_rows: list[dict] = []

    for _, row in queries.iterrows():
        country_code = str(row["country_code"])
        original_query = str(row["query"])
        itunes_query = clean_query_for_itunes(original_query)
        print(f"iTunes: {country_code} | {itunes_query}")

        try:
            results = fetch_itunes_results(country_code, itunes_query, limit=limit)
        except Exception as exc:
            print(f"Failed: {country_code} | {itunes_query} | {exc}")
            results = []

        if not results:
            all_rows.append(
                {
                    **row.to_dict(),
                    "itunes_query": itunes_query,
                    "track_name": None,
                    "artist_name": None,
                    "collection_name": None,
                    "primary_genre_name": None,
                    "release_date": None,
                    "track_price": None,
                    "currency": None,
                    "track_view_url": None,
                    "result_found": 0,
                }
            )
        else:
            for item in results:
                all_rows.append(
                    {
                        **row.to_dict(),
                        "itunes_query": itunes_query,
                        "track_name": item.get("trackName"),
                        "artist_name": item.get("artistName"),
                        "collection_name": item.get("collectionName"),
                        "primary_genre_name": item.get("primaryGenreName"),
                        "release_date": item.get("releaseDate"),
                        "track_price": item.get("trackPrice"),
                        "currency": item.get("currency"),
                        "track_view_url": item.get("trackViewUrl"),
                        "result_found": 1,
                    }
                )
        time.sleep(0.3)

    raw = pd.DataFrame(all_rows)
    raw.to_csv(ITUNES_RAW_FILE, index=False)

    group_cols = [
        "country_code",
        "country_name",
        "region_group",
        "genre",
        "content_type",
        "lyric_style",
        "language",
        "query",
        "itunes_query",
    ]
    summary = (
        raw.groupby(group_cols)
        .agg(
            itunes_catalog_count=("result_found", "sum"),
            unique_artists=("artist_name", "nunique"),
            unique_itunes_genres=("primary_genre_name", "nunique"),
            avg_track_price=("track_price", "mean"),
        )
        .reset_index()
        .sort_values("itunes_catalog_count")
    )
    summary.to_csv(ITUNES_SUMMARY_FILE, index=False)
    print("iTunes outputs generated.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform-evidence", action="store_true")
    parser.add_argument("--youtube", action="store_true")
    parser.add_argument("--itunes", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--youtube-max-results", type=int, default=25)
    parser.add_argument("--itunes-limit", type=int, default=50)
    return parser.parse_args()


def main() -> None:
    ensure_dirs()
    args = parse_args()

    if not any([args.platform_evidence, args.youtube, args.itunes, args.all]):
        raise SystemExit(
            "Choose one option: --platform-evidence, --youtube, --itunes, or --all"
        )

    if args.all or args.platform_evidence:
        build_platform_evidence_table()
    if args.all or args.youtube:
        fetch_youtube_public_metrics(max_results=args.youtube_max_results)
    if args.all or args.itunes:
        fetch_itunes_market_supply(limit=args.itunes_limit)


if __name__ == "__main__":
    main()
