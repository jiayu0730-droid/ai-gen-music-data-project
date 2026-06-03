import requests
import pandas as pd

url = "https://itunes.apple.com/search"

params = {
    "term": "Taylor Swift",
    "media": "music",
    "entity": "song",
    "limit": 20
}

response = requests.get(url, params=params)

data = response.json()

songs = []

for item in data["results"]:
    songs.append({
        "track_name": item.get("trackName"),
        "artist_name": item.get("artistName"),
        "album_name": item.get("collectionName"),
        "release_date": item.get("releaseDate"),
        "genre": item.get("primaryGenreName"),
        "price": item.get("trackPrice")
    })

df = pd.DataFrame(songs)

df.to_csv(
    "data/itunes_songs.csv",
    index=False
)

print(df.head())
print(f"Saved {len(df)} songs")