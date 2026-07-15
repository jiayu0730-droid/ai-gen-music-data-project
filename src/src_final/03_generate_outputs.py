"""
03_generate_outputs.py

User-facing stage 3:
- Generate the core figures
- Generate concise Markdown reports
- Keep output focused and remove redundant legacy reports

Run:
    python src/03_generate_outputs.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_DIR = Path("data")
FIGURE_DIR = Path("figures")
REPORT_DIR = Path("reports")


def ensure_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def fmt_int(x) -> str:
    try:
        return f"{int(x):,}"
    except Exception:
        return str(x)


def fmt_float(x, digits: int = 2) -> str:
    try:
        return f"{float(x):.{digits}f}"
    except Exception:
        return str(x)


def fmt_rate(x) -> str:
    try:
        return f"{float(x) * 100:.2f}%"
    except Exception:
        return str(x)


def create_youtube_market_figures() -> None:
    market_path = DATA_DIR / "youtube_market_opportunity_score.csv"
    country_path = DATA_DIR / "youtube_country_summary.csv"
    content_path = DATA_DIR / "youtube_content_type_summary.csv"
    genre_path = DATA_DIR / "youtube_genre_summary.csv"

    for path in [market_path, country_path, content_path, genre_path]:
        ensure_file(path)

    market = pd.read_csv(market_path)
    country = pd.read_csv(country_path)
    content = pd.read_csv(content_path)
    genre = pd.read_csv(genre_path)

    top = market.head(10).copy()
    top["label"] = (
        top["country_code"].astype(str)
        + " | "
        + top["genre"].astype(str)
        + " | "
        + top["content_type"].astype(str)
    )

    plt.figure(figsize=(12, 7))
    plt.barh(top["label"], top["youtube_opportunity_score"])
    plt.gca().invert_yaxis()
    plt.xlabel("YouTube Opportunity Score")
    plt.ylabel("Market / Genre / Content Type")
    plt.title("Top YouTube Market Opportunities")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "top_youtube_market_opportunities.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(country["country_code"], country["total_views"])
    plt.xlabel("Country")
    plt.ylabel("Total Views")
    plt.title("YouTube Views by Country")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "youtube_views_by_country.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.bar(content["content_type"], content["total_views"])
    plt.xlabel("Content Type")
    plt.ylabel("Total Views")
    plt.title("YouTube Views by Content Type")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "youtube_views_by_content_type.png", dpi=300)
    plt.close()

    plt.figure(figsize=(9, 6))
    plt.bar(genre["genre"], genre["total_views"])
    plt.xlabel("Genre")
    plt.ylabel("Total Views")
    plt.title("YouTube Views by Genre")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "youtube_views_by_genre.png", dpi=300)
    plt.close()


def create_genre_signal_figures() -> None:
    path = DATA_DIR / "genre_signal_opportunity_score.csv"
    ensure_file(path)
    df = pd.read_csv(path)

    opportunity = df.sort_values("opportunity_score")
    plt.figure(figsize=(10, 6))
    plt.barh(opportunity["genre"], opportunity["opportunity_score"])
    plt.xlabel("Opportunity Score")
    plt.ylabel("Genre")
    plt.title("Genre Opportunity Score")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "genre_opportunity_score.png", dpi=300)
    plt.close()

    impact = df.sort_values("genre_impact_score")
    plt.figure(figsize=(10, 6))
    plt.barh(impact["genre"], impact["genre_impact_score"])
    plt.xlabel("Genre Impact Score")
    plt.ylabel("Genre")
    plt.title("Genre Impact Score")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "genre_impact_score.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.scatter(df["supply_score"], df["genre_impact_score"])
    for _, row in df.iterrows():
        plt.text(row["supply_score"], row["genre_impact_score"], row["genre"], fontsize=8)
    plt.xlabel("Supply Score")
    plt.ylabel("Genre Impact Score")
    plt.title("Demand vs Supply by Genre")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "genre_demand_vs_supply.png", dpi=300)
    plt.close()


def create_subgenre_figures() -> None:
    path = DATA_DIR / "subgenre_opportunity_score.csv"
    ensure_file(path)
    df = pd.read_csv(path)

    top = df.sort_values("market_opportunity_score", ascending=False).head(15)

    top_bar = top.sort_values("market_opportunity_score")
    plt.figure(figsize=(10, 7))
    plt.barh(top_bar["subgenre"], top_bar["market_opportunity_score"])
    plt.xlabel("Market Opportunity Score")
    plt.ylabel("Subgenre")
    plt.title("Top Subgenre Market Opportunity Scores")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "top_subgenre_market_opportunity_score.png", dpi=300)
    plt.close()

    plt.figure(figsize=(9, 7))
    plt.scatter(df["supply_score"], df["subgenre_impact_score"])
    for _, row in top.iterrows():
        plt.text(
            row["supply_score"],
            row["subgenre_impact_score"],
            row["subgenre"],
            fontsize=8,
        )
    plt.xlabel("Supply / Competition Score")
    plt.ylabel("Subgenre Impact Score")
    plt.title("Subgenre Demand vs Supply")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "subgenre_demand_vs_supply.png", dpi=300)
    plt.close()

    theme = (
        df.groupby("theme")
        .agg(avg_market_opportunity_score=("market_opportunity_score", "mean"))
        .reset_index()
        .sort_values("avg_market_opportunity_score")
    )
    plt.figure(figsize=(10, 6))
    plt.barh(theme["theme"], theme["avg_market_opportunity_score"])
    plt.xlabel("Average Market Opportunity Score")
    plt.ylabel("Theme")
    plt.title("Average Market Opportunity Score by Theme")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "theme_market_opportunity_score.png", dpi=300)
    plt.close()

    confidence = top.sort_values("confidence_score")
    plt.figure(figsize=(10, 7))
    plt.barh(confidence["subgenre"], confidence["confidence_score"])
    plt.xlabel("Confidence Score")
    plt.ylabel("Subgenre")
    plt.title("Confidence Score of Top Subgenre Candidates")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "subgenre_confidence_score.png", dpi=300)
    plt.close()


def write_youtube_market_report() -> None:
    market_path = DATA_DIR / "youtube_market_opportunity_score.csv"
    ensure_file(market_path)
    df = pd.read_csv(market_path).sort_values("youtube_opportunity_score", ascending=False)
    top = df.head(10).copy()

    display_cols = [
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
    table = top[display_cols].copy()
    table["total_views"] = table["total_views"].apply(fmt_int)
    table["median_views"] = table["median_views"].apply(fmt_int)
    table["avg_like_rate"] = table["avg_like_rate"].apply(fmt_rate)
    table["avg_comment_rate"] = table["avg_comment_rate"].apply(fmt_rate)
    table["youtube_opportunity_score"] = table["youtube_opportunity_score"].apply(
        lambda x: fmt_float(x, 3)
    )

    report = f"""# YouTube-Based Market Opportunity Report

