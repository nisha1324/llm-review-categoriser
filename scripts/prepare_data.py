"""Clean the raw reviews into data/processed/reviews.csv with a stable review_id."""
import csv
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "amazon_cells_labelled.txt"
OUT = ROOT / "data" / "processed" / "reviews.csv"


def load_raw(path: Path = RAW) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", header=None, names=["text", "label"],
                     quoting=csv.QUOTE_NONE, dtype={"text": str})
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["text"] = df["text"].str.strip()
    df = df[df["text"].str.len() > 0]
    df = df.drop_duplicates(subset="text").reset_index(drop=True)
    df["sentiment"] = df["label"].map({1: "positive", 0: "negative"})
    df.insert(0, "review_id", [f"r{i:04d}" for i in range(1, len(df) + 1)])
    return df[["review_id", "text", "sentiment"]]


def main() -> None:
    raw = load_raw()
    df = clean(raw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"raw rows: {len(raw)}  after cleaning: {len(df)}  "
          f"(dropped {len(raw) - len(df)} duplicate/empty)")
    print(df["sentiment"].value_counts().to_string())


if __name__ == "__main__":
    main()
