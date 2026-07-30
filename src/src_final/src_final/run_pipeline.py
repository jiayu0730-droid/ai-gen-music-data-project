"""
Run the complete final AI music market analysis pipeline.

Full refresh:
    python src/src_final/run_pipeline.py

Reuse existing data and skip API collection:
    python src/src_final/run_pipeline.py --skip-collection
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


# 当前文件所在目录：
# AI-GEN-MUSIC-DATA-PROJECT/src/src_final/
FINAL_DIR = Path(__file__).resolve().parent

# 项目根目录：
# AI-GEN-MUSIC-DATA-PROJECT/
PROJECT_ROOT = FINAL_DIR.parent.parent


def run_step(
    script_name: str,
    extra_args: list[str] | None = None,
) -> None:
    """
    Run one Python script in the pipeline.

    Parameters
    ----------
    script_name:
        Name of the Python script located in FINAL_DIR.
    extra_args:
        Optional command-line arguments passed to the script.
    """

    script_path = FINAL_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Missing pipeline script: {script_path}"
        )

    command = [
        sys.executable,
        str(script_path),
    ]

    if extra_args:
        command.extend(extra_args)

    print("\n" + "=" * 70)
    print(f"Running: {' '.join(command)}")
    print("=" * 70)

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
    )


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Run the final AI music market analysis "
            "and song scoring pipeline."
        )
    )

    parser.add_argument(
        "--skip-collection",
        action="store_true",
        help=(
            "Skip API data collection and reuse existing CSV files "
            "from the data folder."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """
    Run the complete pipeline in order.
    """

    args = parse_args()

    # Step 1: Collect or reuse platform market data.
    if not args.skip_collection:
        run_step(
            "01_collect_data.py",
            ["--all"],
        )
    else:
        print(
            "\nSkipping data collection. "
            "Existing CSV files will be reused."
        )

    # Step 2: Analyze platform data and calculate market scores.
    run_step("02_analyze_and_score.py")

    # Step 3: Generate market reports, tables, and figures.
    run_step("03_generate_outputs.py")

    # Step 4: Match the 50 songs with market opportunity scores
    # and generate the song-level scoring table.
    run_step("04_prepare_song_scores.py")

    print("\n" + "=" * 70)
    print("Pipeline completed successfully.")
    print("=" * 70)

    print("\nGenerated outputs are available in:")
    print(f"- Data:        {PROJECT_ROOT / 'data'}")
    print(f"- Song scores: {PROJECT_ROOT / 'data' / 'song_scores.csv'}")
    print(f"- Unmatched:   {PROJECT_ROOT / 'data' / 'song_score_unmatched.csv'}")
    print(f"- Figures:     {PROJECT_ROOT / 'figures'}")
    print(f"- Reports:     {PROJECT_ROOT / 'reports'}")


if __name__ == "__main__":
    main()
    