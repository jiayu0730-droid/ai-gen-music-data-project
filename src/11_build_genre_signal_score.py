import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = "data/youtube_genre_engagement_summary.csv"
OUTPUT_FILE = "data/genre_signal_opportunity_score.csv"


def min_max_scale(series):
    """Scale a numeric series to 0-1 range."""
    if series.max() == series.min():
        return series * 0
    return (series - series.min()) / (series.max() - series.min())


def classify_opportunity(score):
    if score >= 30:
        return "High Opportunity"
    elif score >= 10:
        return "Medium Opportunity"
    else:
        return "Low Opportunity"


def main():
    df = pd.read_csv(INPUT_FILE)

    numeric_cols = [
        "video_count",
        "total_views",
        "median_views",
        "total_likes",
        "total_comments",
        "avg_like_rate",
        "avg_comment_rate",
        "avg_engagement_rate",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["view_score"] = min_max_scale(np.log1p(df["total_views"]))
    df["like_score"] = min_max_scale(df["avg_like_rate"])
    df["comment_score"] = min_max_scale(df["avg_comment_rate"])
    df["engagement_score"] = min_max_scale(df["avg_engagement_rate"])

    df["genre_impact_score"] = (
        0.45 * df["view_score"]
        + 0.25 * df["like_score"]
        + 0.20 * df["comment_score"]
        + 0.10 * df["engagement_score"]
    ) * 100

    df["supply_score"] = min_max_scale(np.log1p(df["video_count"])) * 100
    df["opportunity_score"] = df["genre_impact_score"] - df["supply_score"]
    df["opportunity_level"] = df["opportunity_score"].apply(classify_opportunity)

    output_cols = [
        "genre",
        "video_count",
        "total_views",
        "median_views",
        "avg_like_rate",
        "avg_comment_rate",
        "avg_engagement_rate",
        "view_score",
        "like_score",
        "comment_score",
        "engagement_score",
        "genre_impact_score",
        "supply_score",
        "opportunity_score",
        "opportunity_level",
        "listening_behavior",
    ]

    Path("data").mkdir(exist_ok=True)

    result = df[output_cols].sort_values(
        "opportunity_score", ascending=False
    )

    result.to_csv(OUTPUT_FILE, index=False)

    print("Genre Signal Opportunity Score:")
    print(result.to_string(index=False))
    print(f"\nSaved result to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
