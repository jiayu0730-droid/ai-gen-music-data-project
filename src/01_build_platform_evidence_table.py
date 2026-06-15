"""
Step 1: Build platform evidence table for AI-generated music market research.

Goal:
- Separate what can be measured through public APIs from what requires dashboard/manual royalty exports.
- Convert platform observations into a prioritized data collection plan.

Run from project root:
python src/01_build_platform_evidence_table.py
"""

from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
REPORT_DIR = Path("reports")


def load_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Put the CSV in the data/ folder first.")
    return pd.read_csv(path)


def build_platform_evidence_table() -> None:
    sources = load_csv("platform_data_sources_step1.csv")
    observations = load_csv("platform_observation_seed.csv")

    # Priority logic: this is intentionally simple and explainable for Week 1.
    priority_map = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    observations["confidence_score"] = (
        observations["confidence_level"]
        .str.lower()
        .map(priority_map)
        .fillna(1)
    )

    # Platforms with actionable data should be handled first.
    actionable_keywords = ["export", "collect", "api", "manual"]
    observations["actionable"] = observations["next_action"].str.lower().apply(
        lambda x: any(k in x for k in actionable_keywords)
    )

    observations["data_collection_priority"] = observations["confidence_score"] + observations["actionable"].astype(int)

    priority = observations.sort_values(
        ["data_collection_priority", "confidence_score"],
        ascending=False,
    )

    # Merge source availability into observation table.
    merged = priority.merge(
        sources[[
            "platform",
            "platform_group",
            "public_data_available",
            "actual_method",
            "metrics_available_or_needed",
            "how_to_use_in_project",
        ]],
        on="platform",
        how="left",
    )

    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    merged.to_csv(DATA_DIR / "platform_evidence_priority.csv", index=False)

    platform_summary = (
        merged.groupby(["platform", "platform_group", "public_data_available", "actual_method"], dropna=False)
        .agg(
            num_observations=("claim_or_observation", "count"),
            avg_priority=("data_collection_priority", "mean"),
            key_metrics=("metrics_available_or_needed", "first"),
            project_use=("how_to_use_in_project", "first"),
        )
        .reset_index()
        .sort_values("avg_priority", ascending=False)
    )

    platform_summary.to_csv(DATA_DIR / "platform_evidence_summary.csv", index=False)

    # Markdown report snippet for Week 1 slides/report.
    md_lines = [
        "# Platform Streaming Data Evidence Plan\n",
        "\n## Key idea\n",
        "For Week 1, the analysis should separate public engagement data from private royalty/dashboard data. ",
        "The current objective is to validate audience demand and market fit before optimizing for revenue.\n",
        "\n## Prioritized platforms\n",
    ]

    for _, row in platform_summary.iterrows():
        md_lines.append(
            f"- **{row['platform']}**: method = {row['actual_method']}; "
            f"metrics = {row['key_metrics']}; use = {row['project_use']}"
        )

    md_lines.append("\n## Next data to collect\n")
    for _, row in priority.head(10).iterrows():
        md_lines.append(
            f"- **{row['platform']}** — {row['claim_or_observation']} → {row['next_action']}"
        )

    (REPORT_DIR / "platform_streaming_evidence_plan.md").write_text("\n".join(md_lines), encoding="utf-8")

    print("Saved:")
    print(DATA_DIR / "platform_evidence_priority.csv")
    print(DATA_DIR / "platform_evidence_summary.csv")
    print(REPORT_DIR / "platform_streaming_evidence_plan.md")


if __name__ == "__main__":
    build_platform_evidence_table()
