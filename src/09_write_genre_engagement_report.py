import pandas as pd
from pathlib import Path

INPUT_FILE = "data/youtube_genre_engagement_summary.csv"
OUTPUT_FILE = "reports/genre_engagement_behavior_analysis_cn.md"

def format_number(x):
    try:
        return f"{int(x):,}"
    except:
        return x

def format_rate(x):
    try:
        return f"{x * 100:.2f}%"
    except:
        return x

def main():
    df = pd.read_csv(INPUT_FILE)

    Path("reports").mkdir(exist_ok=True)

    top_views = df.sort_values("total_views", ascending=False).head(3)
    top_engagement = df.sort_values("avg_engagement_rate", ascending=False).head(3)
    background = df[df["listening_behavior"] == "Background / Looping Consumption"]
    active = df[df["listening_behavior"] == "Active Listening / High Engagement"]

    report = []

    report.append("# Genre Engagement Behavior Analysis\n")
    report.append("## 1. Research Objective\n")
    report.append(
        "本阶段分析重点是继续围绕曲风（genre）展开，但不再只看不同曲风的发布数量，"
        "而是结合播放量、点赞率、评论率和综合互动率，判断不同曲风背后的用户收听行为。\n"
    )

    report.append("核心研究问题是：\n")
    report.append(
        "> 不同 AI music genre 是否表现出不同的消费模式？"
        "哪些曲风更偏向背景循环播放，哪些曲风更偏向用户主动收听？\n"
    )

    report.append("## 2. Data Source\n")
    report.append(
        "本次分析使用 YouTube public video metrics 数据，"
        "并基于 genre 维度进行聚合分析。\n"
    )

    report.append("主要字段包括：\n")
    report.append("- genre\n")
    report.append("- video_count\n")
    report.append("- total_views\n")
    report.append("- median_views\n")
    report.append("- total_likes\n")
    report.append("- total_comments\n")
    report.append("- avg_like_rate\n")
    report.append("- avg_comment_rate\n")
    report.append("- avg_engagement_rate\n")
    report.append("- listening_behavior\n\n")

    report.append("## 3. Key Metrics\n")
    report.append("本次分析使用以下核心指标：\n")
    report.append("- Like Rate = Likes / Views\n")
    report.append("- Comment Rate = Comments / Views\n")
    report.append("- Engagement Rate = (Likes + Comments) / Views\n\n")

    report.append(
        "相比单纯播放量，互动率更能帮助我们判断用户是否真正主动参与。"
        "例如，某类音乐播放量很高但点赞率和评论率较低，可能说明它更偏向咖啡厅、餐厅、学习或 playlist 的背景循环播放。"
        "而播放量不一定最高但互动率高的曲风，可能更接近用户主动收听和情绪反馈。\n"
    )

    report.append("## 4. Genre-Level Summary\n")
    report.append("| Genre | Videos | Total Views | Median Views | Avg Like Rate | Avg Comment Rate | Avg Engagement Rate | Behavior |\n")
    report.append("|---|---:|---:|---:|---:|---:|---:|---|\n")

    for _, row in df.iterrows():
        report.append(
            f"| {row['genre']} "
            f"| {format_number(row['video_count'])} "
            f"| {format_number(row['total_views'])} "
            f"| {format_number(row['median_views'])} "
            f"| {format_rate(row['avg_like_rate'])} "
            f"| {format_rate(row['avg_comment_rate'])} "
            f"| {format_rate(row['avg_engagement_rate'])} "
            f"| {row['listening_behavior']} |\n"
        )

    report.append("\n## 5. Findings\n")

    report.append("### 5.1 Genres with Highest Total Views\n")
    for _, row in top_views.iterrows():
        report.append(
            f"- **{row['genre']}**: total views = {format_number(row['total_views'])}, "
            f"median views = {format_number(row['median_views'])}, "
            f"engagement rate = {format_rate(row['avg_engagement_rate'])}\n"
        )

    report.append("\n### 5.2 Genres with Highest Engagement Rate\n")
    for _, row in top_engagement.iterrows():
        report.append(
            f"- **{row['genre']}**: engagement rate = {format_rate(row['avg_engagement_rate'])}, "
            f"like rate = {format_rate(row['avg_like_rate'])}, "
            f"comment rate = {format_rate(row['avg_comment_rate'])}\n"
        )

    report.append("\n### 5.3 Background / Looping Consumption Genres\n")
    if len(background) > 0:
        for _, row in background.iterrows():
            report.append(
                f"- **{row['genre']}**: 该曲风在当前数据中表现为高播放量但相对较低互动率，"
                "可能更偏向背景播放、playlist 循环或场景型消费。\n"
            )
    else:
        report.append("- 当前数据中没有明显被分类为 Background / Looping Consumption 的曲风。\n")

    report.append("\n### 5.4 Active Listening / High Engagement Genres\n")
    if len(active) > 0:
        for _, row in active.iterrows():
            report.append(
                f"- **{row['genre']}**: 该曲风在当前数据中互动率较高，"
                "可能更接近用户主动收听、情绪反馈或内容参与。\n"
            )
    else:
        report.append("- 当前数据中没有明显被分类为 Active Listening / High Engagement 的曲风。\n")

    report.append("\n## 6. Interpretation\n")
    report.append(
        "从当前结果来看，播放量最高的曲风不一定拥有最高互动率。"
        "这说明播放量和用户喜好不能完全等同。"
        "对于 AI music 市场分析来说，播放量可以反映内容曝光和消费规模，"
        "但点赞率、评论率和综合互动率更能反映用户主动参与程度。\n"
    )

    report.append(
        "因此，后续分析不应只判断某个曲风是否发布量高或播放量高，"
        "而应结合 engagement metrics 来判断该曲风属于背景场景消费，还是主动用户消费。\n"
    )

    report.append("\n## 7. Business Implications\n")
    report.append("- 高播放量、低互动率的曲风适合用于背景音乐、长时长播放、咖啡厅、学习和 playlist 场景。\n")
    report.append("- 高互动率曲风更适合做短视频传播、社交媒体测试、用户情绪型内容和主题化营销。\n")
    report.append("- 如果未来做 A/B test，可以测试同一主题下不同曲风，或同一曲风下不同主题的表现。\n")

    report.append("\n## 8. Next Steps\n")
    report.append("下一步可以继续扩展：\n")
    report.append("1. 增加更多 genre 和国家市场。\n")
    report.append("2. 加入 title / description 的 NLP 文本分类。\n")
    report.append("3. 对比不同国家、语言和主题下的 genre 表现。\n")
    report.append("4. 设计真实 A/B test，测试不同曲风和主题的市场反馈。\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(report)

    print(f"Report generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    