## Scope

This report uses public YouTube demand and engagement signals. It should not be interpreted as a full cross-platform revenue model.

## Top 10 Opportunities

{table.to_markdown(index=False)}

## Interpretation

YouTube currently provides the strongest public signals in this project: views, likes, comments, country, genre, content type, and query-level performance.

The results are best used to prioritize markets and concepts for controlled content tests.

## Limitations

- Search results are observational rather than causal.
- High views may reflect existing superstar content.
- Revenue and user-level streaming behavior are not included.
- Cross-platform integration requires Spotify, TikTok, distributor, or dashboard data.

![Top YouTube Market Opportunities](../figures/top_youtube_market_opportunities.png)
"""
    (REPORT_DIR / "youtube_market_report.md").write_text(report, encoding="utf-8")


def write_market_gap_report() -> None:
    path = DATA_DIR / "market_gap_opportunity_score.csv"
    if not path.exists():
        return

    df = pd.read_csv(path).sort_values("final_market_gap_score", ascending=False)
    cols = [
        "country_code",
        "country_name",
        "genre",
        "content_type",
        "lyric_style",
        "query",
        "total_views",
        "youtube_opportunity_score",
        "itunes_catalog_count",
        "supply_score",
        "gap_score",
        "final_market_gap_score",
    ]
    top = df.head(10)[cols].copy()
    top["total_views"] = top["total_views"].apply(fmt_int)

    report = f"""# Cross-Platform Market Gap Report

## Scope

This report combines:

- YouTube public-demand signals
- iTunes catalog-supply signals

