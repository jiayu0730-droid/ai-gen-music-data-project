import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("Missing Spotify credentials. Please check your .env file.")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

artists = [
    "Taylor Swift",
    "Drake",
    "The Weeknd",
    "Bad Bunny",
    "Ariana Grande"
]

results = []

for artist in artists:
    search_result = sp.search(q=artist, type="artist", limit=1)
    items = search_result.get("artists", {}).get("items", [])

    if not items:
        continue

    artist_data = items[0]

    results.append({
        "search_term": artist,
        "artist_name": artist_data.get("name"),
        "spotify_artist_id": artist_data.get("id"),
        "followers": artist_data.get("followers", {}).get("total"),
        "popularity": artist_data.get("popularity"),
        "genres": ", ".join(artist_data.get("genres", [])),
        "spotify_url": artist_data.get("external_urls", {}).get("spotify")
    })

df = pd.DataFrame(results)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/spotify_artist_data.csv", index=False)

print(df.to_string(index=False))
print(f"\nSaved {len(df)} artists to data/spotify_artist_data.csv")