from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[3]
SCORES_FILE = PROJECT_ROOT / "data" / "song_scores.csv"


def load_song_scores() -> pd.DataFrame:
    """读取歌曲评分表。"""

    if not SCORES_FILE.exists():
        raise FileNotFoundError(
            "找不到 data/song_scores.csv。"
            "请先运行 run_pipeline.py。"
        )

    scores = pd.read_csv(SCORES_FILE)

    if scores.empty:
        raise ValueError("song_scores.csv 目前为空。")

    return scores


def find_track(
    track_id: str | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    """根据歌曲编号或歌名查询一首歌曲。"""

    scores = load_song_scores()

    result = pd.DataFrame()

    if track_id:
        result = scores[
            scores["track_id"]
            .astype(str)
            .str.lower()
            .eq(track_id.strip().lower())
        ]

    elif title:
        result = scores[
            scores["title"]
            .astype(str)
            .str.lower()
            .str.contains(
                title.strip().lower(),
                regex=False,
                na=False,
            )
        ]

    else:
        raise ValueError("必须提供 track_id 或 title。")

    if result.empty:
        return {
            "found": False,
            "message": "没有找到对应歌曲。",
            "track_id": track_id,
            "title": title,
        }

    if len(result) > 1:
        return {
            "found": False,
            "message": "找到多首相似歌曲，请提供更准确的编号。",
            "matches": result[
                ["track_id", "title"]
            ].to_dict(orient="records"),
        }

    row = result.iloc[0]

    return {
        "found": True,
        "track_id": row.get("track_id"),
        "title": row.get("title"),
        "subgenre": row.get("subgenre"),
        "target_country": row.get("target_country"),
        "market_score": row.get("market_score"),
        "metadata_score": row.get("metadata_score"),
        "lyric_score": row.get("lyric_score"),
        "audio_score": row.get("audio_score"),
        "final_score": row.get("final_score"),
        "confidence": row.get("confidence"),
        "tier": row.get("tier"),
        "recommendation": row.get("recommendation"),
        "missing_fields": row.get("missing_fields"),
    }


def rank_tracks(limit: int = 10) -> list[dict[str, Any]]:
    """返回评分最高的歌曲。"""

    scores = load_song_scores()

    limit = max(1, min(limit, 50))

    ranked = scores.sort_values(
        "final_score",
        ascending=False,
    ).head(limit)

    return ranked.to_dict(orient="records")


def compare_tracks(
    first_track_id: str,
    second_track_id: str,
) -> dict[str, Any]:
    """比较两首歌曲。"""

    first = find_track(track_id=first_track_id)
    second = find_track(track_id=second_track_id)

    return {
        "first_track": first,
        "second_track": second,
    }


def get_missing_data() -> list[dict[str, Any]]:
    """返回数据不完整的歌曲。"""

    scores = load_song_scores()

    incomplete = scores[
        (scores["confidence"].fillna(0) < 0.8)
        | scores["missing_fields"].fillna("").ne("")
    ]

    return incomplete[
        [
            "track_id",
            "title",
            "confidence",
            "missing_fields",
        ]
    ].to_dict(orient="records")
