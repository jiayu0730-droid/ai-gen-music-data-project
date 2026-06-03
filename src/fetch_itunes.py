import requests
import pandas as pd
from pathlib import Path


def fetch_itunes_music(search_terms, limit=50):
    all_songs = []

    for term in search_terms:
        url = "https://itunes.apple.com/search"

        params = {
            "term": term,
            "media": "music",
            "entity": "song",
            "limit": limit,
            "country": "us"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for item in data.get("results", []):
            all_songs.append({
                "search_term": term,
                "track_name": item.get("trackName"),
                "artist_name": item.get("artistName"),
                "album_name": item.get("collectionName"),
                "release_date": item.get("releaseDate"),
                "genre": item.get("primaryGenreName"),
                "track_price": item.get("trackPrice"),
                "currency": item.get("currency"),
                "preview_url": item.get("previewUrl"),
                "itunes_url": item.get("trackViewUrl")
            })

    df = pd.DataFrame(all_songs)

    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/itunes_music_data.csv", index=False)

    print(df.head())
    print(f"Saved {len(df)} rows to data/itunes_music_data.csv")

    return df


if __name__ == "__main__":
    search_terms = [
        "AI generated music",
        "Taylor Swift",
        "Drake",
        "The Weeknd",
        "Suno AI music"
    ]

    fetch_itunes_music(search_terms)