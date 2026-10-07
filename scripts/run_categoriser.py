"""Label every review with a theme and write data/processed/labelled_<backend>.csv.

--backend auto (default) uses Claude if ANTHROPIC_API_KEY is set, else the
offline keyword baseline.
"""
import argparse
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reviewcat import baseline, llm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "processed" / "reviews.csv"


def main() -> None:
    load_dotenv(ROOT / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["auto", "baseline", "llm"], default="auto")
    args = ap.parse_args()
    backend = args.backend
    if backend == "auto":
        backend = "llm" if llm.has_key() else "baseline"

    df = pd.read_csv(IN)
    if backend == "llm":
        labels = llm.classify_many(df["review_id"].tolist(), df["text"].tolist())
        df["theme"] = df["review_id"].map(labels)
    else:
        df["theme"] = baseline.classify_many(df["text"].tolist())

    out = ROOT / "data" / "processed" / f"labelled_{backend}.csv"
    df.to_csv(out, index=False)
    print(f"backend={backend}  rows={len(df)}  -> {out.relative_to(ROOT)}")
    print(df["theme"].value_counts().to_string())


if __name__ == "__main__":
    main()
