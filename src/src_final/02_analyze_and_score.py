"""
02_analyze_and_score.py

User-facing stage 2:
- Build YouTube market summaries and opportunity score
- Build iTunes + YouTube market-gap score
- Analyze genre engagement behavior
- Build observational A/B comparison
- Build genre signal score
- Extract themes and build subgenre opportunity score

Run:
    python src/02_analyze_and_score.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


DATA_DIR = Path("data")


def ensure_data_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def minmax(series: pd.Series, constant_value: float = 0.0) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce").fillna(0)
    if series.max() == series.min():
        return pd.Series([constant_value] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())


def safe_divide(a: float, b: float) -> float:
    return a / b if b else 0.0


def build_youtube_market_analysis() -> None:
    raw_path = DATA_DIR / "youtube_public_video_metrics.csv"
    ensure_data_file(raw_path)
    raw = pd.read_csv(raw_path)

    for col in ["view_count", "like_count", "comment_count"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce").fillna(0)

    safe_views = raw["view_count"].replace(0, pd.NA)
    if "like_rate" not in raw.columns:
        raw["like_rate"] = raw["like_count"] / safe_views
    if "comment_rate" not in raw.columns:
        raw["comment_rate"] = raw["comment_count"] / safe_views

    def aggregate(group_cols: list[str]) -> pd.DataFrame:
        return (
            raw.groupby(group_cols)
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

    country = aggregate(["country_code", "country_name"]).sort_values(
        "total_views", ascending=False
    )
    content = aggregate(["content_type"]).sort_values("total_views", ascending=False)
    genre = aggregate(["genre"]).sort_values("total_views", ascending=False)

    market_cols = [
        "country_code",
        "country_name",
        "genre",
        "content_type",
        "lyric_style",
        "language",
        "query",
    ]
    market = aggregate(market_cols)
    market["views_score"] = minmax(np.log1p(market["total_views"]), 0.5)
    market["median_views_score"] = minmax(np.log1p(market["median_views"]), 0.5)
    market["like_rate_score"] = minmax(market["avg_like_rate"], 0.5)
    market["comment_rate_score"] = minmax(market["avg_comment_rate"], 0.5)
    market["youtube_opportunity_score"] = (
        0.50 * market["views_score"]
        + 0.20 * market["median_views_score"]
        + 0.15 * market["like_rate_score"]
        + 0.15 * market["comment_rate_score"]
    )
    market = market.sort_values("youtube_opportunity_score", ascending=False)

    country.to_csv(DATA_DIR / "youtube_country_summary.csv", index=False)
    content.to_csv(DATA_DIR / "youtube_content_type_summary.csv", index=False)
    genre.to_csv(DATA_DIR / "youtube_genre_summary.csv", index=False)
    market.to_csv(DATA_DIR / "youtube_market_opportunity_score.csv", index=False)


def build_market_gap_score() -> None:
    youtube_path = DATA_DIR / "youtube_market_opportunity_score.csv"
    itunes_path = DATA_DIR / "itunes_market_supply_summary.csv"
    ensure_data_file(youtube_path)
    ensure_data_file(itunes_path)

    youtube = pd.read_csv(youtube_path)
    itunes = pd.read_csv(itunes_path)

    merge_cols = [
        "country_code",
        "country_name",
        "genre",
        "content_type",
        "lyric_style",
        "language",
        "query",
    ]

    merged = youtube.merge(
        itunes[
            merge_cols
            + [
                "itunes_catalog_count",
                "unique_artists",
                "unique_itunes_genres",
                "avg_track_price",
            ]
        ],
        on=merge_cols,
        how="left",
    )

    for col in ["itunes_catalog_count", "unique_artists", "unique_itunes_genres"]:
        merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0)

    merged["demand_score"] = merged["youtube_opportunity_score"]
    merged["supply_score"] = minmax(np.log1p(merged["itunes_catalog_count"]), 0.5)
    merged["gap_score"] = merged["demand_score"] * (1 - merged["supply_score"])
    merged["final_market_gap_score"] = (
        0.65 * merged["demand_score"] + 0.35 * merged["gap_score"]
    )

    merged.sort_values("final_market_gap_score", ascending=False).to_csv(
        DATA_DIR / "market_gap_opportunity_score.csv", index=False
    )


def build_genre_engagement_behavior() -> None:
    raw_path = DATA_DIR / "youtube_public_video_metrics.csv"
    ensure_data_file(raw_path)
    df = pd.read_csv(raw_path)

    for col in ["view_count", "like_count", "comment_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["like_rate"] = df.apply(
        lambda row: safe_divide(row["like_count"], row["view_count"]), axis=1
    )
    df["comment_rate"] = df.apply(
        lambda row: safe_divide(row["comment_count"], row["view_count"]), axis=1
    )
    df["engagement_rate"] = df.apply(
        lambda row: safe_divide(
            row["like_count"] + row["comment_count"], row["view_count"]
        ),
        axis=1,
    )

    summary = (
        df.groupby("genre")
        .agg(
            video_count=("video_id", "count"),
            total_views=("view_count", "sum"),
            median_views=("view_count", "median"),
            total_likes=("like_count", "sum"),
            total_comments=("comment_count", "sum"),
            avg_like_rate=("like_rate", "mean"),
            avg_comment_rate=("comment_rate", "mean"),
            avg_engagement_rate=("engagement_rate", "mean"),
        )
        .reset_index()
        .sort_values("total_views", ascending=False)
    )

    high_views = summary["median_views"].quantile(0.75)
    low_engagement = summary["avg_engagement_rate"].quantile(0.25)
    high_engagement = summary["avg_engagement_rate"].quantile(0.75)

    def classify(row: pd.Series) -> str:
        if row["median_views"] >= high_views and row["avg_engagement_rate"] <= low_engagement:
            return "Background / Looping Consumption"
        if row["avg_engagement_rate"] >= high_engagement:
            return "Active Listening / High Engagement"
        return "Mixed / Unclear"

    summary["listening_behavior"] = summary.apply(classify, axis=1)
    summary.to_csv(DATA_DIR / "youtube_genre_engagement_summary.csv", index=False)
    summary.to_csv(DATA_DIR / "youtube_genre_behavior_classification.csv", index=False)


def build_genre_ab_comparison() -> None:
    path = DATA_DIR / "youtube_genre_engagement_summary.csv"
    ensure_data_file(path)
    df = pd.read_csv(path)

    background_genres = ["jazz", "lofi", "bossa nova"]
    active_genres = ["pop", "edm", "city pop"]

    df["ab_group"] = "Other"
    df.loc[df["genre"].isin(background_genres), "ab_group"] = "A_Background_Looping"
    df.loc[df["genre"].isin(active_genres), "ab_group"] = "B_Active_Listening"

    test_df = df[df["ab_group"].isin(["A_Background_Looping", "B_Active_Listening"])]
    if test_df.empty:
        print("Skipping A/B comparison: no matching genres.")
        return

    summary = (
        test_df.groupby("ab_group")
        .agg(
            genre_count=("genre", "count"),
            total_video_count=("video_count", "sum"),
            total_views=("total_views", "sum"),
            median_views=("median_views", "median"),
            total_likes=("total_likes", "sum"),
            total_comments=("total_comments", "sum"),
            avg_like_rate=("avg_like_rate", "mean"),
            avg_comment_rate=("avg_comment_rate", "mean"),
            avg_engagement_rate=("avg_engagement_rate", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(DATA_DIR / "genre_ab_test_results.csv", index=False)


def build_genre_signal_score() -> None:
    path = DATA_DIR / "youtube_genre_engagement_summary.csv"
    ensure_data_file(path)
    df = pd.read_csv(path)

    for col in [
        "video_count",
        "total_views",
        "median_views",
        "total_likes",
        "total_comments",
        "avg_like_rate",
        "avg_comment_rate",
        "avg_engagement_rate",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["view_score"] = minmax(np.log1p(df["total_views"]))
    df["like_score"] = minmax(df["avg_like_rate"])
    df["comment_score"] = minmax(df["avg_comment_rate"])
    df["engagement_score"] = minmax(df["avg_engagement_rate"])

    df["genre_impact_score"] = (
        0.45 * df["view_score"]
        + 0.25 * df["like_score"]
        + 0.20 * df["comment_score"]
        + 0.10 * df["engagement_score"]
    ) * 100

    df["supply_score"] = minmax(np.log1p(df["video_count"])) * 100
    df["opportunity_score"] = df["genre_impact_score"] - df["supply_score"]

    def classify(score: float) -> str:
        if score >= 30:
            return "High Opportunity"
        if score >= 10:
            return "Medium Opportunity"
        return "Low Opportunity"

    df["opportunity_level"] = df["opportunity_score"].apply(classify)
    df.sort_values("opportunity_score", ascending=False).to_csv(
        DATA_DIR / "genre_signal_opportunity_score.csv", index=False
    )


THEME_KEYWORDS = {
    "cafe": ["cafe", "coffee", "coffee shop", "restaurant"],
    "study": ["study", "focus", "work", "deep work", "coding"],
    "sleep": ["sleep", "night", "dream", "bedtime"],
    "rain": ["rain", "rainy", "storm"],
    "summer": ["summer", "beach", "vacation"],
    "nostalgia": ["nostalgia", "nostalgic", "retro", "memory", "memories"],
    "romance": ["love", "romance", "romantic", "heartbreak"],
    "gaming": ["gaming", "game", "cyber", "synthwave"],
    "workout": ["workout", "gym", "fitness", "running"],
    "party": ["party", "festival", "club", "dance"],
    "spiritual": ["devotional", "prayer", "meditation", "worship"],
}


def classify_theme(text: str) -> str:
    text = str(text).lower()
    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return theme
    return "general"


def build_theme_classification() -> None:
    path = DATA_DIR / "youtube_public_video_metrics.csv"
    ensure_data_file(path)
    df = pd.read_csv(path)

    if "genre" not in df.columns:
        raise ValueError("Missing required column: genre")

    title_col = "video_title" if "video_title" in df.columns else "title"
    df["title_text"] = df.get(title_col, "").astype(str)
    df["description_text"] = df.get("description", "").astype(str)
    df["combined_text"] = df["title_text"] + " " + df["description_text"]
    df["theme"] = df["combined_text"].apply(classify_theme)

    def build_subgenre(row: pd.Series) -> str:
        genre = str(row.get("genre", "")).lower().strip() or "unknown"
        theme = str(row.get("theme", "")).lower().strip()
        return genre if not theme or theme == "general" else f"{theme} {genre}"

    df["subgenre"] = df.apply(build_subgenre, axis=1)
    df.to_csv(DATA_DIR / "youtube_theme_classification.csv", index=False)


def build_subgenre_opportunity_score() -> None:
    path = DATA_DIR / "youtube_theme_classification.csv"
    ensure_data_file(path)
    df = pd.read_csv(path)

    for col in ["view_count", "like_count", "comment_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["like_rate"] = df.apply(
        lambda row: safe_divide(row["like_count"], row["view_count"]), axis=1
    )
    df["comment_rate"] = df.apply(
        lambda row: safe_divide(row["comment_count"], row["view_count"]), axis=1
    )
    df["engagement_rate"] = df.apply(
        lambda row: safe_divide(
            row["like_count"] + row["comment_count"], row["view_count"]
        ),
        axis=1,
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

    summary["view_score"] = minmax(np.log1p(summary["total_views"]))
    summary["like_score"] = minmax(summary["avg_like_rate"])
    summary["comment_score"] = minmax(summary["avg_comment_rate"])
    summary["engagement_score"] = minmax(summary["avg_engagement_rate"])

    summary["subgenre_impact_score"] = (
        0.45 * summary["view_score"]
        + 0.25 * summary["like_score"]
        + 0.20 * summary["comment_score"]
        + 0.10 * summary["engagement_score"]
    ) * 100

    summary["supply_score"] = minmax(np.log1p(summary["video_count"])) * 100
    max_count = max(int(summary["video_count"].max()), 1)
    summary["confidence_score"] = np.log1p(summary["video_count"]) / np.log1p(max_count)
    summary["raw_opportunity_score"] = (
        summary["subgenre_impact_score"] - summary["supply_score"]
    )
    summary["market_opportunity_score"] = (
        summary["subgenre_impact_score"]
        * summary["confidence_score"]
        * (1 - summary["supply_score"] / 100)
    )

    def classify(score: float) -> str:
        if score >= 20:
            return "Immediate Production Candidate"
        if score >= 10:
            return "Experimental Candidate"
        return "Low Priority"

    summary["opportunity_level"] = summary["market_opportunity_score"].apply(classify)
    summary.sort_values("market_opportunity_score", ascending=False).to_csv(
        DATA_DIR / "subgenre_opportunity_score.csv", index=False
    )


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    print("1/7 YouTube market analysis")
    build_youtube_market_analysis()

    itunes_path = DATA_DIR / "itunes_market_supply_summary.csv"
    if itunes_path.exists():
        print("2/7 Cross-platform market gap score")
        build_market_gap_score()
    else:
        print("2/7 Skipped market gap score: iTunes supply file not found")

    print("3/7 Genre engagement behavior")
    build_genre_engagement_behavior()

    print("4/7 Observational genre A/B comparison")
    build_genre_ab_comparison()

    print("5/7 Genre signal score")
    build_genre_signal_score()

    print("6/7 Theme classification")
    build_theme_classification()

    print("7/7 Subgenre opportunity score")
    build_subgenre_opportunity_score()

    print("Analysis pipeline completed.")


if __name__ == "__main__":
    main()
