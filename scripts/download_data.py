"""Download the UCI 'Sentiment Labelled Sentences' dataset (CC BY 4.0).

Only the Amazon cell-phone file is used: 1,000 one-sentence product reviews,
each labelled positive (1) or negative (0).
"""
import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
MEMBER = "sentiment labelled sentences/amazon_cells_labelled.txt"


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / "amazon_cells_labelled.txt"
    if out.exists():
        print(f"already present: {out}")
        return
    with urllib.request.urlopen(URL, timeout=60) as resp:
        payload = resp.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        out.write_bytes(zf.read(MEMBER))
    print(f"saved {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