## Top 10 Market Gaps

{top.to_markdown(index=False)}

## Interpretation

A high rank means strong YouTube demand combined with relatively lower iTunes catalog supply. This is an initial screening signal, not proof of an empty market.

## Next Step

Use the top-ranked combinations for controlled AI music A/B tests across language, theme, genre, and market.
"""
    (REPORT_DIR / "market_gap_opportunity_report.md").write_text(
        report, encoding="utf-8"
    )


def write_genre_report() -> None:
    path = DATA_DIR / "genre_signal_opportunity_score.csv"
    ensure_file(path)
    df = pd.read_csv(path).sort_values("opportunity_score", ascending=False)

    cols = [
        "genre",
        "video_count",
        "total_views",
        "avg_engagement_rate",
        "genre_impact_score",
        "supply_score",
        "opportunity_score",
        "opportunity_level",
    ]
    table = df[cols].copy()
    table["total_views"] = table["total_views"].apply(fmt_int)
    table["avg_engagement_rate"] = table["avg_engagement_rate"].apply(fmt_rate)

    report = f"""# Genre Signal and Opportunity Report

## Method

- Impact score combines views, like rate, comment rate, and engagement rate.
- Supply score uses YouTube video count as a competition proxy.
- Opportunity score = impact score - supply score.

## Results

{table.to_markdown(index=False)}

## Important Caveat

This is still a YouTube-based genre model. The supply estimate should later be expanded with iTunes catalog count, Spotify track count, TikTok content count, and release-window information.

![Genre Opportunity Score](../figures/genre_opportunity_score.png)

![Demand vs Supply](../figures/genre_demand_vs_supply.png)
"""
    (REPORT_DIR / "genre_signal_report.md").write_text(report, encoding="utf-8")


def write_subgenre_report() -> None:
    path = DATA_DIR / "subgenre_opportunity_score.csv"
    ensure_file(path)
    df = pd.read_csv(path).sort_values("market_opportunity_score", ascending=False)

    cols = [
        "genre",
        "theme",
        "subgenre",
        "video_count",
        "total_views",
        "avg_engagement_rate",
        "subgenre_impact_score",
        "supply_score",
        "confidence_score",
        "market_opportunity_score",
        "opportunity_level",
    ]
    top = df.head(15)[cols].copy()
    top["total_views"] = top["total_views"].apply(fmt_int)
    top["avg_engagement_rate"] = top["avg_engagement_rate"].apply(fmt_rate)

    experimental = df[
        (df["market_opportunity_score"] >= 10) & (df["confidence_score"] < 0.7)
    ].head(10)

    bullets = "\n".join(
        f"- **{row['subgenre']}**: opportunity={fmt_float(row['market_opportunity_score'])}, "
        f"confidence={fmt_float(row['confidence_score'])}, videos={fmt_int(row['video_count'])}"
        for _, row in experimental.iterrows()
    ) or "- No experimental candidates under the current thresholds."

    report = f"""# YouTube-Based Subgenre Opportunity Report

## Scope

This report extracts themes from YouTube titles and descriptions, combines them with genre, and ranks subgenre opportunities.

## Top Candidates

{top.to_markdown(index=False)}

## Experimental Candidates

{bullets}

## Scoring Logic

Market Opportunity Score = Impact Score × Confidence Score × (1 - Supply Score / 100)

## Limitations

- Theme classification is keyword-based.
- Demand and supply are primarily based on YouTube public data.
- Controlled release experiments are still required before production decisions.

![Top Subgenre Market Opportunity Score](../figures/top_subgenre_market_opportunity_score.png)

![Subgenre Demand vs Supply](../figures/subgenre_demand_vs_supply.png)

![Theme Market Opportunity Score](../figures/theme_market_opportunity_score.png)

![Subgenre Confidence Score](../figures/subgenre_confidence_score.png)
"""
    (REPORT_DIR / "subgenre_opportunity_report.md").write_text(
        report, encoding="utf-8"
    )


def main() -> None:
    FIGURE_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    create_youtube_market_figures()
    create_genre_signal_figures()
    create_subgenre_figures()

    write_youtube_market_report()
    write_market_gap_report()
    write_genre_report()
    write_subgenre_report()

    print("Figures and reports generated.")


if __name__ == "__main__":
    main()
