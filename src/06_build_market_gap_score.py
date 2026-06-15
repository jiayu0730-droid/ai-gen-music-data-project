from pathlib import Path

import numpy as np
import pandas as pd


DATA_DIR = Path("data")
REPORT_DIR = Path("reports")

YOUTUBE_FILE = DATA_DIR / "youtube_market_opportunity_score.csv"
ITUNES_FILE = DATA_DIR / "itunes_market_supply_summary.csv"

OUTPUT_FILE = DATA_DIR / "market_gap_opportunity_score.csv"
OUTPUT_REPORT = REPORT_DIR / "market_gap_opportunity_report.md"


def minmax(series):
    series = pd.to_numeric(series, errors="coerce").fillna(0)

    if series.max() == series.min():
        return pd.Series([0.5] * len(series), index=series.index)

    return (series - series.min()) / (series.max() - series.min())


def format_int(x):
    try:
        return f"{int(x):,}"
    except Exception:
        return x


def main():
    REPORT_DIR.mkdir(exist_ok=True)

    if not YOUTUBE_FILE.exists():
        raise FileNotFoundError(f"Missing file: {YOUTUBE_FILE}")

    if not ITUNES_FILE.exists():
        raise FileNotFoundError(f"Missing file: {ITUNES_FILE}")

    youtube = pd.read_csv(YOUTUBE_FILE)
    itunes = pd.read_csv(ITUNES_FILE)

    merge_cols = [
        "country_code",
        "country_name",
        "genre",
        "content_type",
        "lyric_style",
        "language",
        "query",
    ]

    missing_youtube = [col for col in merge_cols if col not in youtube.columns]
    missing_itunes = [col for col in merge_cols if col not in itunes.columns]

    if missing_youtube:
        raise ValueError(f"YouTube file is missing columns: {missing_youtube}")

    if missing_itunes:
        raise ValueError(f"iTunes file is missing columns: {missing_itunes}")

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

    merged["itunes_catalog_count"] = merged["itunes_catalog_count"].fillna(0)
    merged["unique_artists"] = merged["unique_artists"].fillna(0)
    merged["unique_itunes_genres"] = merged["unique_itunes_genres"].fillna(0)

    # Demand side: YouTube
    merged["demand_score"] = merged["youtube_opportunity_score"]

    # Supply side: iTunes catalog count
    # More catalog count = more supply / competition
    merged["supply_score"] = minmax(np.log1p(merged["itunes_catalog_count"]))

    # Gap score: high demand + low supply
    merged["gap_score"] = merged["demand_score"] * (1 - merged["supply_score"])

    # Final score: prioritize demand, but reward lower supply
    merged["final_market_gap_score"] = (
        0.65 * merged["demand_score"]
        + 0.35 * merged["gap_score"]
    )

    merged = merged.sort_values("final_market_gap_score", ascending=False)

    merged.to_csv(OUTPUT_FILE, index=False)

    top10 = merged.head(10).copy()

    display_cols = [
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

    top10_display = top10[display_cols].copy()

    if "total_views" in top10_display.columns:
        top10_display["total_views"] = top10_display["total_views"].apply(format_int)

    for col in [
        "youtube_opportunity_score",
        "supply_score",
        "gap_score",
        "final_market_gap_score",
    ]:
        top10_display[col] = top10_display[col].round(3)

    report_lines = [
        "# Market Gap Opportunity Report",
        "",
        "## Purpose",
        "",
        "This report combines YouTube public-demand signals with iTunes catalog-supply signals.",
        "",
        "The goal is to identify markets where AI-generated music may have strong demand but relatively lower existing catalog supply.",
        "",
        "## Method",
        "",
        "- YouTube opportunity score = demand signal",
        "- iTunes catalog count = supply / competition proxy",
        "- Gap score = high demand + low supply",
        "- Final market gap score = demand score + gap score",
        "",
        "## Top 10 Market Gap Opportunities",
        "",
        top10_display.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "Markets with high YouTube demand and relatively low iTunes catalog supply may be stronger candidates for AI-generated music testing.",
        "",
        "This does not prove the market is completely empty. It gives an automated first-pass signal for potential market gaps.",
        "",
        "## Next Step",
        "",
        "Use the top-ranked markets to design A/B tests across lyrics, language, and genre.",
    ]

    OUTPUT_REPORT.write_text("\n".join(report_lines), encoding="utf-8")

    print("Saved:")
    print(OUTPUT_FILE)
    print(OUTPUT_REPORT)

    print("\nTop 10 market gap opportunities:")
    print(top10_display.to_string(index=False))


if __name__ == "__main__":
    main()
