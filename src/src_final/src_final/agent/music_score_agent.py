"""
GoldenAI natural-language music score agent.

This agent lets users ask questions such as:
- 帮我看一下 P01B 的评分
- P01A 和 P01B 哪个更适合先发行
- 给我评分最高的五首歌曲
- 哪些歌曲的数据还不完整
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


# ============================================================
# 1. Locate and load the project-level .env file
# ============================================================

# Current file:
# project/src/src_final/src_final/agent/music_score_agent.py
#
# parents[0] = agent
# parents[1] = inner src_final
# parents[2] = outer src_final
# parents[3] = src
# parents[4] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(
    dotenv_path=ENV_PATH,
    override=False,
)

API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
MODEL = (os.getenv("OPENAI_MODEL") or "gpt-5-mini").strip()

if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY could not be loaded.\n"
        f"Expected .env file at: {ENV_PATH}\n"
        "Please confirm the file contains:\n"
        "OPENAI_API_KEY=your_real_key"
    )


# ============================================================
# 2. Import Agents SDK and local scoring tools
# ============================================================

from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_key,
)

from .tools import (
    compare_tracks,
    find_track,
    get_missing_data,
    rank_tracks,
)


# ============================================================
# 3. Explicitly provide the API key to the Agents SDK
# ============================================================

# Do not paste the actual sk-... key here.
# API_KEY is the variable already loaded from the project .env file.
set_default_openai_key(
    API_KEY,
    use_for_tracing=True,
)


# ============================================================
# 4. Agent instructions
# ============================================================

SYSTEM_PROMPT = """
You are GoldenAI Music Score Assistant.

You help users understand the current pre-release scores for a catalog of
50 AI-generated songs.

The user may ask questions in Chinese or English.

You must use the provided tools whenever the user asks about:
- a specific song
- a song score
- market opportunity
- song comparison
- ranking
- missing data
- release recommendations

Important rules:

1. Never invent a song, title, score, market, or recommendation.

2. Clearly distinguish these fields:
   - market_score:
     Current market opportunity evidence.
   - final_score or pre_release_score:
     Current combined pre-release score.
   - metadata_score:
     Completeness of the song metadata.
   - lyric_score:
     AI lyric-fit score, if available.
   - audio_score:
     Audio technical-quality score, if available.
   - confidence:
     Completeness and reliability of the supporting data.

3. The current scores may be provisional.
   When score_status is provisional, explicitly tell the user that it is a
   temporary pre-release score rather than a prediction of actual streams.

4. Do not claim that a song will definitely become popular.

5. If lyric_score or audio_score is missing, explain that the score has not
   yet been calculated. Do not treat missing values as zero.

6. If the requested song cannot be found, ask the user for a precise track ID,
   such as P01B, or a more exact song title.

7. Answer in concise, natural Chinese unless the user asks for English.

8. For a single-song query, organize the answer with:
   - Track ID and title
   - Market score
   - Combined score and tier
   - Confidence
   - Main strengths
   - Missing evidence
   - Recommended next action

9. For comparisons, clearly state which song currently ranks higher and why.

10. Never expose Python implementation details unless the user specifically
    asks for technical details.
"""


# ============================================================
# 5. JSON cleaning helper
# ============================================================

def make_json_safe(value: Any) -> Any:
    """
    Convert NaN values into None so tool results become valid JSON.
    """

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, float) and math.isnan(value):
        return None

    return value


def serialize_result(result: Any) -> str:
    """
    Convert tool output into safe JSON text.
    """

    cleaned = make_json_safe(result)

    return json.dumps(
        cleaned,
        ensure_ascii=False,
        allow_nan=False,
        default=str,
    )


# ============================================================
# 6. Function tools available to the AI agent
# ============================================================

@function_tool
def get_track_score(
    track_id: str = "",
    title: str = "",
) -> str:
    """
    Look up one song's current scores.

    Args:
        track_id:
            Stable track ID such as P01B. Leave blank when searching by title.
        title:
            Exact song title or a distinctive portion of the title.
    """

    if not track_id.strip() and not title.strip():
        return serialize_result(
            {
                "found": False,
                "message": (
                    "Please provide either a track ID "
                    "or a song title."
                ),
            }
        )

    result = find_track(
        track_id=track_id.strip() or None,
        title=title.strip() or None,
    )

    return serialize_result(result)


@function_tool
def compare_track_scores(
    first_track_id: str,
    second_track_id: str,
) -> str:
    """
    Compare two songs by their track IDs.

    Args:
        first_track_id:
            First track ID, such as P01A.
        second_track_id:
            Second track ID, such as P01B.
    """

    result = compare_tracks(
        first_track_id.strip(),
        second_track_id.strip(),
    )

    return serialize_result(result)


@function_tool
def get_top_tracks(
    limit: int = 10,
) -> str:
    """
    Return the highest-scoring songs.

    Args:
        limit:
            Number of tracks to return, from 1 to 50.
    """

    safe_limit = max(
        1,
        min(int(limit), 50),
    )

    result = rank_tracks(safe_limit)

    return serialize_result(result)


@function_tool
def list_tracks_needing_data() -> str:
    """
    Return songs with incomplete scoring evidence or low confidence.
    """

    result = get_missing_data()

    return serialize_result(result)


# ============================================================
# 7. Create the music score agent
# ============================================================

music_score_agent = Agent(
    name="GoldenAI Music Score Assistant",
    instructions=SYSTEM_PROMPT,
    model=MODEL,
    tools=[
        get_track_score,
        compare_track_scores,
        get_top_tracks,
        list_tracks_needing_data,
    ],
)


# ============================================================
# 8. Public function used by Terminal or Streamlit
# ============================================================

def ask_music_agent(message: str) -> str:
    """
    Send one natural-language question to the music score agent.
    """

    cleaned_message = message.strip()

    if not cleaned_message:
        raise ValueError(
            "Message cannot be empty."
        )

    result = Runner.run_sync(
        music_score_agent,
        cleaned_message,
    )

    return str(result.final_output)


# ============================================================
# 9. Optional direct-file test
# ============================================================

if __name__ == "__main__":
    test_question = (
        "帮我看一下 P01B 的市场评分、综合评分和发行建议。"
    )

    print(
        ask_music_agent(test_question)
    )