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


FINAL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FINAL_DIR.parent.parent


def run_step(
    script_name: str,
    extra_args: list[str] | None = None,
) -> None:
    script_path = FINAL_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Missing pipeline script: {script_path}")

    command = [sys.executable, str(script_path)]

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
    parser = argparse.ArgumentParser(
        description="Run the final AI music market analysis pipeline."
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
    args = parse_args()

    if not args.skip_collection:
        run_step(
            "01_collect_data.py",
            ["--all"],
        )
    else:
        print("\nSkipping data collection. Existing CSV files will be reused.")

    run_step("02_analyze_and_score.py")
    run_step("03_generate_outputs.py")

    print("\n" + "=" * 70)
    print("Pipeline completed successfully.")
    print("=" * 70)

    print("\nGenerated outputs are available in:")
    print(f"- Data:    {PROJECT_ROOT / 'data'}")
    print(f"- Figures: {PROJECT_ROOT / 'figures'}")
    print(f"- Reports: {PROJECT_ROOT / 'reports'}")


if __name__ == "__main__":
    main()
    