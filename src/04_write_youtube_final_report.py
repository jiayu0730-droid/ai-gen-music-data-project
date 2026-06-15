from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
REPORT_DIR = Path("reports")
FIGURE_DIR = Path("figures")

OPPORTUNITY_FILE = DATA_DIR / "youtube_market_opportunity_score.csv"
COUNTRY_FILE = DATA_DIR / "youtube_country_summary.csv"
CONTENT_FILE = DATA_DIR / "youtube_content_type_summary.csv"
GENRE_FILE = DATA_DIR / "youtube_genre_summary.csv"

OUTPUT_REPORT = REPORT_DIR / "youtube_final_market_report.md"


def format_int(x):
    try:
        return f"{int(x):,}"
    except Exception:
        return x


def format_float(x, digits=4):
    try:
        return f"{float(x):.{digits}f}"
    except Exception:
        return x


def df_to_markdown_table(df):
    return df.to_markdown(index=False)


def main():
    REPORT_DIR.mkdir(exist_ok=True)

    opportunity = pd.read_csv(OPPORTUNITY_FILE)
    country = pd.read_csv(COUNTRY_FILE)
    content = pd.read_csv(CONTENT_FILE)
    genre = pd.read_csv(GENRE_FILE)

    top10 = opportunity.head(10).copy()

    top10_display = top10[
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
    ].copy()

    top10_display["total_views"] = top10_display["total_views"].apply(format_int)
    top10_display["median_views"] = top10_display["median_views"].apply(format_int)
    top10_display["avg_like_rate"] = top10_display["avg_like_rate"].apply(lambda x: format_float(x, 4))
    top10_display["avg_comment_rate"] = top10_display["avg_comment_rate"].apply(lambda x: format_float(x, 4))
    top10_display["youtube_opportunity_score"] = top10_display["youtube_opportunity_score"].apply(lambda x: format_float(x, 3))

    country_display = country.copy()
    for col in ["total_views", "median_views", "total_likes", "total_comments"]:
        if col in country_display.columns:
            country_display[col] = country_display[col].apply(format_int)

    content_display = content.copy()
    for col in ["total_views", "median_views", "total_likes", "total_comments"]:
        if col in content_display.columns:
            content_display[col] = content_display[col].apply(format_int)

    genre_display = genre.copy()
    for col in ["total_views", "median_views", "total_likes", "total_comments"]:
        if col in genre_display.columns:
            genre_display[col] = genre_display[col].apply(format_int)

    top_market = opportunity.iloc[0]
    top_country = country.iloc[0]
    top_content = content.iloc[0]
    top_genre = genre.iloc[0]

    report = f"""# YouTube Public Market Analysis for AI-Generated Music

## 1. Purpose

This report uses public YouTube video metrics to evaluate early audience-demand signals for AI-generated music across countries, genres, and content formats.

The current goal is not to estimate exact streaming revenue. Instead, the goal is to identify which markets and content types may be more promising for early-stage release testing.

## 2. Data Source

The dataset was collected through the YouTube Data API using a predefined search matrix of country, genre, content type, lyric style, language, and query.

The main metrics include:

- video count
- total views
- median views
- total likes
- total comments
- average like rate
- average comment rate
- YouTube opportunity score

The opportunity score gives the highest weight to view volume, followed by median views and engagement rates. This matches the current business priority: audience discovery and market validation first, revenue optimization later.

## 3. Top YouTube Market Opportunities

The strongest market-content combination in the current sample is:

- Country: {top_market["country_name"]} ({top_market["country_code"]})
- Genre: {top_market["genre"]}
- Content type: {top_market["content_type"]}
- Lyric style: {top_market["lyric_style"]}
- Query: {top_market["query"]}
- YouTube opportunity score: {top_market["youtube_opportunity_score"]:.3f}

### Top 10 Market Opportunities

{df_to_markdown_table(top10_display)}

![Top YouTube Market Opportunities](../figures/top_youtube_market_opportunities.png)

## 4. Country-Level Findings

The strongest country-level signal in the current sample is:

- Country: {top_country["country_name"]} ({top_country["country_code"]})
- Total views: {int(top_country["total_views"]):,}
- Median views: {int(top_country["median_views"]):,}

### Country Summary

{df_to_markdown_table(country_display)}

![YouTube Views by Country](../figures/youtube_views_by_country.png)

## 5. Content-Type Findings: Instrumental vs. Lyrical

The stronger content type in the current YouTube sample is:

- Content type: {top_content["content_type"]}
- Total views: {int(top_content["total_views"]):,}
- Median views: {int(top_content["median_views"]):,}

### Content Type Summary

{df_to_markdown_table(content_display)}

![YouTube Views by Content Type](../figures/youtube_views_by_content_type.png)

### Interpretation

The current sample suggests that lyrical content has much higher total YouTube visibility than instrumental content. However, this should not be interpreted as a final causal conclusion that lyrics always outperform instrumental music.

A key limitation is that the current lyrical queries are mostly pop and local-language pop, while the instrumental queries are mostly jazz and lofi. Therefore, the result reflects both content-type effects and genre effects. A cleaner A/B test should compare the same genre with and without lyrics, such as jazz instrumental versus jazz vocal, or lofi instrumental versus lofi with vocals.

## 6. Genre-Level Findings

The strongest genre-level signal in the current sample is:

- Genre: {top_genre["genre"]}
- Total views: {int(top_genre["total_views"]):,}
- Median views: {int(top_genre["median_views"]):,}

### Genre Summary

{df_to_markdown_table(genre_display)}

![YouTube Views by Genre](../figures/youtube_views_by_genre.png)

### Interpretation

Pop dominates the current YouTube public-search sample, especially in local-language markets such as Brazil, Mexico, India, and Indonesia. Jazz and lofi show lower total view volume, but they may still be useful for niche positioning, background listening, study, work, café, and relaxation contexts.

## 7. Implications for AI-Generated Music Release Strategy

Based on the current YouTube sample, the strongest short-term direction is to prioritize local-language lyrical pop in high-volume markets such as Mexico, Brazil, India, and Indonesia.

For niche testing, Japanese jazz instrumental and Brazilian jazz instrumental are still worth testing because jazz may represent a smaller but more differentiated market. These tracks may not maximize immediate volume, but they may help identify underserved audience segments.

## 8. Business Interpretation

At the current stage, view volume is more important than direct monetization. Early AI-generated music releases may not generate meaningful payout on major streaming platforms if the stream volume is low. Therefore, the first release strategy should optimize for discovery, reach, and engagement.

Revenue should be treated as a secondary validation metric and should be added later through distributor reports, YouTube Studio / YouTube Analytics, TikTok performance data, Facebook/Instagram reporting, and Chinese platform dashboards such as Tencent Music and NetEase Cloud Music.

## 9. Limitations

Several limitations should be noted:

1. YouTube search results are not a controlled experiment. They reflect public visibility, existing popularity, and YouTube ranking behavior.
2. The dataset captures public YouTube video metrics, not exact YouTube Music streaming revenue.
3. Lyrical and instrumental categories are not perfectly balanced by genre.
4. High total views may reflect existing superstar content rather than an easy market entry opportunity.
5. TikTok, Spotify, Facebook, Luna, Tencent Music, and NetEase Cloud Music still require manual sampling or distributor dashboard data.

## 10. Next Steps

The next step is to add TikTok manual sampling and platform revenue observations.

Recommended next datasets:

- TikTok manual observations: views, likes, comments, shares, search query, country/language signal
- Spotify / DistroKid observations: streams, revenue, platform payout notes
- YouTube Music / YouTube Analytics: country-level revenue where available
- Tencent Music and NetEase Cloud Music: plays, comments, favorites, revenue per play
- Facebook/Instagram and Luna: distributor-level plays and revenue

The next analytical step is to combine public engagement data and manual revenue observations into a platform-market recommendation table.
"""

    OUTPUT_REPORT.write_text(report, encoding="utf-8")

    print(f"Saved final report: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
    