"""Score a backend's theme labels against the hand-labelled gold sample.

Writes results/evaluation_<backend>.md and results/charts/confusion_<backend>.png.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
import sys  # noqa: E402
sys.path.insert(0, str(ROOT))
from reviewcat.taxonomy import THEME_NAMES  # noqa: E402

SAMPLE_SIZE, SEED = 150, 42


def draw_sample(reviews: pd.DataFrame) -> pd.DataFrame:
    return reviews.sample(SAMPLE_SIZE, random_state=SEED).sort_values("review_id")


def per_theme_scores(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for t in THEME_NAMES:
        tp = int(((merged.theme == t) & (merged.gold_theme == t)).sum())
        pred = int((merged.theme == t).sum())
        gold = int((merged.gold_theme == t).sum())
        p = tp / pred if pred else 0.0
        r = tp / gold if gold else 0.0
        f1 = 2 * p * r / (p + r) if p + r else 0.0
        rows.append({"theme": t, "gold": gold, "predicted": pred, "correct": tp,
                     "precision": round(p, 3), "recall": round(r, 3), "f1": round(f1, 3)})
    return pd.DataFrame(rows)


def confusion(merged: pd.DataFrame) -> pd.DataFrame:
    return pd.crosstab(merged.gold_theme, merged.theme).reindex(
        index=THEME_NAMES, columns=THEME_NAMES, fill_value=0)


def chart(cm: pd.DataFrame, path: Path, backend: str, acc: float) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    ax.imshow(cm.values, cmap="Blues")
    ax.set_xticks(range(len(cm.columns)), cm.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(cm.index)), cm.index, fontsize=8)
    vmax = cm.values.max()
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            v = cm.iat[i, j]
            if v:
                ax.text(j, i, v, ha="center", va="center", fontsize=8,
                        color="white" if v > vmax / 2 else "black")
    ax.set_xlabel(f"{backend} label")
    ax.set_ylabel("gold label")
    ax.set_title(f"{backend} vs gold sample (n={cm.values.sum()}, accuracy {acc:.1%})")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="baseline")
    ap.add_argument("--draw-sample", action="store_true", help="print the sample to label and exit")
    args = ap.parse_args()
    if args.draw_sample:
        for r in draw_sample(pd.read_csv(ROOT / "data/processed/reviews.csv")).itertuples():
            print(r.review_id, "|", r.text)
        return

    gold = pd.read_csv(ROOT / "data/gold/gold_labels.csv")
    pred = pd.read_csv(ROOT / "data/processed" / f"labelled_{args.backend}.csv")
    merged = gold.merge(pred, on="review_id", how="left", validate="1:1")
    assert merged.theme.notna().all(), "gold review missing from predictions"

    acc = (merged.theme == merged.gold_theme).mean()
    scores = per_theme_scores(merged)
    cm = confusion(merged)
    specific = merged[merged.gold_theme != "general_sentiment"]
    to_general = (specific.theme == "general_sentiment").mean()
    (ROOT / "results/charts").mkdir(parents=True, exist_ok=True)
    chart(cm, ROOT / "results/charts" / f"confusion_{args.backend}.png", args.backend, acc)

    errors = merged[merged.theme != merged.gold_theme][["review_id", "text", "sentiment", "gold_theme", "theme"]]
    md = [f"# Evaluation: {args.backend} vs gold sample", "",
          f"- Gold reviews: {len(merged)} (labelling rules: `data/gold/LABELLING_GUIDE.md`)",
          f"- Accuracy: **{acc:.1%}**",
          f"- Macro F1 (9 themes): **{scores.f1.mean():.3f}**",
          f"- Reviews with a specific gold theme: {len(specific)}; "
          f"{to_general:.1%} of them were put in `general_sentiment`", "",
          "## Per theme", "", scores.to_markdown(index=False), "",
          "## Confusion matrix (rows = gold, columns = predicted)", "", cm.to_markdown(), "",
          f"## Disagreements ({len(errors)})", "", errors.to_markdown(index=False), ""]
    (ROOT / "results" / f"evaluation_{args.backend}.md").write_text("\n".join(md))
    print("\n".join(md[:7]))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
