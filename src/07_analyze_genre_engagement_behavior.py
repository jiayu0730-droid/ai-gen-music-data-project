import pandas as pd
from pathlib import Path

INPUT_FILE = "data/youtube_public_video_metrics.csv"

OUTPUT_GENRE_SUMMARY = "data/youtube_genre_engagement_summary.csv"
OUTPUT_BEHAVIOR_FILE = "data/youtube_genre_behavior_classification.csv"

def safe_divide(a, b):
    return a / b if b != 0 else 0

def main():
    df = pd.read_csv(INPUT_FILE)

    # 统一字段名，防止有些列是字符串
    numeric_cols = ["view_count", "like_count", "comment_count"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 计算互动率
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

    # 按 genre 汇总
    genre_summary = (
        df.groupby("genre")
        .agg(
            video_count=("video_id", "count"),
            total_views=("view_count", "sum"),
            median_views=("view_count", "median"),
            total_likes=("like_count", "sum"),
            total_comments=("comment_count", "sum"),
            avg_like_rate=("like_rate", "mean"),
            avg_comment_rate=("comment_rate", "mean"),
            avg_engagement_rate=("engagement_rate", "mean")
        )
        .reset_index()
        .sort_values("total_views", ascending=False)
    )

    # 用分位数判断行为类型
    high_views_threshold = genre_summary["median_views"].quantile(0.75)
    low_engagement_threshold = genre_summary["avg_engagement_rate"].quantile(0.25)
    high_engagement_threshold = genre_summary["avg_engagement_rate"].quantile(0.75)

    def classify_behavior(row):
        if row["median_views"] >= high_views_threshold and row["avg_engagement_rate"] <= low_engagement_threshold:
            return "Background / Looping Consumption"
        elif row["avg_engagement_rate"] >= high_engagement_threshold:
            return "Active Listening / High Engagement"
        else:
            return "Mixed / Unclear"

    genre_summary["listening_behavior"] = genre_summary.apply(classify_behavior, axis=1)

    Path("data").mkdir(exist_ok=True)

    genre_summary.to_csv(OUTPUT_GENRE_SUMMARY, index=False)
    genre_summary.to_csv(OUTPUT_BEHAVIOR_FILE, index=False)

    print("\nGenre Engagement Summary:")
    print(genre_summary)

    print(f"\nSaved to {OUTPUT_GENRE_SUMMARY}")
    print(f"Saved to {OUTPUT_BEHAVIOR_FILE}")

if __name__ == "__main__":
    main()