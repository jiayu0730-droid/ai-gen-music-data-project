import pandas as pd


def analyze_itunes_data():
    df = pd.read_csv("data/itunes_music_data.csv")

    print("Dataset shape:")
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

    print("\nSaved summary to data/itunes_genre_summary.csv")


if __name__ == "__main__":
    analyze_itunes_data()