from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATA_DIR = Path("data")
REPORT_DIR = Path("reports")
FIGURE_DIR = Path("figures")

RAW_FILE = DATA_DIR / "youtube_public_video_metrics.csv"
SUMMARY_FILE = DATA_DIR / "youtube_public_market_summary.csv"

REPORT_DIR.mkdir(exist_ok=True)
FIGURE_DIR.mkdir(exist_ok=True)


def minmax(series: pd.Series) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce").fillna(0)

    if series.max() == series.min():
        return pd.Series([0.5] * len(series), index=series.index)

    return (series - series.min()) / (series.max() - series.min())


def load_youtube_data():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Missing file: {RAW_FILE}")

    if not SUMMARY_FILE.exists():
        raise FileNotFoundError(f"Missing file: {SUMMARY_FILE}")

    raw = pd.read_csv(RAW_FILE)
    summary = pd.read_csv(SUMMARY_FILE)

    numeric_cols = [
        "view_count",
        "like_count",
        "comment_count",
        "engagement_total",
        "like_rate",
        "comment_rate",
    ]

    for col in numeric_cols:
        if col in raw.columns:
            raw[col] = pd.to_numeric(raw[col], errors="coerce").fillna(0)

    summary_numeric_cols = [
        "video_count",
        "total_views",
        "median_views",
        "total_likes",
        "total_comments",
        "avg_like_rate",
        "avg_comment_rate",
    ]

    for col in summary_numeric_cols:
        if col in summary.columns:
            summary[col] = pd.to_numeric(summary[col], errors="coerce").fillna(0)

    return raw, summary


def build_analysis_tables(raw: pd.DataFrame, summary: pd.DataFrame):
    # 1. Country-level performance
    country_summary = (
        raw.groupby(["country_code", "country_name"])
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

    # 2. Content type comparison: instrumental vs lyrical
    content_type_summary = (
        raw.groupby(["content_type"])
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

    # 3. Genre-level performance
    genre_summary = (
        raw.groupby(["genre"])
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

    # 4. Country + genre + content type
    market_content_summary = (
        raw.groupby(["country_code", "country_name", "genre", "content_type", "lyric_style", "language", "query"])
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
    )

    # 5. YouTube opportunity score
    # 当前阶段：播放量最重要，其次互动率
    market_content_summary["views_score"] = minmax(np.log1p(market_content_summary["total_views"]))
    market_content_summary["median_views_score"] = minmax(np.log1p(market_content_summary["median_views"]))
    market_content_summary["like_rate_score"] = minmax(market_content_summary["avg_like_rate"])
    market_content_summary["comment_rate_score"] = minmax(market_content_summary["avg_comment_rate"])

    market_content_summary["youtube_opportunity_score"] = (
        0.50 * market_content_summary["views_score"]
        + 0.20 * market_content_summary["median_views_score"]
        + 0.15 * market_content_summary["like_rate_score"]
        + 0.15 * market_content_summary["comment_rate_score"]
    )

    market_content_summary = market_content_summary.sort_values(
        "youtube_opportunity_score",
        ascending=False,
    )

    country_summary.to_csv(DATA_DIR / "youtube_country_summary.csv", index=False)
    content_type_summary.to_csv(DATA_DIR / "youtube_content_type_summary.csv", index=False)
    genre_summary.to_csv(DATA_DIR / "youtube_genre_summary.csv", index=False)
    market_content_summary.to_csv(DATA_DIR / "youtube_market_opportunity_score.csv", index=False)

    return country_summary, content_type_summary, genre_summary, market_content_summary


def create_figures(country_summary, content_type_summary, genre_summary, market_content_summary):
    # Figure 1: Top market/query opportunities
    top_queries = market_content_summary.head(10).copy()
    top_queries["label"] = (
        top_queries["country_code"]
        + " | "
        + top_queries["genre"]
        + " | "
        + top_queries["content_type"]
    )

    plt.figure(figsize=(12, 7))
    plt.barh(top_queries["label"], top_queries["youtube_opportunity_score"])
    plt.xlabel("YouTube Opportunity Score")
    plt.ylabel("Market / Genre / Content Type")
    plt.title("Top YouTube Market Opportunities")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "top_youtube_market_opportunities.png", dpi=300)
    plt.close()

    # Figure 2: Content type comparison
    plt.figure(figsize=(8, 6))
    plt.bar(content_type_summary["content_type"], content_type_summary["total_views"])
    plt.xlabel("Content Type")
    plt.ylabel("Total Views")
    plt.title("YouTube Views by Content Type")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "youtube_views_by_content_type.png", dpi=300)
    plt.close()

    # Figure 3: Genre comparison
    plt.figure(figsize=(8, 6))
    plt.bar(genre_summary["genre"], genre_summary["total_views"])
    plt.xlabel("Genre")
    plt.ylabel("Total Views")
    plt.title("YouTube Views by Genre")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "youtube_views_by_genre.png", dpi=300)
    plt.close()

    # Figure 4: Country comparison
    plt.figure(figsize=(10, 6))
    plt.bar(country_summary["country_code"], country_summary["total_views"])
    plt.xlabel("Country")
    plt.ylabel("Total Views")
    plt.title("YouTube Views by Country")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "youtube_views_by_country.png", dpi=300)
    plt.close()


