import pandas as pd
from pathlib import Path

INPUT_FILE = "data/subgenre_opportunity_score.csv"
OUTPUT_FILE = "reports/subgenre_recommendation_report_cn.md"


def format_number(x):
    try:
        return f"{int(x):,}"
    except Exception:
        return x


def format_score(x):
    try:
        return f"{float(x):.2f}"
    except Exception:
        return x


def format_rate(x):
    try:
        return f"{float(x) * 100:.2f}%"
    except Exception:
        return x


def main():
    df = pd.read_csv(INPUT_FILE)

    Path("reports").mkdir(exist_ok=True)

    required_cols = [
        "genre", "theme", "subgenre", "video_count", "total_views",
        "avg_engagement_rate", "subgenre_impact_score", "supply_score",
        "confidence_score", "market_opportunity_score", "opportunity_level"
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    top_candidates = df.sort_values(
        "market_opportunity_score", ascending=False
    ).head(10)

    immediate_candidates = df[
        (df["market_opportunity_score"] >= 20)
        & (df["confidence_score"] >= 0.7)
    ].sort_values("market_opportunity_score", ascending=False)

    experimental_candidates = df[
        (df["market_opportunity_score"] >= 10)
        & (df["confidence_score"] < 0.7)
    ].sort_values("market_opportunity_score", ascending=False)

    saturated_markets = df[
        df["supply_score"] >= 80
    ].sort_values("subgenre_impact_score", ascending=False)

    theme_summary = (
        df.groupby("theme")
        .agg(
            subgenre_count=("subgenre", "count"),
            avg_market_opportunity_score=("market_opportunity_score", "mean"),
            avg_impact_score=("subgenre_impact_score", "mean"),
            avg_confidence_score=("confidence_score", "mean"),
            total_views=("total_views", "sum"),
            avg_engagement_rate=("avg_engagement_rate", "mean"),
        )
        .reset_index()
        .sort_values("avg_market_opportunity_score", ascending=False)
    )

    report = []

    report.append("# Subgenre Market Opportunity Recommendation Report\n\n")

    report.append("## 1. Research Goal\n\n")
    report.append(
        "本阶段分析的目标是进一步解决团队提出的核心问题："
        "如何锁定若干需求较大、供给相对不足、可以指导未来 AI 生成音乐的曲风方向。\n\n"
    )

    report.append(
        "上一阶段的 genre-level analysis 可以判断一级曲风的整体表现，"
        "但一级曲风过于宽泛，例如 Jazz、Lofi、Pop 内部包含很多不同使用场景。"
        "因此，本阶段进一步从 YouTube title / description 中提取 theme，"
        "并构建 subgenre 维度，例如 study lofi、cafe jazz、nostalgia city pop，"
        "从而更具体地判断哪些曲风组合值得进入下一轮 AI music generation test。\n\n"
    )

    report.append("## 2. Updated Scoring Logic\n\n")
    report.append(
        "为了避免仅凭 1–2 个爆款视频误判市场机会，本阶段在原有 Opportunity Score 的基础上新增了 Confidence Score。\n\n"
    )

    report.append("### 2.1 Impact Score\n\n")
    report.append(
        "Impact Score 衡量一个细分曲风的综合需求强度，综合考虑播放量、点赞率、评论率和互动率。\n\n"
    )

    report.append("### 2.2 Supply Score\n\n")
    report.append(
        "Supply Score 使用 video_count 作为供给 / 竞争程度的代理变量。"
        "视频数量越多，说明该细分曲风已有供给越多，竞争越高。\n\n"
    )

    report.append("### 2.3 Confidence Score\n\n")
    report.append(
        "Confidence Score 用于衡量当前样本是否足够可靠。"
        "如果某个 subgenre 只有 1 个视频，即使它播放量很高，也不能直接判断为稳定机会；"
        "如果某个 subgenre 有更多视频样本，说明这个方向的市场信号更稳定。\n\n"
    )

    report.append("### 2.4 Market Opportunity Score\n\n")
    report.append(
        "最终 Market Opportunity Score 结合三层逻辑：需求强度、样本可信度和低竞争程度。\n\n"
    )

    report.append(
        "> Market Opportunity Score = Impact Score × Confidence Score × (1 - Supply Score / 100)\n\n"
    )

    report.append(
        "这个分数比原始 Impact - Supply 更稳健，可以减少单个爆款视频对排名的影响，"
        "更适合用于筛选未来 AI 音乐生成方向。\n\n"
    )

    report.append("## 3. Top Market Opportunity Candidates\n\n")
    report.append(
        "| Rank | Genre | Theme | Subgenre | Videos | Total Views | Engagement Rate | Impact | Supply | Confidence | Market Opportunity | Level |\n"
    )
    report.append("|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|\n")

    for idx, (_, row) in enumerate(top_candidates.iterrows(), start=1):
        report.append(
            f"| {idx} "
            f"| {row['genre']} "
            f"| {row['theme']} "
            f"| {row['subgenre']} "
            f"| {format_number(row['video_count'])} "
            f"| {format_number(row['total_views'])} "
            f"| {format_rate(row['avg_engagement_rate'])} "
            f"| {format_score(row['subgenre_impact_score'])} "
            f"| {format_score(row['supply_score'])} "
            f"| {format_score(row['confidence_score'])} "
            f"| {format_score(row['market_opportunity_score'])} "
            f"| {row['opportunity_level']} |\n"
        )

    report.append("\n## 4. Actionable Recommendation Tiers\n\n")

    report.append("### 4.1 Immediate Production Candidates\n\n")
    if len(immediate_candidates) > 0:
        report.append(
            "这些方向同时具备较高 Market Opportunity Score 和较高 Confidence Score，"
            "可以作为下一轮 AI-generated music 的优先生成方向。\n\n"
        )
        for _, row in immediate_candidates.iterrows():
            report.append(
                f"- **{row['subgenre']}**: Market Opportunity = {format_score(row['market_opportunity_score'])}, "
                f"Impact = {format_score(row['subgenre_impact_score'])}, "
                f"Supply = {format_score(row['supply_score'])}, "
                f"Confidence = {format_score(row['confidence_score'])}, "
                f"Videos = {format_number(row['video_count'])}.\n"
            )
    else:
        report.append(
            "当前样本中暂无同时满足高机会分和高置信度的 Immediate Production Candidate。"
            "这说明下一步需要扩大样本量，尤其是增加更多 subgenre query。\n"
        )

    report.append("\n### 4.2 Experimental Candidates\n\n")
    if len(experimental_candidates) > 0:
        report.append(
            "这些方向具有一定机会信号，但 Confidence Score 仍然偏低，"
            "更适合作为小规模 Suno 生成和真实发布 A/B test 的候选方向，而不是直接大规模生产。\n\n"
        )
        for _, row in experimental_candidates.head(10).iterrows():
            report.append(
                f"- **{row['subgenre']}**: Market Opportunity = {format_score(row['market_opportunity_score'])}, "
                f"Confidence = {format_score(row['confidence_score'])}, "
                f"Videos = {format_number(row['video_count'])}. "
                f"建议先做小规模测试。\n"
            )
    else:
        report.append("当前样本中暂无明显 Experimental Candidate。\n")

    report.append("\n### 4.3 Saturated Markets\n\n")
    if len(saturated_markets) > 0:
        report.append(
            "以下方向 Impact 可能较高，但 Supply Score 也很高，说明市场供给充足、竞争较强。"
            "不建议直接以 broad subgenre 方式进入，应进一步通过国家、语言、主题或情绪细分。\n\n"
        )
        for _, row in saturated_markets.head(10).iterrows():
            report.append(
                f"- **{row['subgenre']}**: Impact = {format_score(row['subgenre_impact_score'])}, "
                f"Supply = {format_score(row['supply_score'])}, "
                f"Market Opportunity = {format_score(row['market_opportunity_score'])}.\n"
            )
    else:
        report.append("当前样本中暂无明显 Saturated Market。\n")

    report.append("\n## 5. Theme-Level Findings\n\n")
    report.append(
        "| Theme | Subgenre Count | Avg Market Opportunity | Avg Impact | Avg Confidence | Total Views | Avg Engagement Rate |\n"
    )
    report.append("|---|---:|---:|---:|---:|---:|---:|\n")

    for _, row in theme_summary.iterrows():
        report.append(
            f"| {row['theme']} "
            f"| {format_number(row['subgenre_count'])} "
            f"| {format_score(row['avg_market_opportunity_score'])} "
            f"| {format_score(row['avg_impact_score'])} "
            f"| {format_score(row['avg_confidence_score'])} "
            f"| {format_number(row['total_views'])} "
            f"| {format_rate(row['avg_engagement_rate'])} |\n"
        )

    report.append("\n## 6. Production Guidance\n\n")
    report.append(
        "当前结果说明，未来 AI music production 不应该只基于 broad genre 进行决策，"
        "而应该逐渐转向 genre + theme + market 的组合推荐。\n\n"
    )

    report.append("具体来说：\n\n")
    report.append(
        "1. 如果某个 subgenre 的 Market Opportunity Score 高且 Confidence Score 高，"
        "它可以进入 Immediate Production Candidate。\n"
    )
    report.append(
        "2. 如果某个 subgenre Opportunity 高但 Confidence 低，说明它可能只是少数视频带来的信号，"
        "应该先进入 Experimental Candidate，通过 Suno 生成少量歌曲做真实 A/B test。\n"
    )
    report.append(
        "3. 如果某个方向 Impact 高但 Supply 也高，说明它是红海市场，"
        "不建议直接进入，需要进一步细分主题、国家、语言或情绪。\n\n"
    )

    report.append("## 7. Recommended Next Experiments\n\n")
    report.append(
        "下一轮不建议直接大规模生成 broad genre 音乐，而应该围绕候选 subgenre 设计小规模实验：\n\n"
    )

    for _, row in top_candidates.head(5).iterrows():
        report.append(
            f"- Test **{row['subgenre']}**: genre = {row['genre']}, theme = {row['theme']}, "
            f"market opportunity = {format_score(row['market_opportunity_score'])}. "
            f"建议生成 3–5 首变体，观察 views、likes、comments 和后续 revenue。\n"
        )

    report.append("\n## 8. Current Limitations\n\n")
    report.append(
        "当前 theme classification 仍然基于 keyword matching，属于第一版规则分类。"
        "后续可以升级为 NLP embedding、topic modeling 或 LLM-based classification，以提高主题识别准确性。\n\n"
    )

    report.append(
        "当前 Supply Score 仍然只用 YouTube video_count 近似表示供给。"
        "未来可以加入 Spotify track count、iTunes catalog count、TikTok video count、发布时间窗口和国家维度，"
        "形成更完整的供需矩阵。\n\n"
    )

    report.append(
        "最后，当前结果仍然属于 observational analysis。"
        "真正的 A/B test 需要用 Suno 生成可控歌曲，并控制 title format、cover style、release time、language、country 和 promotion level。\n"
    )

    report.append("\n## 9. Related Figures\n\n")
    report.append("![Top Subgenre Market Opportunity Score](../figures/top_subgenre_market_opportunity_score.png)\n\n")
    report.append("![Subgenre Demand vs Supply](../figures/subgenre_demand_vs_supply.png)\n\n")
    report.append("![Theme Market Opportunity Score](../figures/theme_market_opportunity_score.png)\n\n")
    report.append("![Subgenre Confidence Score](../figures/subgenre_confidence_score.png)\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(report)

    print(f"Report generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()