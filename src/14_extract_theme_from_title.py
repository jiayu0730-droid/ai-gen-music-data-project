import pandas as pd
from pathlib import Path

INPUT_FILE = "data/youtube_public_video_metrics.csv"
OUTPUT_FILE = "data/youtube_theme_classification.csv"


THEME_KEYWORDS = {
    "cafe": ["cafe", "coffee", "coffee shop", "restaurant"],
    "study": ["study", "focus", "work", "deep work", "coding"],
    "sleep": ["sleep", "night", "dream", "bedtime"],
    "rain": ["rain", "rainy", "storm"],
    "summer": ["summer", "beach", "vacation"],
    "nostalgia": ["nostalgia", "nostalgic", "retro", "memory", "memories"],
    "romance": ["love", "romance", "romantic", "heartbreak"],
    "gaming": ["gaming", "game", "cyber", "synthwave"],
    "workout": ["workout", "gym", "fitness", "running"],
    "party": ["party", "festival", "club", "dance"],
    "spiritual": ["devotional", "prayer", "meditation", "worship"],
}


def classify_theme(text):
    text = str(text).lower()

    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return theme

    return "general"


def build_subgenre(row):
    genre = str(row.get("genre", "")).lower().strip()
    theme = str(row.get("theme", "")).lower().strip()

    if not genre:
        genre = "unknown"

    if theme == "general" or not theme:
        return genre

    return f"{theme} {genre}"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("Loaded columns:")
    print(df.columns.tolist())

    if "video_title" in df.columns:
        df["title_text"] = df["video_title"].astype(str)
    elif "title" in df.columns:
        df["title_text"] = df["title"].astype(str)
    else:
        df["title_text"] = ""

    if "description" in df.columns:
        df["description_text"] = df["description"].astype(str)
    else:
        df["description_text"] = ""

    if "genre" not in df.columns:
        raise ValueError("Missing required column: genre")

    df["combined_text"] = df["title_text"] + " " + df["description_text"]

    df["theme"] = df["combined_text"].apply(classify_theme)
    df["subgenre"] = df.apply(build_subgenre, axis=1)

    Path("data").mkdir(exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTheme classification complete.")
    print(df[["genre", "theme", "subgenre"]].head(20).to_string(index=False))
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()