def write_markdown_report(country_summary, content_type_summary, genre_summary, market_content_summary):
    top_country = country_summary.iloc[0]
    top_content = content_type_summary.iloc[0]
    top_genre = genre_summary.iloc[0]
    top_market = market_content_summary.iloc[0]

    report = f"""# YouTube Public Market Analysis

## Purpose

This analysis uses public YouTube video metrics to evaluate early demand signals for AI-generated music across different countries, genres, and content formats. The current goal is not to estimate full platform revenue, but to identify which markets and music formats show stronger audience discovery potential.

## Key Findings

### 1. Strongest Country-Level Signal

The highest total YouTube view volume in the current sample came from:

- Country: {top_country["country_name"]} ({top_country["country_code"]})
- Total views: {int(top_country["total_views"]):,}
- Median views: {int(top_country["median_views"]):,}
- Total likes: {int(top_country["total_likes"]):,}
- Total comments: {int(top_country["total_comments"]):,}

### 2. Instrumental vs. Lyrical Content

The stronger content type in the current YouTube sample was:

- Content type: {top_content["content_type"]}
- Total views: {int(top_content["total_views"]):,}
- Median views: {int(top_content["median_views"]):,}
- Average like rate: {top_content["avg_like_rate"]:.4f}
- Average comment rate: {top_content["avg_comment_rate"]:.4f}

This result should be interpreted as an early demand signal rather than a final conclusion, because YouTube search results reflect public visibility and algorithmic ranking rather than controlled experimental exposure.

### 3. Strongest Genre-Level Signal

The strongest genre in the current YouTube sample was:

- Genre: {top_genre["genre"]}
- Total views: {int(top_genre["total_views"]):,}
- Median views: {int(top_genre["median_views"]):,}
- Total likes: {int(top_genre["total_likes"]):,}
- Total comments: {int(top_genre["total_comments"]):,}

### 4. Top Market Opportunity

The highest-scoring market-content combination was:

- Country: {top_market["country_name"]} ({top_market["country_code"]})
- Genre: {top_market["genre"]}
- Content type: {top_market["content_type"]}
- Lyric style: {top_market["lyric_style"]}
- Query: {top_market["query"]}
- YouTube opportunity score: {top_market["youtube_opportunity_score"]:.4f}

## Interpretation

At this stage, view volume and engagement should be treated as stronger short-term indicators than revenue. Early AI-generated music releases may not immediately generate meaningful payout on major streaming platforms, especially when stream volume is low. Therefore, public engagement metrics such as views, likes, and comments are useful for identifying which markets and content types are worth testing first.

## Next Step

The next step is to complement YouTube public data with TikTok manual sampling, distributor royalty observations, and platform-specific notes for Spotify, YouTube Music, Facebook/Instagram, Luna, Tencent Music, and NetEase Cloud Music.
"""

    report_path = REPORT_DIR / "youtube_public_market_analysis.md"
    report_path.write_text(report, encoding="utf-8")


def main():
    raw, summary = load_youtube_data()
    country_summary, content_type_summary, genre_summary, market_content_summary = build_analysis_tables(raw, summary)

    create_figures(
        country_summary,
        content_type_summary,
        genre_summary,
        market_content_summary,
    )

    write_markdown_report(
        country_summary,
        content_type_summary,
        genre_summary,
        market_content_summary,
    )

    print("Saved analysis outputs:")
    print("data/youtube_country_summary.csv")
    print("data/youtube_content_type_summary.csv")
    print("data/youtube_genre_summary.csv")
    print("data/youtube_market_opportunity_score.csv")
    print("figures/top_youtube_market_opportunities.png")
    print("figures/youtube_views_by_content_type.png")
    print("figures/youtube_views_by_genre.png")
    print("figures/youtube_views_by_country.png")
    print("reports/youtube_public_market_analysis.md")

    print("\nTop 10 YouTube market opportunities:")
    print(
        market_content_summary[
            [
                "country_code",
                "country_name",
                "genre",
                "content_type",
                "lyric_style",
                "query",
                "total_views",
                "median_views",
                "avg_like_rate",
                "avg_comment_rate",
                "youtube_opportunity_score",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
    