import pandas as pd
from pathlib import Path

INPUT_FILE = "data/genre_signal_opportunity_score.csv"
OUTPUT_FILE = "reports/genre_signal_opportunity_report_cn.md"


def format_number(x):
    try:
        return f"{int(x):,}"
    except Exception:
        return x


def format_score(x):
    try:
        return f"{x:.2f}"
    except Exception:
        return x


def format_rate(x):
    try:
        return f"{x * 100:.2f}%"
    except Exception:
        return x


def main():
    df = pd.read_csv(INPUT_FILE)

    Path("reports").mkdir(exist_ok=True)

    top_impact = df.sort_values("genre_impact_score", ascending=False).head(5)
    top_opportunity = df.sort_values("opportunity_score", ascending=False).head(5)
    low_supply_high_impact = df[
        (df["genre_impact_score"] >= df["genre_impact_score"].median())
        & (df["supply_score"] <= df["supply_score"].median())
    ].sort_values("opportunity_score", ascending=False)

    report = []

    report.append("# Genre Signal Score & Opportunity Analysis\n\n")

    report.append("## 1. Research Goal\n\n")
    report.append(
        "本阶段分析是在上一阶段 Genre Engagement Analysis 和 A/B Comparison 的基础上继续推进。"
        "之前我们主要比较不同曲风的播放量、点赞率、评论率和互动率；本阶段进一步将这些分散指标整合成一到两个可解释的 signal metrics，"
        "用于衡量每个曲风的综合影响力和未来 AI 音乐生成机会。\n\n"
    )

    report.append("核心问题是：\n\n")
    report.append(
        "> 哪些曲风不仅有较高市场需求，同时供给相对不足，可以作为未来 AI-generated music 的优先生成方向？\n\n"
    )

    report.append("## 2. Methodology\n\n")

    report.append("### 2.1 Genre Impact Score\n\n")
    report.append(
        "Genre Impact Score 用于衡量一个曲风发布后的综合市场影响力。"
        "该分数综合考虑播放规模、点赞率、评论率和综合互动率。\n\n"
    )

    report.append("当前第一版权重设计如下：\n\n")
    report.append("- View Score: 45%\n")
    report.append("- Like Rate Score: 25%\n")
    report.append("- Comment Rate Score: 20%\n")
    report.append("- Engagement Rate Score: 10%\n\n")

    report.append(
        "其中，播放量权重最高，因为流媒体平台的曝光规模和潜在收益通常与播放量最直接相关。"
        "点赞率和评论率用于衡量用户偏好和主动互动。"
        "综合互动率作为辅助验证指标，但由于它本身已经由点赞和评论构成，因此权重较低，以避免重复计算。\n\n"
    )

    report.append("### 2.2 Supply Score\n\n")
    report.append(
        "Supply Score 用 video_count 作为供给量的近似指标。"
        "一个曲风下已有视频数量越多，说明该曲风当前市场供给越高，竞争也可能越激烈。\n\n"
    )

    report.append("### 2.3 Opportunity Score\n\n")
    report.append(
        "Opportunity Score 用于衡量曲风的供需不平衡机会：\n\n"
    )
    report.append(
        "> Opportunity Score = Genre Impact Score - Supply Score\n\n"
    )
    report.append(
        "如果一个曲风的 Impact Score 较高，但 Supply Score 较低，说明它可能存在需求较高但供给不足的机会，"
        "更适合作为未来 AI 音乐生成和发布的优先方向。\n\n"
    )

    report.append("## 3. Genre Score Summary\n\n")
    report.append(
        "| Genre | Videos | Total Views | Avg Engagement Rate | Impact Score | Supply Score | Opportunity Score | Opportunity Level |\n"
    )
    report.append("|---|---:|---:|---:|---:|---:|---:|---|\n")

    for _, row in df.iterrows():
        report.append(
            f"| {row['genre']} "
            f"| {format_number(row['video_count'])} "
            f"| {format_number(row['total_views'])} "
            f"| {format_rate(row['avg_engagement_rate'])} "
            f"| {format_score(row['genre_impact_score'])} "
            f"| {format_score(row['supply_score'])} "
            f"| {format_score(row['opportunity_score'])} "
            f"| {row['opportunity_level']} |\n"
        )

    report.append("\n## 4. Key Findings\n\n")

    report.append("### 4.1 Genres with Highest Impact Score\n\n")
    report.append(
        "这些曲风代表当前 YouTube 数据中综合影响力较强的类别，即播放规模和互动表现相对更好。\n\n"
    )

    for _, row in top_impact.iterrows():
        report.append(
            f"- **{row['genre']}**: Impact Score = {format_score(row['genre_impact_score'])}, "
            f"Total Views = {format_number(row['total_views'])}, "
            f"Avg Engagement Rate = {format_rate(row['avg_engagement_rate'])}\n"
        )

    report.append("\n### 4.2 Genres with Highest Opportunity Score\n\n")
    report.append(
        "这些曲风在综合影响力和供给水平之间存在更明显的机会空间，可能更适合未来 AI-generated music 的优先生成。\n\n"
    )

    for _, row in top_opportunity.iterrows():
        report.append(
            f"- **{row['genre']}**: Opportunity Score = {format_score(row['opportunity_score'])}, "
            f"Impact Score = {format_score(row['genre_impact_score'])}, "
            f"Supply Score = {format_score(row['supply_score'])}\n"
        )

    report.append("\n### 4.3 Potential Low-Supply / High-Impact Genres\n\n")

    if len(low_supply_high_impact) > 0:
        report.append(
            "以下曲风在当前数据中表现出相对较高影响力和相对较低供给，值得进一步观察：\n\n"
        )
        for _, row in low_supply_high_impact.iterrows():
            report.append(
                f"- **{row['genre']}**: Impact Score = {format_score(row['genre_impact_score'])}, "
                f"Supply Score = {format_score(row['supply_score'])}, "
                f"Opportunity Score = {format_score(row['opportunity_score'])}\n"
            )
    else:
        report.append(
            "当前样本中尚未出现非常明显的低供给、高影响力曲风，后续需要扩大样本和细分曲风。\n"
        )

    report.append("\n## 5. Interpretation\n\n")
    report.append(
        "本阶段结果说明，曲风选择不能只看播放量最高的类别。"
        "例如，某些主流曲风可能拥有非常高的播放规模，但同时供给也很高，市场竞争激烈；"
        "而某些较细分曲风虽然播放规模没有最大，但如果互动表现较好且供给相对不足，反而可能具有更高的生成机会。\n\n"
    )

    report.append(
        "因此，Genre Impact Score 更适合回答“哪个曲风影响力大”，"
        "而 Opportunity Score 更适合回答“哪个曲风值得优先生成”。"
        "这使分析从单纯描述数据，进一步转向可用于内容生产决策的 scoring system。\n\n"
    )

    report.append("## 6. Current Limitations\n\n")
    report.append(
        "当前分数仍然是第一版 heuristic scoring framework。"
        "权重设计基于业务逻辑，而不是最终模型参数。"
        "后续如果能够获得真实收入、完播率、分享量、收藏量或真实 A/B test 数据，可以进一步用回归、排序模型或优化方法校准权重。\n\n"
    )

    report.append(
        "此外，Supply Score 目前使用 video_count 作为供给代理变量。"
        "未来可以进一步结合 iTunes catalog count、Spotify track count、平台发布数量或地区维度供应量，形成更稳健的供给指标。\n\n"
    )

    report.append("## 7. Next Steps\n\n")
    report.append("1. 继续细分曲风，例如 Jazz → Cafe Jazz / Study Jazz / Smooth Jazz。\n")
    report.append("2. 加入 Theme 维度，例如 Study、Sleep、Romance、Food、Hometown。\n")
    report.append("3. 构建 Genre × Theme × Market 的机会矩阵。\n")
    report.append("4. 后续基于 Suno 生成歌曲，设计真实 A/B test 来验证评分结果。\n\n")

    report.append("## 8. Related Figures\n\n")
    report.append("![Genre Opportunity Score](../figures/genre_opportunity_score.png)\n\n")
    report.append("![Genre Impact Score](../figures/genre_impact_score.png)\n\n")
    report.append("![Demand vs Supply](../figures/genre_demand_vs_supply.png)\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(report)

    print(f"Report generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()