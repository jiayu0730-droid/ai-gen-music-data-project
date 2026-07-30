"""Quick local tests for tools and the natural-language agent."""

from agent.tools import find_track, rank_tracks


def main() -> None:
    print("=== Direct tool test ===")
    print(find_track(track_id="P01B"))

    print("\n=== Top 3 test ===")
    print(rank_tracks(3))

    print(
        "\nDirect tools work. To test the AI agent, run:\n"
        'python -c "from agent.music_score_agent import ask_music_agent; '
        "print(ask_music_agent('帮我看 P01B 的评分'))""
    )


if __name__ == "__main__":
    main()
