import pandas as pd
from pathlib import Path


def analyze_itunes():
    print("\n==============================")
    print("iTunes Data Analysis")
    print("==============================")

    itunes_path = "data/itunes_music_data.csv"

    if not Path(itunes_path).exists():
        print("iTunes data file not found. Please run src/fetch_itunes.py first.")
        return

    df = pd.read_csv(itunes_path)

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nTop genres:")
    print(df["genre"].value_counts().head(10))

    print("\nTop artists:")
    print(df["artist_name"].value_counts().head(10))

    print("\nAverage track price:")
    print(df["track_price"].mean())

    genre_summary = (
        df.groupby("genre")
        .agg(
            num_tracks=("track_name", "count"),
            avg_price=("track_price", "mean")
        )
        .reset_index()
        .sort_values("num_tracks", ascending=False)
    )

    genre_summary.to_csv("data/itunes_genre_summary.csv", index=False)

    print("\nSaved iTunes genre summary to data/itunes_genre_summary.csv")


def analyze_spotify():
    print("\n==============================")
    print("Spotify Data Analysis")
    print("==============================")

    spotify_path = "data/spotify_artist_data.csv"

    if not Path(spotify_path).exists():
        print("Spotify data file not found. Please run src/fetch_spotify.py first.")
        return

    df = pd.read_csv(spotify_path)

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nArtists ranked by followers:")
    print(
        df[["artist_name", "followers", "popularity", "genres"]]
        .sort_values("followers", ascending=False)
    )

    print("\nArtists ranked by popularity:")
    print(
        df[["artist_name", "followers", "popularity", "genres"]]
        .sort_values("popularity", ascending=False)
    )

    print("\nAverage followers:")
    print(df["followers"].mean())

    print("\nAverage popularity score:")
    print(df["popularity"].mean())

    spotify_summary = (
        df[["artist_name", "followers", "popularity", "genres", "spotify_url"]]
        .sort_values("followers", ascending=False)
    )

    spotify_summary.to_csv("data/spotify_artist_summary.csv", index=False)

    print("\nSaved Spotify artist summary to data/spotify_artist_summary.csv")


def compare_platforms():
    print("\n==============================")
    print("Platform Data Availability Comparison")
    print("==============================")

    comparison = pd.DataFrame({
        "data_type": [
            "Track Name",
            "Artist Name",
            "Album Name",
            "Genre",
            "Release Date",
            "Track Price",
            "Preview URL",
            "Artist Followers",
            "Popularity Score",
            "Revenue",
            "Listener Demographics",
            "User-level Listening Data"
        ],
        "itunes_available": [
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "No",
            "No",
            "No",
            "No",
            "No"
        ],
        "spotify_available": [
            "Partial",
            "Yes",
            "Partial",
            "Yes",
            "Partial",
            "No",
            "Partial",
            "Yes",
            "Yes",
            "No",
            "No",
            "No"
        ]
    })

    comparison.to_csv("data/platform_data_availability.csv", index=False)

    print(comparison)

    print("\nSaved platform comparison to data/platform_data_availability.csv")


if __name__ == "__main__":
    analyze_itunes()
    analyze_spotify()
    compare_platforms()