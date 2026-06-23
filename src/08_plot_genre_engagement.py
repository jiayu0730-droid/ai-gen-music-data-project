import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE = "data/youtube_genre_engagement_summary.csv"

def main():
    df = pd.read_csv(INPUT_FILE)

    Path("figures").mkdir(exist_ok=True)

    # 图1：不同曲风总播放量
    views_df = df.sort_values("total_views", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(views_df["genre"], views_df["total_views"])
    plt.xlabel("Total Views")
    plt.ylabel("Genre")
    plt.title("Total YouTube Views by Genre")
    plt.tight_layout()
    plt.savefig("figures/genre_total_views.png", dpi=300)
    plt.close()

    # 图2：不同曲风平均点赞率
    like_df = df.sort_values("avg_like_rate", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(like_df["genre"], like_df["avg_like_rate"])
    plt.xlabel("Average Like Rate")
    plt.ylabel("Genre")
    plt.title("Average Like Rate by Genre")
    plt.tight_layout()
    plt.savefig("figures/genre_like_rate.png", dpi=300)
    plt.close()

    # 图3：不同曲风平均评论率
    comment_df = df.sort_values("avg_comment_rate", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(comment_df["genre"], comment_df["avg_comment_rate"])
    plt.xlabel("Average Comment Rate")
    plt.ylabel("Genre")
    plt.title("Average Comment Rate by Genre")
    plt.tight_layout()
    plt.savefig("figures/genre_comment_rate.png", dpi=300)
    plt.close()

    # 图4：总播放量 vs 互动率散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(df["median_views"], df["avg_engagement_rate"])

    for _, row in df.iterrows():
        plt.text(row["median_views"], row["avg_engagement_rate"], row["genre"], fontsize=8)

    plt.xlabel("Median Views")
    plt.ylabel("Average Engagement Rate")
    plt.title("Genre Positioning: Views vs Engagement")
    plt.tight_layout()
    plt.savefig("figures/genre_views_vs_engagement.png", dpi=300)
    plt.close()

    print("Saved figures:")
    print("figures/genre_total_views.png")
    print("figures/genre_like_rate.png")
    print("figures/genre_comment_rate.png")
    print("figures/genre_views_vs_engagement.png")

if __name__ == "__main__":
    main()