import pandas as pd
from pathlib import Path

INPUT_FILE = "data/youtube_genre_engagement_summary.csv"

OUTPUT_FILE = "data/genre_ab_test_results.csv"
REPORT_FILE = "reports/genre_ab_test_results_cn.md"

BACKGROUND_GENRES = ["jazz", "lofi", "bossa nova"]
ACTIVE_GENRES = ["pop", "edm", "city pop"]


def format_number(x):
    try:
        return f"{int(x):,}"
    except Exception:
        return x


def format_rate(x):
    try:
        return f"{x * 100:.2f}%"
    except Exception:
        return x


def main():
    df = pd.read_csv(INPUT_FILE)

    df["ab_group"] = "Other"

    df.loc[df["genre"].isin(BACKGROUND_GENRES), "ab_group"] = "A_Background_Looping"
    df.loc[df["genre"].isin(ACTIVE_GENRES), "ab_group"] = "B_Active_Listening"

    ab_df = df[df["ab_group"].isin(["A_Background_Looping", "B_Active_Listening"])].copy()

    if ab_df.empty:
        raise ValueError("No matching genres found for A/B test groups.")

    ab_summary = (
        ab_df.groupby("ab_group")
        .agg(
            genre_count=("genre", "count"),
            total_video_count=("video_count", "sum"),
            total_views=("total_views", "sum"),
            median_views=("median_views", "median"),
            total_likes=("total_likes", "sum"),
            total_comments=("total_comments", "sum"),
            avg_like_rate=("avg_like_rate", "mean"),
            avg_comment_rate=("avg_comment_rate", "mean"),
            avg_engagement_rate=("avg_engagement_rate", "mean")
        )
        .reset_index()
    )

    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    ab_summary.to_csv(OUTPUT_FILE, index=False)

    a = ab_summary[ab_summary["ab_group"] == "A_Background_Looping"].iloc[0]
    b = ab_summary[ab_summary["ab_group"] == "B_Active_Listening"].iloc[0]

    report = []

    report.append("# Genre A/B Test: Background Looping vs Active Listening\n\n")

    report.append("## 1. Research Question\n\n")
    report.append(
        "本次 A/B test 的目标是验证：不同曲风是否呈现不同的收听行为。"
        "具体来说，我们想比较背景循环播放型音乐和主动收听型音乐在播放量、点赞率、评论率和综合互动率上的差异。\n\n"
    )

    report.append("## 2. A/B Group Design\n\n")
    report.append("### Group A: Background / Looping Music\n\n")
    report.append("包含曲风：jazz, lofi, bossa nova\n\n")
    report.append(
        "这类音乐通常可能用于咖啡厅、餐厅、学习、放松或 playlist 循环播放场景。"
        "理论假设是：播放量可能较高，但点赞率和评论率可能相对较低。\n\n"
    )

    report.append("### Group B: Active Listening / Entertainment Music\n\n")
    report.append("包含曲风：pop, edm, city pop\n\n")
    report.append(
        "这类音乐更可能被用户主动点击、收听和互动。"
        "理论假设是：播放量不一定最高，但点赞率、评论率或综合互动率可能更高。\n\n"
    )

    report.append("## 3. Metrics\n\n")
    report.append("- Total Views\n")
    report.append("- Median Views\n")
    report.append("- Like Rate = Likes / Views\n")
    report.append("- Comment Rate = Comments / Views\n")
    report.append("- Engagement Rate = (Likes + Comments) / Views\n\n")

    report.append("## 4. A/B Test Results\n\n")
    report.append("| Group | Genres | Total Videos | Total Views | Median Views | Avg Like Rate | Avg Comment Rate | Avg Engagement Rate |\n")
    report.append("|---|---|---:|---:|---:|---:|---:|---:|\n")

    for _, row in ab_summary.iterrows():
        genres = ", ".join(ab_df[ab_df["ab_group"] == row["ab_group"]]["genre"].tolist())
        report.append(
            f"| {row['ab_group']} "
            f"| {genres} "
            f"| {format_number(row['total_video_count'])} "
            f"| {format_number(row['total_views'])} "
            f"| {format_number(row['median_views'])} "
            f"| {format_rate(row['avg_like_rate'])} "
            f"| {format_rate(row['avg_comment_rate'])} "
            f"| {format_rate(row['avg_engagement_rate'])} |\n"
        )

    report.append("\n## 5. Interpretation\n\n")

    report.append(
        f"Group A 的总播放量为 {format_number(a['total_views'])}，"
        f"平均互动率为 {format_rate(a['avg_engagement_rate'])}。\n\n"
    )

    report.append(
        f"Group B 的总播放量为 {format_number(b['total_views'])}，"
        f"平均互动率为 {format_rate(b['avg_engagement_rate'])}。\n\n"
    )

    if a["total_views"] > b["total_views"] and a["avg_engagement_rate"] < b["avg_engagement_rate"]:
        report.append(
            "结果支持初始假设：背景循环播放型音乐整体播放量更高，但互动率更低，"
            "说明这类音乐可能更偏向场景型播放或 playlist 循环使用。\n\n"
        )
    elif b["avg_engagement_rate"] > a["avg_engagement_rate"]:
        report.append(
            "结果部分支持初始假设：主动收听型音乐的互动率更高，"
            "说明用户对这类内容可能有更强的主动反馈和情绪参与。\n\n"
        )
    else:
        report.append(
            "当前结果没有完全支持初始假设，说明还需要扩大样本量、细分曲风和加入更多控制变量。\n\n"
        )

    report.append("## 6. Limitations\n\n")
    report.append(
        "本次分析是基于公开 YouTube 数据的 observational A/B comparison，"
        "并不是严格意义上的真实线上 A/B test。真实 A/B test 需要控制发布时间、封面、标题、推广量、国家市场和歌曲长度等变量。\n\n"
    )

    report.append("此外，YouTube public API 当前可以获取 views、likes 和 comments，但不能稳定获取 saves / 收藏量。因此第一版分析使用播放量、点赞率、评论率和综合互动率作为核心指标。\n\n")

    report.append("## 7. Next Step: Real A/B Test Design\n\n")
    report.append("下一步可以用 Suno 生成多组歌曲，并进行真实 A/B test：\n\n")
    report.append("### Test 1: Same Theme, Different Genre\n\n")
    report.append("| Version | Theme | Genre |\n")
    report.append("|---|---|---|\n")
    report.append("| A | Study / Cafe | Jazz |\n")
    report.append("| B | Study / Cafe | Lofi |\n")
    report.append("| C | Study / Cafe | Bossa Nova |\n\n")

    report.append("### Test 2: Same Genre, Different Theme\n\n")
    report.append("| Version | Genre | Theme |\n")
    report.append("|---|---|---|\n")
    report.append("| A | Pop | Romance |\n")
    report.append("| B | Pop | Hometown |\n")
    report.append("| C | Pop | Food / Novelty |\n\n")

    report.append("真实实验中需要尽量控制：title format、cover style、publish time、song length、language、target country 和 promotion level。\n")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.writelines(report)

    print("\nA/B Summary:")
    print(ab_summary)

    print(f"\nSaved A/B result data to {OUTPUT_FILE}")
    print(f"Saved A/B report to {REPORT_FILE}")


if __name__ == "__main__":
    main()
    