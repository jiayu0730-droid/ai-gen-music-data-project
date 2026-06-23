from pathlib import Path
import time
import re

import pandas as pd
import requests


DATA_DIR = Path("data")

QUERY_FILE = DATA_DIR / "youtube_market_queries.csv"
OUTPUT_RAW = DATA_DIR / "itunes_market_supply_raw.csv"
OUTPUT_SUMMARY = DATA_DIR / "itunes_market_supply_summary.csv"


def clean_query_for_itunes(query: str) -> str:
    """
    YouTube query 里可能有 shorts / music video 等词。
    iTunes 主要查音乐 catalog，所以这里做简单清理。
    """
    query = str(query)
    query = re.sub(r"\bshorts\b", "", query, flags=re.IGNORECASE)
    query = re.sub(r"\bmusic video\b", "music", query, flags=re.IGNORECASE)
    query = re.sub(r"\s+", " ", query).strip()
    return query


def fetch_itunes_results(country_code: str, query: str, limit: int = 50):
    url = "https://itunes.apple.com/search"

    params = {
        "term": query,
        "country": country_code,
        "media": "music",
        "entity": "song",
        "limit": limit,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get("results", [])


def main():
    if not QUERY_FILE.exists():
        raise FileNotFoundError(f"Missing file: {QUERY_FILE}")

    queries = pd.read_csv(QUERY_FILE)

    all_rows = []

    for _, row in queries.iterrows():
        country_code = row["country_code"]
        original_query = row["query"]
        itunes_query = clean_query_for_itunes(original_query)

        print(f"Fetching iTunes supply: {country_code} | {itunes_query}")

        try:
            results = fetch_itunes_results(
                country_code=country_code,
                query=itunes_query,
                limit=50,
            )
        except Exception as e:
            print(f"Failed: {country_code} | {itunes_query} | {e}")
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
    raw.to_csv(OUTPUT_RAW, index=False)

    summary = (
        raw.groupby(
            [
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
        )
        .agg(
            itunes_catalog_count=("result_found", "sum"),
            unique_artists=("artist_name", "nunique"),
            unique_itunes_genres=("primary_genre_name", "nunique"),
            avg_track_price=("track_price", "mean"),
        )
        .reset_index()
        .sort_values("itunes_catalog_count", ascending=True)
    )

    summary.to_csv(OUTPUT_SUMMARY, index=False)

    print("\nSaved:")
    print(OUTPUT_RAW)
    print(OUTPUT_SUMMARY)

    print("\nLowest supply examples:")
    print(summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
    