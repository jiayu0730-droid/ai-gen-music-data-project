import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE = "data/subgenre_opportunity_score.csv"
FIGURE_DIR = "figures"

Path(FIGURE_DIR).mkdir(exist_ok=True)


def main():
    df = pd.read_csv(INPUT_FILE)

    required_cols = [
        "subgenre", "theme", "supply_score",
        "subgenre_impact_score", "confidence_score",
        "market_opportunity_score"
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Figure 1: Top market opportunity subgenres
    top_df = (
        df.sort_values("market_opportunity_score", ascending=False)
        .head(15)
        .sort_values("market_opportunity_score", ascending=True)
    )

    plt.figure(figsize=(10, 7))
    plt.barh(top_df["subgenre"], top_df["market_opportunity_score"])
    plt.xlabel("Market Opportunity Score")
    plt.ylabel("Subgenre")
    plt.title("Top Subgenre Market Opportunity Scores")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/top_subgenre_market_opportunity_score.png", dpi=300)
    plt.close()

    # Figure 2: Demand vs supply
    plt.figure(figsize=(9, 7))
    plt.scatter(df["supply_score"], df["subgenre_impact_score"])

    label_df = df.sort_values("market_opportunity_score", ascending=False).head(15)

    for _, row in label_df.iterrows():
        plt.text(
            row["supply_score"],
            row["subgenre_impact_score"],
            row["subgenre"],
            fontsize=8
        )

    plt.xlabel("Supply / Competition Score")
    plt.ylabel("Subgenre Impact Score")
    plt.title("Subgenre Demand vs Supply")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/subgenre_demand_vs_supply.png", dpi=300)
    plt.close()

    # Figure 3: Theme-level average market opportunity
    theme_df = (
        df.groupby("theme")
        .agg(
            avg_market_opportunity_score=("market_opportunity_score", "mean"),
            avg_impact_score=("subgenre_impact_score", "mean"),
            avg_confidence_score=("confidence_score", "mean"),
            subgenre_count=("subgenre", "count"),
        )
        .reset_index()
        .sort_values("avg_market_opportunity_score", ascending=True)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(theme_df["theme"], theme_df["avg_market_opportunity_score"])
    plt.xlabel("Average Market Opportunity Score")
    plt.ylabel("Theme")
    plt.title("Average Market Opportunity Score by Theme")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/theme_market_opportunity_score.png", dpi=300)
    plt.close()

    # Figure 4: Confidence score by top subgenre
    confidence_df = (
        df.sort_values("market_opportunity_score", ascending=False)
        .head(15)
        .sort_values("confidence_score", ascending=True)
    )

    plt.figure(figsize=(10, 7))
    plt.barh(confidence_df["subgenre"], confidence_df["confidence_score"])
    plt.xlabel("Confidence Score")
    plt.ylabel("Subgenre")
    plt.title("Confidence Score of Top Subgenre Candidates")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/subgenre_confidence_score.png", dpi=300)
    plt.close()

    print("Saved figures:")
    print(f"{FIGURE_DIR}/top_subgenre_market_opportunity_score.png")
    print(f"{FIGURE_DIR}/subgenre_demand_vs_supply.png")
    print(f"{FIGURE_DIR}/theme_market_opportunity_score.png")
    print(f"{FIGURE_DIR}/subgenre_confidence_score.png")


if __name__ == "__main__":
    main()