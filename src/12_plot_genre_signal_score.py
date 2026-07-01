import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE = "data/genre_signal_opportunity_score.csv"

FIGURE_DIR = "figures"
Path(FIGURE_DIR).mkdir(exist_ok=True)


def main():
    df = pd.read_csv(INPUT_FILE)

    # 1. Opportunity Score 排名图
    opportunity_df = df.sort_values("opportunity_score", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(opportunity_df["genre"], opportunity_df["opportunity_score"])
    plt.xlabel("Opportunity Score")
    plt.ylabel("Genre")
    plt.title("Genre Opportunity Score")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/genre_opportunity_score.png", dpi=300)
    plt.close()

    # 2. Impact Score 排名图
    impact_df = df.sort_values("genre_impact_score", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(impact_df["genre"], impact_df["genre_impact_score"])
    plt.xlabel("Genre Impact Score")
    plt.ylabel("Genre")
    plt.title("Genre Impact Score")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/genre_impact_score.png", dpi=300)
    plt.close()

    # 3. Demand vs Supply 散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(df["supply_score"], df["genre_impact_score"])

    for _, row in df.iterrows():
        plt.text(
            row["supply_score"],
            row["genre_impact_score"],
            row["genre"],
            fontsize=8
        )

    plt.xlabel("Supply Score")
    plt.ylabel("Genre Impact Score")
    plt.title("Demand vs Supply by Genre")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/genre_demand_vs_supply.png", dpi=300)
    plt.close()

    print("Saved figures:")
    print(f"{FIGURE_DIR}/genre_opportunity_score.png")
    print(f"{FIGURE_DIR}/genre_impact_score.png")
    print(f"{FIGURE_DIR}/genre_demand_vs_supply.png")


if __name__ == "__main__":
    main()