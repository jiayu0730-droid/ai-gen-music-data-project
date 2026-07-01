import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = "data/youtube_theme_classification.csv"
OUTPUT_FILE = "data/subgenre_opportunity_score.csv"


def min_max_scale(series):
    if series.max() == series.min():
        return series * 0
    return (series - series.min()) / (series.max() - series.min())


def safe_divide(a, b):
    return a / b if b != 0 else 0


def classify_opportunity(score):
    if score >= 20:
        return "Immediate Production Candidate"
    elif score >= 10:
        return "Experimental Candidate"
    else:
        return "Low Priority"


def main():
    df = pd.read_csv(INPUT_FILE)

    required_cols = [
        "genre", "theme", "subgenre",
        "view_count", "like_count", "comment_count"
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    for col in ["view_count", "like_count", "comment_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["like_rate"] = df.apply(
        lambda row: safe_divide(row["like_count"], row["view_count"]),
        axis=1
    )

    df["comment_rate"] = df.apply(
        lambda row: safe_divide(row["comment_count"], row["view_count"]),
        axis=1
    )

    df["engagement_rate"] = df.apply(
        lambda row: safe_divide(
            row["like_count"] + row["comment_count"],
            row["view_count"]
        ),
        axis=1
    )

    summary = (
        df.groupby(["genre", "theme", "subgenre"])
        .agg(
            video_count=("subgenre", "count"),
            total_views=("view_count", "sum"),
            median_views=("view_count", "median"),
            total_likes=("like_count", "sum"),
            total_comments=("comment_count", "sum"),
            avg_like_rate=("like_rate", "mean"),
            avg_comment_rate=("comment_rate", "mean"),
            avg_engagement_rate=("engagement_rate", "mean"),
        )
        .reset_index()
    )

    # Demand-side scores
    summary["view_score"] = min_max_scale(np.log1p(summary["total_views"]))
    summary["like_score"] = min_max_scale(summary["avg_like_rate"])
    summary["comment_score"] = min_max_scale(summary["avg_comment_rate"])
    summary["engagement_score"] = min_max_scale(summary["avg_engagement_rate"])

    # Demand / impact score
    summary["subgenre_impact_score"] = (
        0.45 * summary["view_score"]
        + 0.25 * summary["like_score"]
        + 0.20 * summary["comment_score"]
        + 0.10 * summary["engagement_score"]
    ) * 100

    # Supply / competition score
    summary["supply_score"] = min_max_scale(np.log1p(summary["video_count"])) * 100

    # Confidence score: avoid over-ranking subgenres with only 1–2 videos
    summary["confidence_score"] = (
        np.log1p(summary["video_count"])
        / np.log1p(summary["video_count"].max())
    )

    # Old score kept for comparison
    summary["raw_opportunity_score"] = (
        summary["subgenre_impact_score"] - summary["supply_score"]
    )

    # New market opportunity score
    summary["market_opportunity_score"] = (
        summary["subgenre_impact_score"]
        * summary["confidence_score"]
        * (1 - summary["supply_score"] / 100)
    )

    summary["opportunity_level"] = summary["market_opportunity_score"].apply(
        classify_opportunity
    )

    result = summary.sort_values("market_opportunity_score", ascending=False)

    Path("data").mkdir(exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("Subgenre Market Opportunity Score:")
    print(result.head(30).to_string(index=False))
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()