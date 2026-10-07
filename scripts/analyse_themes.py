"""Theme x sentiment summary: which themes drive negative feedback?

Writes results/theme_summary_<backend>.md and results/charts/negative_share_<backend>.png.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def theme_table(df: pd.DataFrame) -> pd.DataFrame:
    t = (df.groupby("theme")["sentiment"].value_counts().unstack(fill_value=0)
           .reindex(columns=["negative", "positive"], fill_value=0))
    t["reviews"] = t.sum(axis=1)
    t["share_of_reviews_pct"] = (100 * t["reviews"] / t["reviews"].sum()).round(1)
    t["negative_rate_pct"] = (100 * t["negative"] / t["reviews"]).round(1)
    t["share_of_all_negatives_pct"] = (100 * t["negative"] / t["negative"].sum()).round(1)
    return t.sort_values("negative", ascending=False)


def chart(t: pd.DataFrame, path: Path, backend: str) -> None:
    t = t.drop(index="general_sentiment", errors="ignore").sort_values("negative")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(t.index, t["negative"], color="#c0504d", label="negative")
    ax.barh(t.index, t["positive"], left=t["negative"], color="#9bbb59", label="positive")
    for y, (n, r) in enumerate(zip(t["negative"], t["negative_rate_pct"])):
        ax.text(t["reviews"].iloc[y] + 1, y, f"{r:.0f}% neg", va="center", fontsize=9)
    ax.set_xlabel("reviews")
    ax.set_title(f"Reviews by theme and sentiment ({backend} labels, excl. general)")
    ax.legend(loc="lower right", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, t["reviews"].max() * 1.18)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="baseline")
    backend = ap.parse_args().backend
    df = pd.read_csv(ROOT / "data" / "processed" / f"labelled_{backend}.csv")
    t = theme_table(df)
    (ROOT / "results" / "charts").mkdir(parents=True, exist_ok=True)
    chart(t, ROOT / "results" / "charts" / f"negative_share_{backend}.png", backend)
    md = [f"# Theme summary ({backend} labels)", "",
          f"{len(df)} reviews, {int(t['negative'].sum())} negative.", "",
          t.reset_index().to_markdown(index=False), ""]
    (ROOT / "results" / f"theme_summary_{backend}.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
