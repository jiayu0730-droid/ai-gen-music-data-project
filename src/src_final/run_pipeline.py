"""
Run the complete AI Music Market Analysis pipeline.

Pipeline:

1. Collect public data
2. Analyze and score
3. Generate figures and reports
"""

import subprocess
import sys


def run(script):
    print("=" * 60)
    print(f"Running {script}")
    print("=" * 60)

    subprocess.run(
        [sys.executable, script],
        check=True
    )


def main():

    run("src_final/01_collect_data.py --all")

    run("src_final/02_analyze_and_score.py")

    run("src_final/03_generate_reports.py")

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
    